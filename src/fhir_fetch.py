import requests
from pathlib import Path
import os
import json
from pprint import pprint
from datetime import datetime

# Importing all the functions needed
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

''' To check for last updated patients eligible (should have asthma, should not be on asthma meication and age should be
 >4 patients and store their id'''


'''For patients not on long-term medication, check if required measurements exist for decision support; if missing, send 
a reminder, take user input, and create the observation.'''

def rule_1():
    file_path = data_dir / "patient_list.txt"
    patient_list = []
    with open(file_path, "r") as file:
        for line in file:
            patient_id = line.strip()
            if patient_id:
                patient_list.append(patient_id)

# Checking if the patient has fev1 observation, reminder, create
    obs_status = check_obs(patient_list)
    for patient_id in patient_list:
        if obs_status.get(patient_id, False) == False:
            while True:
                try:
                    fev1_value = int(input(f"Reminder for patient {patient_id} (FEV1 predicted percentage):\nEnter FEV1 predicted percentage from following values (integer only): "))
                    if fev1_value < 0 or fev1_value > 200:
                        print("Please enter a realistic FEV1 percentage value (0-200).")
                        continue
                    break
                except ValueError:
                    print("Invalid input, please enter an integer.")
            print(f"You entered: {fev1_value}")
            obs_file = save_observation_json(patient_id, fev1_value)
            valid = validate_resource(obs_file)
            if valid:
                with open(obs_file, "r") as f:
                    observation = json.load(f)
                post_observation_to_hapi(observation)
            else:
                print(f"Observation for patient {patient_id} failed validation and was not posted.")


    obs_status = check_obs_na(patient_list)
    # Mapping the units
    ucum_map = {
        "week": "wk",
        "month": "mo"
    }

# Check night waking frequency; if missing, prompt and create observation.
    for patient_id in patient_list:
        if obs_status.get(patient_id, False) == False:
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
                        post_observation_to_hapi(observation) # If validated posting then to HAPI fhir
                    else:
                        print(f"Observation for patient {patient_id} failed validation and was not posted.")

                    break

                except ValueError:
                    print("Invalid input. Please enter a number for frequency.")
    patient_data = fetch_patient_data(patient_list)
    print(patient_data)

    # Treatment recommendation rules
    for patient_sets in patient_data:
        pid = patient_sets.get('patient_id')
        age = patient_sets.get('age')
        fev1_value = patient_sets.get('fev1_value')
        # Decision modelled from high to low severity (Recommendation for worst case scenario)
        if age >= 12 and fev1_value < 60:
            print(f"{pid}: Medication recommendation: Step 4 or 5")
        elif age in range(5, 12) and fev1_value < 60:
            print(f"{pid}: Medication recommendation: Step 3 or 4")
        elif age >= 12 and fev1_value in range(60, 81):
            print(f"{pid}: Medication recommendation: Step 3")
        elif age in range(5, 12) and fev1_value in range(60, 81):
            print(f"{pid}: Medication recommendation: Step 3 (Medium dose ICS option)")
        elif age >= 12 and fev1_value > 80:
            print(f"{pid}: Medication recommendation: Step 2")
        elif age in range(5, 12) and fev1_value > 80:
            print(f"{pid}: Medication recommendation: Step 2")


if __name__ == '__main__':
    eligibility_condition() # run this to fetch the last patient resource who is diagnosed with asthma
    rule_1() # Decision rules


