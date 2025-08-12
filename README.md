# CDSS for severity assessment and medication recommendation for ASTHMA
## Introduction:
The guideline is applicable only for the initial assessment and treatment recommendation for asthma  who are not on long 
term asthma therapy. Therefore, patients who's MedicalStatement resource does not include medication for asthma are 
excluded. Later we tried to access the observation records for predicted FEV1 score which is a lung function test, but 
none of the observations include predicted FEV1. Considering usability we created the observation for 
FEV1 by takin the input value from the user. Similarly, we also tried to model other parameters that will help in 
accessing usability and then added them to observation as well. 


## check if the patients with condition asthma
```python
url= f'{BASE_URL}/Condition?code:text=asthma&_sort=-_lastUpdated&_count=10'
```
## Get patient id's for patients with asthma condition and check for condition
```python
url= f'{BASE_URL}/MedicationStatement/?patient={id}'
```
## checking if patients are on medication (active) for asthma:
```python
if 'entry' not in data:
    print(f"Patient (Id:{id}) has no medication statements.")
```
```python
for coding in reason.get('coding', []):
    if 'asthma (disorder)' in coding.get('display', '').lower():
```
### Output
```
Patient (Id:22) has no medication statements.
patient (ID:48594309) is on asthma medication
```
## For patients who are not on medication, we checked if the patient has any entries under observation resource
```python
url = f'{BASE_URL}/Observation?patient={id}'
```
```python
if '20149-1' in patient_codes or '313223002' in patient_codes:
```
### Output
```
Patient (Id:48651908) has no observation.
https://hapi.fhir.org/baseR4/Observation?patient=48651906
Patient (Id:48651906) has no observation.
https://hapi.fhir.org/baseR4/Observation?patient=48649492
Patient with 48649492 do not have FEV1 observation
```
## we checked if the patient has Asthma causing night waking 

