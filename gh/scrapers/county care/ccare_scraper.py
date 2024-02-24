import json
import lxml
import requests
from utils import make_request, make_post

post_data = {"providerTypeSelect": "",
 "providerName": "",
 "mileRadiusForSearch": "5",
 "mileRadius": "5",
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

search_page_url = "https://countycare.valence.care/member/rest/findAProvider/search"

def scrape_ccare(re_scrape = False, use_provider_codes = True):
    """
    Scrape's county care's provider directory. 
    """
    
    if re_scrape is True:
        ccare_scrape = {}
    else:
        with open("ccare_scrape.json", "w") as d:
            ccare_scrape = json.load(d)

    with open("cook_county_coordinates_zips.json") as f:
        address_params = json.load(f)

    if use_provider_codes is True:
        provider_codes = gen_provider_types_dict()
        provider_codes = list(provider_codes.values())
    else:
        provider_codes = []
        for num in range(25):
            code = str(num + 1)
            if len(code) < 2:
                code = "0" + code
            provider_codes.append(code)
    
    post_data["mileRadiusForSearch"] = 10
    post_data["mileRadius"] = 10

    for zip_code, coord in address_params.items():
        if zip_code not in ccare_scrape.keys():
            ccare_scrape[zip_code] = {}
        
        post_data["providerAddress"] = coord
        post_data["searchAddress"] = zip_code + ", IL"

        for doc_code in provider_codes:
            
            if doc_code in ccare_scrape[zip_code]:
                continue

            print(zip_code, doc_code)
            
            post_data["providerTypeSelect"] = doc_code
            r = make_post(search_page_url, post_data)
            if len(r.text) <= 2:
                print("Empty")
            
            scrape_data = r.json()

            ccare_scrape[zip_code][doc_code] = scrape_data

            with open("ccare_scrape.json", "w") as f:
                json.dump(ccare_scrape, f, indent=4, sort_keys=True)




def scrape_test_provider_id(blanks):
    """
    This function tests all numbers after "01" to see which was are used as codes 
    for provider types. If the post request recieves data it appends the data to a dictionary
    which is later returned. 
    """

    post_data["providerTypeSelect"] = "01"
    post_data["mileRadiusForSearch"] = 50
    post_data["mileRadius"] = 50
    scrape_dict = {}
    misses = 0
    while misses < blanks:
        r = make_post(search_page_url, post_data)
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
    

def gen_provider_types_dict(incon = False):
    """
    This function checks the scraped dictionaries to make sure provider type is consistently used.
    It returns a dictionary that maps numbers onto provider types to use when scraping and a count of any potential
    inconsistencies.
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
    if incon is True:
        return p_types_dict, inconsistencies
    
    return p_types_dict