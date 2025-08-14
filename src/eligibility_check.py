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


BASE_URL = "https://hapi.fhir.org/baseR4"


cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)

# Fetch last updated patient resource who has asthma
import requests
from pathlib import Path
import os
from datetime import datetime

BASE_URL = "https://hapi.fhir.org/baseR4"

cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)

def eligibility_condition():
    # Fetch last updated patients with asthma
    url = f'{BASE_URL}/Condition?code:text=asthma&_sort=-_lastUpdated&_count=1'
    response = requests.get(url)
    data = response.json()

    # Step 1: Create a list of patients who have asthma
    asthma_patient_list = []
    for patient_entry in data.get('entry', []):
        patient_id = patient_entry['resource']['subject']['reference'].split('/')[-1]
        asthma_patient_list.append(patient_id)

    # Step 2: Check which patients are NOT on asthma medication
    patients_no_med = []
    for patient_id in asthma_patient_list:
        med_url = f'{BASE_URL}/MedicationStatement/?patient={patient_id}'
        med_response = requests.get(med_url)
        med_data = med_response.json()

        if 'entry' not in med_data:
            patients_no_med.append(patient_id)
            print(f"Patient (ID:{patient_id}) has no medication statements.")
        else:
            on_med = False
            for entry in med_data['entry']:
                med = entry['resource']
                reason_codes = med.get('reasonCode', [])
                for reason in reason_codes:
                    for coding in reason.get('coding', []):
                        if 'asthma (disorder)' in coding.get('display', '').lower():
                            on_med = True
            if not on_med:
                patients_no_med.append(patient_id)
                print(f"Patient (ID:{patient_id}) is not on asthma medication.")
            else:
                print(f"Patient (ID:{patient_id}) is on asthma medication.")

    # Step 3: Filter patients by age > 4
    eligible_patients = []
    for patient_id in patients_no_med:
        url = f'{BASE_URL}/Patient/{patient_id}'
        response = requests.get(url)
        patient_data = response.json()

        birth_date_str = patient_data.get('birthDate')
        if not birth_date_str:
            print(f"Patient {patient_id} has no birthDate")
            continue  # skip this patient if no birthdate is present

        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        except ValueError:
            print(f"Patient {patient_id} has invalid birthDate format: {birth_date_str}. Skipping.")
            continue

        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print(f"Patient {patient_id} age: {age}")

        if age > 4:
            eligible_patients.append(patient_id)

    # Step 4: Save eligible patient IDs to file in data directory
    file_path = data_dir / "patient_list.txt"
    with open(file_path, "w") as f:
        for pid in eligible_patients:
            f.write(pid + "\n")
    print(f"Eligible patient IDs saved to {file_path}")

    return eligible_patients



if __name__ == '__main__':
    eligibility_condition()