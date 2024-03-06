import json
from .utils import make_post
from .search_parameters import POST_DATA, search_page_url, url_search_results_count
from .search_parameters import *
import pathlib

pathlib.Path(_file_).parent / "data/selected_columns.csv"
#ccare_scrape.json 

def scrape_ccare(start_over=False):
    """
    This function runs the first scrape of county care's "Find a Provider" page.
    It iterates through all combinations of all the zip codes in Cook County and the 18
    "Provider Types" that County Care uses as their first level filter and makes a post
    To see a list of provider types go to search_parameters.py.
    Inputs:
    statrt_over(bool): A boolean parameter that specifies if the scrape should
    start from an empty dictionary, as opposed to building on an existing file.
    """
    
    #This would start from an empty dictionary
    if start_over is True:
        ccare_scrape = {}
    else:
    # This loads the file which stores all data from the last scrape into a dictionay.
    # ccare_scrape is a dictionary of dictionaries. The first nested layer corresponds
    # to the zip codes used on the search. The second nested layer corresponds to the
    # provider type code used.
        with open("gh/scrapers/county_care/ccare_scrape.json") as d:
            ccare_scrape = json.load(d)

    # address_params is a dictionary of zip-code, lat-long pairs. The lat-long
    # coordinates are the centroids of the zip-codes and they are pulled from 
    # a google maps API. The lat-long coordinates are needed to make a post
    # to the county care website.
    with open("gh/scrapers/county_care/cook_county_coordinates_zips.json") as f:
        address_params = json.load(f)
    
    # Converts the dictionary of provider types into a list.
    provider_codes = list(PROVIDER_TYPES.values()) 
    
    # Each search will cover all provider within 10 miles of the provided centroid.
    POST_DATA["mileRadiusForSearch"] = 10
    POST_DATA["mileRadius"] = 10

    #Iteratting first over zip code and lat-long pairs.
    for zip_code, coord in address_params.items():
        
        # If the zip_code is not a key in the dictionary loaded at the outset,
        # then we creat an empty entry.
        if zip_code not in ccare_scrape.keys():
            ccare_scrape[zip_code] = {}
        
        # Here we update our post_data with the lat long coordinates and the
        # zip code of the search.
        POST_DATA["providerAddress"] = coord
        POST_DATA["searchAddress"] = "".join([zip_code, ", IL"])

        # Now we iterate throught provider type codes.
        for doc_code in provider_codes:
            # If a search has been run with the provider code and the zip_code
            # parameters, we skip this search.
            if doc_code in ccare_scrape[zip_code]:
                continue
            
            # This print statement lets us know which query our scraper is executing
            # at a given moment.
            print(zip_code, doc_code)
            
            # update the post_data to the provider code
            POST_DATA["providerTypeSelect"] = doc_code
            
            # make the post to the provider type search.
            r = make_post(search_page_url, POST_DATA)
            
            # remove
            if len(r.text) <= 2:
                print("Empty")
            
            # Our response is always in json format. Specifically as a list 
            # of dictionaries. This command saves it into a variable.
            scrape_data = r.json()

            # Now we update our double dictionary of all executed searches 
            # to include the results from this one search.
            ccare_scrape[zip_code][doc_code] = scrape_data

            # After updating the dictionary we always save our data locally so that
            # we still have data even if the scraper stops.
            with open("gh/scrapers/county_care/ccare_scrape.json", "w") as f:
                json.dump(ccare_scrape, f, indent=4, sort_keys=True)
        

def re_scrape(re_re_do=False):
    """
    This function re-runs the searches where we got more than 250
    search results in the corresponding zip code. Those zip-codes have hit
    county cares 250 result limit. This function then adds filter to those 
    searches and re-runs them.
    Inputs:
    re_re_do(Boolean): If set to true we will re-scrape starting with an empty
    dictionary instead of building on one that is saved. This will write over any
    previous second round scrapes. 
    """
    
    POST_DATA['mileRadiusForSearch'] = 10
    POST_DATA['mileRadius'] = 10
    re_scrape = gen_re_scrape_list()
    
    if re_re_do is True:
        re_scrape_results = {}
        with open("re_scrape_ccare.json", "w") as f:
            json.dump(re_scrape_results, f, indent=4, sort_keys=True)
    
    for new_attempt in re_scrape:

        filter_iteration(new_attempt)


def filter_iteration(old_search):
    """
    Iteratively tries two more sets of filters on a given search.
    """
    # Before running any additional queries we make sure our second query filters
    # are blank. Unlike previous filters, these do not need to be present for a search
    # and failing to re-set them can cause values to carry over betweeen queries.
    POST_DATA['gender'] = ""
    POST_DATA['speciality'] = ""

    # This loads all previous searches into a dictionary that we will update after
    # every post request.
    with open("re_scrape_ccare.json") as f:
        re_scrape_results = json.load(f)
    
    # Set the base post-request to replicate the query that we are iterating on.
    for query_type, value in old_search.items():
        POST_DATA[query_type] = value
    
    # Our first added filter is gender. This creates a variable for the query
    # and for each potential value we could use to query.
    gender_query, gender_values = SECOND_SEARCH_PARAMS

    # We iterate over each value in sex (just "M" and "F")
    for sex in gender_values:
        POST_DATA[gender_query] = sex

        # This updates the dictionary of search terms to include gender
        # and converts all keys into a string that will be the key to our final
        # dictionary of results.
        new_search = old_search.copy()
        new_search[gender_query] = sex
        dict_values_list = list(new_search.values())
        full_search = "+".join(dict_values_list)
    
        # We will only re-run the post, if there is no key in our saved dictionary
        # that indicates the post has not been run before.
        if full_search not in re_scrape_results.keys():

            # This lets the viewer know which query is being executed.
            print(full_search)
            r = make_post(search_page_url, POST_DATA)

            # Our output is always in json format.
            doc_list = r.json()
        else:
            doc_list = re_scrape_results[full_search]

        # We leave empty lists when the first search returns 250 values
        # in the same zip code. If the the length of the list is 0, that means
        # that on a previous scrape, the count of doctors in that zip code reached
        # 250, which is the maximum number of returned results.
        if len(doc_list) > 0:
            doc_count = 0
            # We want to know how many providers found in this zip code
            # work in this zip code. If this number is 250, which is the 
            # maximum number of search results, then we know there could
            # be additional providers that our search isn't capturing. 
            # In that case we need to add new search parameters and re-do the search.

            for doc in doc_list:
                if doc["locationZipCode"] == new_search['searchAddress'][0:5]:
                    doc_count += 1
            # Inform the viewer how many doctors that search found.
            print(doc_count)
        else: 
            doc_count = 250

        if doc_count < 250:
            re_scrape_results[full_search] = doc_list
            with open("re_scrape_ccare.json", "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)
        
        else:
            re_scrape_results[full_search] = []
            with open("re_scrape_ccare.json", "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)            
            
            print("Applying specialities filters")
            re_scrape_results[full_search] = []
            specialties_list = SPECIALTIES_BY_CODE[old_search['providerTypeSelect']]

            for s in specialties_list:
                POST_DATA['speciality'] = s

                new_search['spciality'] = s
                dict_values_list = list(new_search.values())
                full_search = "+".join(dict_values_list)
                
                if full_search in re_scrape_results.keys():
                    continue
                
                print(full_search)
                r = make_post(search_page_url, POST_DATA)
                re_scrape_results[full_search] = r.json()
                with open("re_scrape_ccare.json", "w") as f:
                    json.dump(re_scrape_results, f, indent=4, sort_keys=True)
        
        POST_DATA['gender'] = ""
        POST_DATA['speciality'] = ""


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

