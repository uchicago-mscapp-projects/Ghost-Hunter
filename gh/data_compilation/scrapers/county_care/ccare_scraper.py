import json
import pathlib
from .utils import ccare_post
from .search_parameters.search_parameters import (
    PROVIDER_TYPES,
    SECOND_SEARCH_PARAMS,
    SPECIALTIES_BY_CODE,
)


def scrape_ccare(start_over=False, monitoring=True):
    """
    This function runs the first scrape of county care's "Find a Provider" page.
    It iterates through all combinations of all the zip codes in Cook County and the 18
    "Provider Types" that County Care uses as their first level filter and makes a post
    To see a list of provider types go to search_parameters.py.
    Inputs:
    statrt_over(bool): A boolean parameter that specifies if the scrape should
    start from an empty dictionary, as opposed to building on an existing file.
    Returns:
    None. This file saves all output to "scraped_data/ccare_scrape.json."
    """
    first_scrape_file = pathlib.Path(__file__).parent / "scraped_data/ccare_scrape.json"
    coordinates_file = (
        pathlib.Path(__file__).parent
        / "search_parameters/cook_county_coordinates_zips.json"
    )

    # This would start from an empty dictionary
    if start_over is True:
        ccare_scrape = {}

    else:
        # This loads the file which stores all data from the last scrape into a dictionay.
        # ccare_scrape is a dictionary of dictionaries. The first nested layer corresponds
        # to the zip codes used on the search. The second nested layer corresponds to the
        # provider type code used.
        with open(first_scrape_file) as d:
            ccare_scrape = json.load(d)

    # address_params is a dictionary of zip-code, lat-long pairs. The lat-long
    # coordinates are the centroids of the zip-codes and they are pulled from
    # a google maps API. The lat-long coordinates are needed to make a post
    # to the county care website.
    with open(coordinates_file) as f:
        address_params = json.load(f)

    # Converts the dictionary of provider types into a list.
    provider_codes = list(PROVIDER_TYPES.keys())

    # Initialize our default search parameters for the first round scrape.
    doctor_search = {"mileRadiusForSearch": "10", "mileRadius": "10"}

    # Iteratting first over zip code and lat-long pairs.
    for zip_code, coord in address_params.items():

        # If the zip_code is not a key in the dictionary loaded at the outset,
        # then we creat an empty entry.
        if zip_code not in ccare_scrape.keys():
            ccare_scrape[zip_code] = {}

        # Here we update our post_data with the lat long coordinates and the
        # zip code of the search.
        doctor_search["providerAddress"] = coord
        doctor_search["searchAddress"] = "".join([zip_code, ", IL"])

        # Now we iterate throught provider type codes.
        for doc_code in provider_codes:
            # If a search has been run with the provider code and the zip_code
            # parameters, we skip this search.
            if doc_code in ccare_scrape[zip_code]:
                continue

            # update the post_data to the provider code
            doctor_search["providerTypeSelect"] = doc_code

            # make the post to the provider type search. The default return value for
            # ccare_post is json, specifically a list of dictionaries. Each
            # dictionary corresponds to a search result.
            scrape_data = ccare_post(doctor_search, monitoring=monitoring)

            # Now we update our double dictionary of all executed searches
            # to include the results from this one search.
            ccare_scrape[zip_code][doc_code] = scrape_data

            # After updating the dictionary we always save our data locally so that
            # we still have data even if the scraper stops.
            with open(first_scrape_file, "w") as f:
                json.dump(ccare_scrape, f, indent=4, sort_keys=True)


def re_scrape(re_re_do=False, monitoring=True):
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
    scnd_scrape_file = (
        pathlib.Path(__file__).parent / "scraped_data/re_scrape_ccare.json"
    )

    # We gather the list of searches that hit "packed" zipcodes.
    re_scrape_list = gen_re_scrape_list()

    # If we want to re-scrape from the beginning we start by setting
    # the dictionary that stores our results to be empty and wiping the data
    # from our last re-scrape.
    if re_re_do is True:
        re_scrape_results = {}
        with open(scnd_scrape_file, "w") as f:
            json.dump(re_scrape_results, f, indent=4, sort_keys=True)

    for new_attempt in re_scrape_list:
        # For each entry in our re-scrape list we iteratively use our
        # remaining filters to squeeze out more data.
        # This process is defined in filter_iteration.
        filter_iteration(new_attempt, monitoring=monitoring)


