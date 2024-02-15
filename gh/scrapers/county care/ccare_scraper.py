import json
import lxml
import requests
from utils import make_request, make_post

url = "https://countycare.valence.care/member/rest/findAProvider/search"


post_data = {"providerTypeSelect": "06",
 "providerName": "",
 "mileRadiusForSearch": "1",
 "mileRadius": "1",
 "gender": "",
 "network": "",
 "service": "",
 "speciality": "",
 "language": "",
 "specialNeeds": "",
 "handicapAccess" : "",
 "acceptNewPatient": "",
 "providerAddress": "41.80153,-87.60134",
 "hospitalAffiliation": "",
 "groupAffiliation": "",
 "groupAffiliationName": "",
 "providerFirstName": "",
 "providerLastName": "",
 "providerNumber": "",
 "providerCity": "",
 "providerState": "",
 "providerPhone": "",
 "lob": "",
 "policyBenefitId": "",
 "pcpOptions": "",
 "affiliationType": "",
 "errored": "",
 "searchAddress": "60615, IL",
 "patientAgeRangeSeen": "",
 "networkPriority": "",
 "accreditationTitle": "",
 "accreditationOrganization": "",
 "providerSelectOption": "LIKE",
 "acceptsBlindVisuallyImpairedPatients": "",
"acceptsHearingImpairedPatients": "",
"dualDemonstrationPopulationTraining": "",
"acceptsHivAidsPatients": "",
"acceptsHomelessPatients": "",
"provAffiliation_specialNeeds": "",
"acceptsChronicIllnessPatients": "",
"acceptsSeriousMentalIllnessPatients": "",
"acceptsPhysicalDisabilitiesPatients": "",
"acceptsCoOccuringDisordersPatients": "",
"open24By7": "",
"adjustableExamTable": "",
"handicapSupport": "",
"handicapParking": "",
"culturalCompetencyTraining":"",
"accessibleByPublicTransportation": "",
"translationServices": "",
"wheelchairAccessibleExamRoom":"" ,
"wheelchairAccessibleRestroom":"" ,
"wheelchairRamps":"" ,
"ttyService": "" ,
"transactionsExcludedInd": 'false'
}

url_search_results_count = "https://countycare.valence.care/member/rest/findAProvider/searchResultSize"

search_page_url = "https://countycare.valence.care/member/#findAProvider"

def scrape_ccare():
    """
    Runs make_request with ccare data. 
    """

    r = make_post(url, post_data)

    list = r.json()

    return list

