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

def fetch_patient_data(patient_list):
    all_patient_data = []

    for patient_id in patient_list:
        # Fetch age
        url = f'{BASE_URL}/Patient/{patient_id}'
        response = requests.get(url)
        data = response.json()
        birth_date = datetime.strptime(data['birthDate'], "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        # Fetch observations
        url = f'{BASE_URL}/Observation?patient={patient_id}'
        response = requests.get(url)
        data = response.json()

        fev1_value = None
        night_awake_value = None
        night_awake_unit = None

        for entry in data.get('entry', []):
            resource = entry.get('resource', {})
            code_coding = resource.get('code', {}).get('coding', [{}])[0]
            code = code_coding.get('code')

            if code == '313223002':  # FEV1 percent predicted
                fev1_value = resource.get('valueQuantity', {}).get('value')
            elif code == '170632009':  # Asthma night waking
                night_awake_value = resource.get('valueQuantity', {}).get('value')
                night_awake_unit = resource.get('valueQuantity', {}).get('unit')

        patient_data = {
            "patient_id": patient_id,
            "age": age,
            "fev1_value": fev1_value,
            "night_awake_value": night_awake_value,
            "night_awake_unit": night_awake_unit
        }

        all_patient_data.append(patient_data)

    return all_patient_data
