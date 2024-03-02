import json
import requests
from utils import make_request, make_post

POST_DATA = {"providerTypeSelect": "",
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

# codes that need more:  {'04', '06', '08', '10'}
PROVIDER_TYPES = {'Primary Care Doctors/Nurses': 'PCP',
'Transportation': '01',
'Hospitals': '02',
'Surgery': '04',
'Behavioral Health Providers & Specialists': '06',
'Medical Specialists': '08',
'Hearing Services': '09',
'Physical, Occupational and Speech Therapy': '10',
'Durable Medical Equipment Suppliers': '11',
'Other Facilities': '13',
'Home Health': '14',
'Long Term Care Facilities & Nursing Homes': '15',
'Dialysis Centers': '17',
'Pharmacy': '18',
'Primary Care Facilities': '19',
"Lab and Imaging": '38',
'Supportive Living Facilities': '32',
'Urgent Care': '39'}

url_search_results_count = "https://countycare.valence.care/member/rest/findAProvider/searchResultSize"

search_page_url = "https://countycare.valence.care/member/rest/findAProvider/search"

def scrape_ccare(re_scrape = False):
    """
    Scrape's county care's provider directory. 
    """
    
    if re_scrape is True:
        ccare_scrape = {}
    else:
        with open("ccare_scrape.json") as d:
            ccare_scrape = json.load(d)

    with open("cook_county_coordinates_zips.json") as f:
        address_params = json.load(f)
    
    provider_codes = list(PROVIDER_TYPES.values()) 
    
    POST_DATA["mileRadiusForSearch"] = 10
    POST_DATA["mileRadius"] = 10

    for zip_code, coord in address_params.items():
        if zip_code not in ccare_scrape.keys():
            ccare_scrape[zip_code] = {}
        
        POST_DATA["providerAddress"] = coord
        POST_DATA["searchAddress"] = zip_code + ", IL"

        for doc_code in provider_codes:
            
            if doc_code in ccare_scrape[zip_code]:
                continue

            print(zip_code, doc_code)
            
            POST_DATA["providerTypeSelect"] = doc_code
            r = make_post(search_page_url, POST_DATA)
            if len(r.text) <= 2:
                print("Empty")
            
            scrape_data = r.json()

            ccare_scrape[zip_code][doc_code] = scrape_data

            with open("ccare_scrape.json", "w") as f:
                json.dump(ccare_scrape, f, indent=4, sort_keys=True)


def scrape_unpacker(file_path = "ccare_scrape.json"):
    """
    This unpacks the scrape results and returns two items:
    1) A set of all unique providers.
    2) A list of the zip codes where the scraper reached the limit, and there
    could be doctors left.
    3) A dictionary of the list of blanks by doctor code.
    
    """

    with open("ccare_scrape.json") as f:
        ccare_scrape = f.read()
    fst_scrape = json.loads(ccare_scrape)
    provider_set = set()
    too_many_docs = []
    code_use_count = {}

    for zip_code, doc_dict in fst_scrape.items():
        for doc_code, doc_list in doc_dict.items():
            docs_in_zip = 0

            if len(doc_list) == 0:
                code_use_count[doc_code] = 1 + code_use_count.get(doc_code, 0)
            
            for doc in doc_list:
                identifier = str(doc["locationId"]) + str(doc["providerId"]) + doc["providerNo"]
                provider_set.add(identifier)
                
                if zip_code == doc["locationZipCode"]:
                    docs_in_zip += 1

            if docs_in_zip == 250:
                too_many_docs.append((zip_code, doc_code))
    
    return provider_set, too_many_docs, code_use_count

def scrape_test_provider_id():
    """
    This function tests all numbers from "01" to "100" see which was are used as codes 
    for provider types. If the post request recieves data it appends the data to a dictionary
    which is later returned.
    """
    POST_DATA["providerTypeSelect"] = "01"
    POST_DATA["mileRadiusForSearch"] = 5
    POST_DATA["mileRadius"] = 5
    scrape_dict = {}
    provider_type = 1
    for _ in range(100):
        provider_type = str(provider_type)
        if len(provider_type) == 1:
            sep = ""
            provider_type = sep.join(["0", provider_type])
        
        POST_DATA["providerTypeSelect"] = provider_type        
        r = make_post(url_search_results_count, POST_DATA)
        key = POST_DATA["providerTypeSelect"]
        provider_type = str(int(key) + 1)

        
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

