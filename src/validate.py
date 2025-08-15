import requests
from pathlib import Path
import os
import json
from pprint import pprint
from datetime import datetime

hapi_url = "https://hapi.fhir.org/baseR4"

cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)

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