def filter_iteration(old_search, monitoring=True):
    """
    Iteratively tries two more sets of filters on a given search.
    """
    new_search = old_search.copy()

    scnd_scrape_file = (
        pathlib.Path(__file__).parent / "scraped_data/re_scrape_ccare.json"
    )
    # This loads all previous searches into a dictionary that we will update after
    # every post request.
    with open(scnd_scrape_file) as f:
        re_scrape_results = json.load(f)

    # Our first added filter is gender. This creates a variable for the query
    # and for each potential value we could use to query.
    gender_query, gender_values = SECOND_SEARCH_PARAMS

    # We iterate over each value in sex (just "M" and "F")
    for sex in gender_values:
        # This updates the dictionary of search terms to include gender
        # and converts all keys into a string that will be the key to our final
        # dictionary of results.
        new_search[gender_query] = sex
        dict_values_list = list(new_search.values())
        full_search_key = "+".join(dict_values_list)
        # We will only re-run the post, if there is no key in our saved dictionary.
        # that indicates the post has not been run before.
        if full_search_key not in re_scrape_results.keys():
            # Our output is by default in json format. Specifically, a list of
            # dictionaries, each dictionary being a search result.
            doc_list = ccare_post(new_search, monitoring=monitoring)

        else:
            doc_list = re_scrape_results[full_search_key]

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
                if doc["locationZipCode"] == new_search["searchAddress"][0:5]:
                    doc_count += 1
            # Inform the viewer how many doctors that search found, if they
            # so choose.
            if monitoring is True:
                print(f"The search found {doc_count} doctors in this zipcode.")
        
        else:
            # If the list is empty, that means exatly 250 providers were found
            # in that zip_code and additional filters are needed. We specify this
            # for instances when we are running the re-scrape after being disconnected.
            doc_count = 250

        if doc_count < 250:
            # If we have less than 250 providers, we update the dictionary,
            # write the file, and move on.
            re_scrape_results[full_search_key] = doc_list
            with open(scnd_scrape_file, "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)
        else:
            # If we have exactly 250, we will now add a specialty search for
            # every specialty associated with this provider type. First we leave
            # an empty list so that on future scrapes, we know that this search
            # has already been attempted.
            re_scrape_results[full_search_key] = []
            with open(scnd_scrape_file, "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)

            # Update the viewer.
            if monitoring is True:
                print("Checking additional filters.")

            # There is a different list of provider specialties for each
            # provider type. The list of additional specialty codes associated
            # with those types can be found in SPECIALTIES_BY_CODE in
            # search_parameters.search_parameters.py.
            # SPECIAlTIES_BY_CODE is a dictionary that links each providerTypeSelect
            # code with its associated list of sub_specialty codes so that it
            # can be accessed simply here.
            specialties_list = SPECIALTIES_BY_CODE[new_search["providerTypeSelect"]]

            # We iterate over each possible specialty for the providerTypeSelect
            # code on this search.
            for s in specialties_list:

                # Add/update our additional search parameter.
                new_search["speciality"] = s

                # Update the key that lets us access this data once it has been saved.
                dict_values_list = list(new_search.values())
                full_search = "+".join(dict_values_list)

                # If this key has been used, then this search has been run and we
                # can move on to the next one.
                if full_search in re_scrape_results.keys():
                    continue

                doc_list = ccare_post(new_search, monitoring=monitoring)
                re_scrape_results[full_search] = doc_list
                with open(scnd_scrape_file, "w") as f:
                    json.dump(re_scrape_results, f, indent=4, sort_keys=True)


def gen_re_scrape_list():
    """
    This function loops through the raw scrape results and checks which
    provider code/ zip code combinations need to be re-scraped.
    Inputs: None
    Returns:
    re_scrape_list (lst of dicts): A list of search parameters that
    need to be re-run with additional filters.
    """
    first_scrape_file = pathlib.Path(__file__).parent / "scraped_data/ccare_scrape.json"
    coordinates_file = (
        pathlib.Path(__file__).parent
        / "search_parameters/cook_county_coordinates_zips.json"
    )

    # Loads the file from the first scrape into a dictionary.
    with open(first_scrape_file) as f:
        fst_scrape = json.load(f)
    # Loads the address parameters so that we can fully represent the search
    # that we need to re-run.
    with open(coordinates_file) as d:
        address_params = json.load(d)

    re_scrape_list = []

    # Iterating over all of our results.
    for zip_code, doc_dict in fst_scrape.items():
        for doc_code, doc_list in doc_dict.items():
            docs_in_zip = 0
            # Here we check if a given zip_code - provider code combination
            # is "packed". That means we are returning the maxmium number
            # possible providers in a givenzip code and we are likely bumping into
            # the limit on post-responses. If so, we need to re-run the post
            # with additional parameters.
            for doc in doc_list:
                if zip_code == doc["locationZipCode"]:
                    docs_in_zip += 1

            # If we found a "packed" zip_code-search pair, we create a dictionary
            # of the search terms used in that search to access for the re-scrape.
            if docs_in_zip == 250:
                search_terms = {"mileRadiusForSearch": "10", "mileRadius": "10"}
                search_terms["providerTypeSelect"] = doc_code
                search_terms["searchAddress"] = "".join([zip_code, ", IL"])
                search_terms["providerAddress"] = address_params[zip_code]
                re_scrape_list.append((search_terms))

    return re_scrape_list
