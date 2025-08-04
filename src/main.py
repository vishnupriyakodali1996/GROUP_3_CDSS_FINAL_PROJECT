import requests
import json
from pprint import pprint

# Setting base URL of a public FHIR resource (HAPI FHIR)
BASE_URL = "https://hapi.fhir.org/baseR4"

def search_patient():
    # Constructing the URL
    url = f'{BASE_URL}/Patient'
    # Sending GET request
    response = requests.get(url=url)
    # Checking if response is successful
    if response.status_code == 200:
        data = response.json()
        pprint(data)
    else:
        print(f"Request failed with status code: {response.status_code}")

def search_patient_by_id(resource_id):
    url = f'{BASE_URL}/Patient/{resource_id}'
    response = requests.get(url=url)
    print(response.url)
    data = response.json()
    pprint(data)

if __name__ == '__main__':
    # Calling search patient()
    #search_patient()
    search_patient_by_id(resource_id=44842203)
