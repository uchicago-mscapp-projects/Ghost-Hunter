import json
import lxml
import requests
from utils import make_request, make_post

url = "https://countycare.valence.care/member/rest/findAProvider/search"


post_data = {"providerTypeSelect": "",
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

provider_types = {'Transportation': '01',
 'Hospitals': '02',
 'Surgery': '04',
 'Behavioral Health Providers & Specialists': '06',
 'Medical Specialists': '08',
 'Hearing Services': '09',
 'Physical, Occupational and Speech Therapy': '10',
 'Durable Medical Equipment Suppliers': '11',
 'Other Facilities': '13',
 'Long Term Care Facilities & Nursing Homes': '15',
 'Dialysis Centers': '17',
 'Pharmacy': '18',
 'Primary Care Facilities': '19'}

url_search_results_count = "https://countycare.valence.care/member/rest/findAProvider/searchResultSize"

search_page_url = "https://countycare.valence.care/member/rest/findAProvider/search"

def scrape_ccare():
    """
    Runs make_request with ccare data. 
    """

    r = make_post(url, post_data)

    list = r.json()

    return list


def scrape_test_provider_id(blanks):
    post_data["providerTypeSelect"] = "01"
    scrape_dict = {}
    misses = 0
    while misses < blanks:
        r = make_post(url, post_data)
        key = post_data["providerTypeSelect"]
        provider_type = str(int(key) + 1)
        if len(provider_type) == 1:
            provider_type = "0" + provider_type
        post_data["providerTypeSelect"] = provider_type
        
        if len(r.text) <= 2:
            misses += 1
            print("Miss number", misses)
        else:
            dicts = r.json()
            scrape_dict[key] = dicts

        print(provider_type)
    with open("provider_scrape_test.json", "w") as f:
        json.dump(scrape_dict, f, indent=4, sort_keys=True)
    

def gen_provider_types_dict():
    """
    This function checks the scraped dictionaries to make sure provider type is consistently used.
    """
    with open("provider_scrape_test.json") as f:
        scrape_lists = json.load(f)
    inconsistencies = []
    p_types_dict = {}
    for key, vals in scrape_lists.items():
        ptype = vals[0]["providerType"]
        for val in vals:
            if ptype == val["providerType"]:
                continue
            else:
                print("inconsistency at", key)
                inconsistencies.append(key)
                break
        if key not in inconsistencies:
            p_types_dict[ptype] = key
    
    return p_types_dict, inconsistencies