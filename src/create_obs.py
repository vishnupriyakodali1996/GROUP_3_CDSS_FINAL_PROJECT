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

def save_observation_json_2(patient_id, frequency, unit_code):
    observation = {
        "resourceType": "Observation",
        "id": f"asthma-causing-night-waking-{patient_id}",
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/Observation"]
        },
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "exam",
                "display": "Exam"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": "170632009",
                "display": "Asthma causing night waking"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "valueQuantity": {
            "value": frequency,
            "unit": unit_code,
            "system": "http://unitsofmeasure.org",
            "code": unit_code
        }
    }
    file_path = data_dir / f"observation_na_{patient_id}.json"
    with open(file_path, "w") as f:
        json.dump(observation, f, indent=2)
    print(f"Observation saved to {file_path}")
    return file_path