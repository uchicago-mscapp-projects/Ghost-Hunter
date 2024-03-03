import json
import requests
from utils import make_post
from search_parameters import POST_DATA, search_page_url, url_search_results_count
from search_parameters import PROVIDER_TYPES


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

