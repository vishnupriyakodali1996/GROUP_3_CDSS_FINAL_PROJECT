import requests
from pathlib import Path
import os
import json
from pprint import pprint
from datetime import datetime

BASE_URL = "https://hapi.fhir.org/baseR4"


cwd = Path(os.getcwd())
data_dir = cwd / "data"
data_dir.mkdir(exist_ok=True)

def post_observation_to_hapi(observation):
    url = f"{BASE_URL}/Observation"
    headers = {"Content-Type": "application/fhir+json"}

    try:
        response = requests.post(url, headers=headers, json=observation)
        response.raise_for_status()
        print("Observation posted successfully.")
        #pprint(response.json())# uncomment it only if intended to view in the output
    except Exception as e:
        print(f"Error posting observation: {e}")
        if response is not None:
            print(response.text)