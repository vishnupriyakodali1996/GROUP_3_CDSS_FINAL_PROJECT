import requests
from pathlib import Path
import os
import json
from pprint import pprint
from datetime import datetime

BASE_URL = "https://hapi.fhir.org/baseR4"
hapi_url = BASE_URL

cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)

def search_condition():
    url= f'{BASE_URL}/Condition?code:text=asthma&_sort=-_lastUpdated&_count=2'
    response = requests.get(url=url)
    data = response.json()
    patient_list=[]
    for patients in data['entry']:
        id= patients['resource']['subject']['reference'].split('/')[-1]
        patient_list.append(id)
    file_path = data_dir / "patient_list.txt"
    with open(file_path, "w") as f:
        for pid in patient_list:
            f.write(pid + "\n")
    for id in patient_list:
        url = f'{BASE_URL}/Patient/{id}'
        response= requests.get(url)
        data= response.json()

def check_med(patient_list):
    med_status = {}
    for id in patient_list:
        url= f'{BASE_URL}/MedicationStatement/?patient={id}'
        response = requests.get(url)
        data = response.json()
        if 'entry' not in data:
            print(f"Patient (Id:{id}) has no medication statements.")
            med_status[id] = False
        else:
            medication= 0
            for entry in data['entry']:
                med = entry['resource']
                reason_codes = med.get('reasonCode', [])
                for reason in reason_codes:
                    for coding in reason.get('coding', []):
                        if 'asthma (disorder)' in coding.get('display', '').lower():
                            medication += 1
            if medication >= 1:
                print(f"patient (ID:{id}) is on asthma medication")
                med_status[id] = True
            else:
                print(f"patient (ID:{id}) is not on asthma medication")
                med_status[id] = False
    return med_status

def check_obs(patient_list):
    obs_status = {}
    for id in patient_list:
        url = f'{BASE_URL}/Observation?patient={id}'
        response = requests.get(url=url)
        data = response.json()
        patient_codes = []
        if 'entry' not in data:
            print(f"Patient (Id:{id}) has no observation.")
            obs_status[id] = False
        else:
            for entry in data.get('entry', []):
                for coding in entry['resource']['code']['coding']:
                    observation_code = coding.get('code')
                    patient_codes.append(observation_code)
            if '20149-1' in patient_codes or '313223002' in patient_codes:
                print(f"Patient with {id} has FEV1 observation")
                obs_status[id] = True
            else:
                print(f"Patient with {id} do not have FEV1 observation")
                obs_status[id] = False
    return obs_status

def save_observation_json(patient_id, fev1_value):
    observation = {
        "resourceType": "Observation",
        "id": f"fev1-measurement-{patient_id}",
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/Observation"]
        },
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "procedure",
                "display": "Procedure"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "313223002",
                "display": "Percent predicted forced expired volume in one second"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "valueQuantity": {
            "value": fev1_value,
            "unit": "%",
            "system": "http://unitsofmeasure.org",
            "code": "%"
        }
    }
    file_path = data_dir / f"observation_{patient_id}.json"
    with open(file_path, "w") as f:
        json.dump(observation, f, indent=2)
    print(f"Observation saved to {file_path}")
    return file_path

def validate_resource(file_path, resource_type="Observation"):
    with open(file_path, "r") as f:
        resource = json.load(f)
    response = requests.post(
        f"{hapi_url}/{resource_type}/$validate",
        headers={"Content-Type": "application/fhir+json"},
        json=resource
    )
    print(f"Validation response status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200  # return True if valid

def post_observation_to_hapi(observation):
    url = f"{BASE_URL}/Observation"
    headers = {"Content-Type": "application/fhir+json"}

    try:
        response = requests.post(url, headers=headers, json=observation)
        response.raise_for_status()
        print("Observation posted successfully.")
        pprint(response.json())
    except Exception as e:
        print(f"Error posting observation: {e}")
        if response is not None:
            print(response.text)

def rule_1():
    file_path = data_dir / "patient_list.txt"
    patient_list = []
    with open(file_path, "r") as file:
        for line in file:
            patient_id = line.strip()
            if patient_id:
                patient_list.append(patient_id)
    med_status = check_med(patient_list)
    obs_status = check_obs(patient_list)
    for patient_id in patient_list:
        if med_status.get(patient_id, False) == False and obs_status.get(patient_id, False) == False:
            while True:
                try:
                    fev1_value = int(input(f"Reminder for patient {patient_id}:\nEnter FEV1 predicted percentage from following values (integer only): "))
                    if fev1_value < 0 or fev1_value > 200:  # basic sanity check
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


def check():
    url = f'{BASE_URL}/Observation?patient=48651906'
    response = requests.get(url=url)
    data = response.json()
    pprint(data)


if __name__ == '__main__':
    # search_condition()
    # rule_1()
    check()
