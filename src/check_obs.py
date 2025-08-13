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

def check_obs_na(patient_list):
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
            if "170632009" in patient_codes:
                print(f"Patient with {id} has night time awakening observation")
                obs_status[id] = True
            else:
                print(f"Patient with {id} do not have night time awakening observation")
                obs_status[id] = False
    return obs_status
