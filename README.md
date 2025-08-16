# A Guideline-Based CDSS for Classifying Asthma Severity and Initial Therapy Recommendation
## Introduction:
This script implements a Clinical Decision Support System (CDSS) designed to provide severity grading and initial therapy 
recommendations for asthma patients who are not currently on long-term asthma medication and are over 4 years of age. 
The recommendations are based on clinical guidelines published by the National Heart, Lung, and Blood Institute, 
as reported by the National Asthma Education and Prevention Program Coordinating Committee Expert Panel Working Group [^1],[^8].

The guidelines list multiple factors for assessing asthma severity and guiding treatment, including symptoms, asthma 
exacerbations requiring oral systemic corticosteroids, and interference with normal activity [^1],[^8]. For this implementation, 
parameters with corresponding SNOMED codes and those that can be incorporated into declarative logic were selected. 
These include nighttime awakening frequency due to asthma and FEV1 predicted percentage[^1],[^8].

User input is also taken into consideration when generating recommendations. The primary decision-making logic is 
implemented in the cdss_decision_logic.py file. The required patient data is obtained public FHIR server (HAPI server)
using http methods and then substituted in the logic [^2]. Additionally, user input was taken where required.

## Steps to implement the cdss:
### System Requirements
- Python version 3 and above
- PyCharm (or any Python IDE)
- GitHub for repository management
### clone the git repository:
> git clone https://github.iu.edu/vkodali/GROUP_3_CDSS_FINAL_PROJECT.git
or 
* Use pycharm: File -> New -> Project from Version Control-> copy repo link

## Implementing CDSS: 
* Libraries to Install:
```bash
pip install requests
```
* Navigate to the cdss_decision_logic.py file in src package and run the file to see execution of 
decision logic output will have the CDSS reminder and will take the user input for modelling final recommendation.


## Files Description:
### data/ directory: Contains JSON templates:
* observation_template.json - sample observation template copied from FHIR website [^7].
### patient_list.txt: 
* Holds the IDs of eligible patients.
### eligibility.py:
* Checks the latest patient records in the HAPI FHIR server for asthma. 
* Verifies if the patient has any medication records.
* Confirms the patient’s age is above 4 years.
* Returns a list of eligible patient IDs.
### check_obs.py:
* Has functions to check if the observation records of the patient include observations for the FEV1 predicted percentage
and the frequency of nighttime awakening. 
### create_obs.py:
* Has functions to create the observations with the user input for FEV! percentage and nighttime awakening frequency due 
to asthma modelled referring to FHIR specification, SNOMED international browser [^2], [^3], [^4], [^5], [^6], [^7].
### validate.py
* Has functions to validate the observation created
### post_obs.py
* Has functions to post the observation to HAPI FHIR server
### Fetch_pt_data
* Has functions to fetch patient's data needed for decision logic (age, fev1 value, Night time awakening frequency
, Night time awakening unit along with the patient ID)
### cdss_decision_logic.py:
* Imports all the required functions and libraries other python files runs them sequentially rule_1() which has the 
decision logic and recommendations.
### medication.py:
* Has function with medication mappings for age and severity

## References:
[^1]: National Heart, Lung, and Blood Institute. (2012). _Asthma care quick reference: Diagnosing and managing asthma_. 
National Institutes of Health. https://www.nhlbi.nih.gov/sites/default/files/publications/12-5075.pdf
[^2]: HAPI FHIR. (n.d.). _HAPI FHIR Test/Demo Server R4 Endpoint_. Retrieved August 15, 2025, 
from https://hapi.fhir.org/baseR4/swagger-ui/
[^3]: Health Level Seven International. (n.d.). _Observation - FHIR v6.0.0-ballot2_. Retrieved August 15, 2025, 
from https://build.fhir.org/observation.html
[^4]: Health Level Seven International. (n.d.). _Observation interpretation value set - FHIR v6.0.0-ballot2_. Retrieved 
August 15, 2025, from https://build.fhir.org/valueset-observation-interpretation.html
[^5]: Health Level Seven International. (n.d.). _Observation category value set - FHIR v6.0.0-ballot2_. Retrieved 
August 15, 2025, from https://build.fhir.org/valueset-observation-category.html
[^6]: International Health Terminology Standards Development Organisation. (n.d.). _SNOMED CT Browser_.
Retrieved August 15, 2025, from https://browser.ihtsdotools.org/?perspective=full&conceptId1=404684003&edition=MAIN/2025-08-01&release=&languages=en
[^7]: Health Level Seven International. (n.d.). _Observation/example.json - FHIR v6.0.0-ballot2_. Retrieved 
August 15, 2025, from https://build.fhir.org/observation-example.json.html
[^8]: National Heart, Lung, and Blood Institute. (2007). _Expert Panel Report 3: Guidelines for the diagnosis and 
management of asthma - Full report 2007_. National Institutes of Health. https://www.nhlbi.nih.gov/sites/default/files/media/docs/EPR-3_Asthma_Full_Report_2007.pdf