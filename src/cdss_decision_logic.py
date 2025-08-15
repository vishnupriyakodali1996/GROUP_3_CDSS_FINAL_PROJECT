import requests
from pathlib import Path
import os
import json
from pprint import pprint
from datetime import datetime

# Importing all the functions needed
from medication import get_medication
from check_obs import check_obs
from check_obs import check_obs_na
from create_obs import save_observation_json
from create_obs import save_observation_json_2
from validate import validate_resource
from post_obs import post_observation_to_hapi
from fetch_pt_data import fetch_patient_data
from eligibility_check import eligibility_condition
BASE_URL = "https://hapi.fhir.org/baseR4"


cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)



def rule_1():
    file_path = data_dir / "patient_list.txt"
    patient_list = []
    with open(file_path, "r") as file:
        for line in file:
            patient_id = line.strip()
            if patient_id:
                patient_list.append(patient_id)

# Checking if the patient has fev1 observation
# If there is no fev1 percentage record for the patient reminder to enter value
# spirometer not available then can ignore this
# If fev1 value is entered then post observation
    fev1_status = check_obs(patient_list)
    for patient_id in patient_list:
        if fev1_status.get(patient_id, False) == False:
            while True:
                choice = input(
                    f"Reminder for patient {patient_id} (FEV1 predicted percentage):\n"
                    "Enter numerical value above 0 for FEV1 percentage or type 'ignore' to skip: "
                ).strip().lower()

                if choice == "ignore":
                    print(
                        f"Clinician chose to skip FEV1 entry for patient {patient_id}. Proceeding to nighttime awakening evaluation."
                    )
                    break

                try:
                    fev1_value = int(choice)
                    if fev1_value < 0:
                        print("Please enter a realistic FEV1 percentage value.")
                        continue

                    obs_file = save_observation_json(patient_id, fev1_value)
                    valid = validate_resource(obs_file)
                    if valid:
                        with open(obs_file, "r") as f:
                            observation = json.load(f)
                        post_observation_to_hapi(observation)
                        fev1_status[patient_id] = True
                    else:
                        print(f"Observation for patient {patient_id} failed validation and was not posted.")

                except ValueError:
                    print("Invalid input.")

# checking for the finding night waking frequency due to asthma
    night_awake_status = check_obs_na(patient_list)
    # Mapping the units
    ucum_map = {
        "week": "wk",
        "month": "mo"
    }
# If observation is missing send the reminder to enter the details
    for patient_id in patient_list:
        if night_awake_status.get(patient_id, False) == False:
            while True:
                try:
                    frequency = int(input(
                        f"Reminder for patient {patient_id} (Asthma causing night waking):\nEnter the frequency (number): "
                    ))
                    frequency_unit = input("Enter measure (week or month): ").strip().lower()

                    print(f"For frequency you entered: {frequency} / {frequency_unit}")

                    unit_code = ucum_map.get(frequency_unit)
                    if not unit_code:
                        print("Invalid unit. Please enter 'week' or 'month'.")
                        continue

                    obs_file = save_observation_json_2(patient_id, frequency, unit_code)# creating observations, saving them as json
                    valid = validate_resource(obs_file) # validating the saved file

                    if valid:
                        with open(obs_file, "r") as f:
                            observation = json.load(f)
                        post_observation_to_hapi(observation)# If validated posting then to HAPI fhir
                        night_awake_status[patient_id] = True
                    else:
                        print(f"Observation for patient {patient_id} failed validation and was not posted.")

                    break

                except ValueError:
                    print("Invalid input.")
    patient_data = fetch_patient_data(patient_list)
    print(patient_data)

    # Treatment recommendation rules
    for patient_sets in fetch_patient_data(patient_list):
        pid = patient_sets.get('patient_id')
        age = patient_sets.get('age')
        fev1_value = patient_sets.get('fev1_value')
        night_awake_value= patient_sets.get('night_awake_value')
        night_awake_unit = patient_sets.get('night_awake_unit')
        # Decision modelled from high to low severity (Recommendation for worst case scenario)
        # Initial severity recommendation based on rules
        if night_awake_unit == 'wk':
            if age >= 12 and (fev1_value < 60 or night_awake_value >= 7):
                severity = "Persistent severe"
            elif age in range(5, 12) and (fev1_value < 60 or night_awake_value >= 7):
                severity = "Persistent severe"
            elif age >= 12 and (fev1_value in range(60, 81) or night_awake_value in range(1, 7)):
                severity = "Persistent moderate"
            elif age in range(5, 12) and (fev1_value in range(60, 81) or night_awake_value in range(1, 7)):
                severity = "Persistent moderate"
        elif night_awake_unit == 'mo':
            if age >= 12 and (fev1_value > 80 or night_awake_value in range(3, 5)):
                severity = "Persistent mild"
            elif age in range(5, 12) and (fev1_value > 80 or night_awake_value in range(3, 5)):
                severity = "Persistent mild"
            elif age >= 5 and (fev1_value > 80 or night_awake_value <= 2):
                severity = "Intermittent"

        # Show initial recommendation
        print(f"\nPatient {pid} initial severity recommendation: {severity}")

        # Assign medication for initial severity
        medication = get_medication(severity, age)

        # Show initial recommendation
        print(f"\nPatient {pid} initial severity recommendation: {severity}")
        print(f"Medication recommendation: {medication}")

        # Clinician override
        while True:
            override = input("----------------------------------------------------\n"
                "Do you want to change the severity based on clinical assessment? (yes/no): ").strip().lower()
            if override == "yes":
                print("Select new severity level:")
                print("1) Intermittent\n2) Persistent mild\n3) Persistent moderate\n4) Persistent severe")
                while True:
                    try:
                        choice = int(input("Enter the number corresponding to severity: "))
                        severity_options = {1: "Intermittent", 2: "Persistent mild",
                                            3: "Persistent moderate", 4: "Persistent severe"}
                        if choice in severity_options:
                            severity = severity_options[choice]
                            medication = get_medication(severity, age)  # recalc medication
                            break
                        else:
                            print("Please enter a valid number (1-4).")
                    except ValueError:
                        print("Invalid input. Enter a number from 1 to 4.")
                break
            elif override == "no":
                # Keep initial severity and medication
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        # Print the final recommendation
        print(f"Final severity recommendation for patient {pid}: {severity}")
        print(f"Medication recommendation: {medication}")

if __name__ == '__main__':
    eligibility_condition()  # creates patient_list.txt for eligible patients

    # Getting patient IDs from eligible patient list
    file_path = data_dir / "patient_list.txt"
    patient_list = []
    if file_path.exists():
        with open(file_path, "r") as f:
            for line in f:
                pid = line.strip()
                if pid:
                    patient_list.append(pid)

    # Run rule_1 if there are eligible patients
    if patient_list:
        rule_1()


