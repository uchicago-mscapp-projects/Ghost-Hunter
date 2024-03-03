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

def scrape_ccare(start_over=False):
    """
    Scrape's county care's provider directory. 
    """
    
    if start_over is True:
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
        POST_DATA["searchAddress"] = "".join([zip_code, ", IL"])

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
        

    def re_scrape():

        re_scrape = gen_re_scrape_list()
        for new_attempt in re_scrape:
            provider_type_select = new_attempt['providerTypeSelect']
            speciality_tup = ("speciality", SPECIALTIES_BY_CODE[provider_type_select])
            new_params = SECOND_SEARCH_PARAMS + [speciality_tup]
            recursive_re_scraper(new_attempt, new_params, POST_DATA)
     
    
def recursive_re_scraper(old_search, new_parameters, post_data, start_over=False):
    """
    This function takes a list of dictionaries for searches that need to be re-run
    and recursively re-runs those searches.
    """
    if start_over is True:
        re_scrape_results = {}
    else:
        with open("re_scrape_ccare.json") as f:
            re_scrape_results = json.load(f)

    next_search = new_parameters.pop()
    
    for query_type, value in old_search.items():
        post_data[query_type] = value
    
    new_query, new_values = next_search
    
    for value in new_values:
        old_search[new_query] = value
        post_data[new_query] = value
        dict_values_list = list(old_search.values())
        full_search = "+".join(dict_values_list)
        if full_search in re_scrape_results.keys():
            continue

        r = make_post(search_page_url, post_data)
        if len(r.text) <= 2:
            print("Empty")
        
        print(full_search)

        doc_list = r.json()
        doc_count = 0
        for doc in doc_list:
            if doc["locationZipCode"] == old_search['searchAddress'][0:5]:
                doc_count += 1
        
        if doc_count < 250 or len(new_parameters) == 0:
            
            re_scrape_results[full_search] = r.json()
            with open("re_scrape_ccare.json", "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)

        else:
            recursive_re_scraper(old_search, new_parameters, post_data)
        


def gen_re_scrape_list(file_path = "ccare_scrape.json"):
    """
    This function loops through the raw scrape results and checks which 
    provider code/ zip code combinations need to be re-scraped. 
    
    """

    with open("ccare_scrape.json") as f:
        fst_scrape = json.load(f)

    with open("cook_county_coordinates_zips.json") as d:
        address_params = json.load(d)

    re_scrape_list = []

    for zip_code, doc_dict in fst_scrape.items():
        for doc_code, doc_list in doc_dict.items():
            docs_in_zip = 0
            for doc in doc_list:
                if zip_code == doc["locationZipCode"]:
                    docs_in_zip += 1

            if docs_in_zip == 250:
                search_terms = {}
                search_terms["providerTypeSelect"] = doc_code
                search_terms["searchAddress"] = "".join([zip_code, ", IL"])
                search_terms["providerAddress"] = address_params[zip_code]
                re_scrape_list.append((search_terms))

    return re_scrape_list

