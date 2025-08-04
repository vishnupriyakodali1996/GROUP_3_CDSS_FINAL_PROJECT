import requests
import json
from pprint import pprint

# Setting base URL of a public FHIR resource (HAPI FHIR)
BASE_URL = "https://hapi.fhir.org/baseR4"

def search_patient():
    # Constructing the URL
    url = f'{BASE_URL}/Condition?code=44054006'
    # Sending GET request
    response = requests.get(url=url)
    # Checking if response is successful
    if response.status_code == 200:
        data = response.json()
        pprint(data)
    else:
        print(f"Request failed with status code: {response.status_code}")

if __name__ == '__main__':
    # Calling search patient()
    search_patient()
