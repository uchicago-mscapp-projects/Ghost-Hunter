def recursive_re_scraper(old_search, new_parameters, post_data):
    """
    This function takes a list of dictionaries for searches that need to be re-run
    and recursively re-runs those searches.
    """
    print(new_parameters)

    with open("re_scrape_ccare.json") as f:
        re_scrape_results = json.load(f)

    next_search = new_parameters.pop()

    # This sets the post data to match the base search
    for query_type, value in old_search.items():
        post_data[query_type] = value
    
    new_query, new_values = next_search
    for value in new_values:
                
        # We construct our new search first by taking the values of the old
        # search and then by adding a new key-value pair.
        new_search = old_search.copy()
        new_search[new_query] = value
        
        post_data[new_query] = value
        
        #We concatenate all of the calues in our new search
        # and use that as the key associated with our output.
        # Full search is a string that saves this query in our final output.
        dict_values_list = list(new_search.values())
        full_search = "+".join(dict_values_list)
        
        # If the string identifying this query is in our dictionary, that means it has been run before.
        # Now we need to evaluate if that last query was completed.
        if full_search in re_scrape_results.keys():
            
            # If the output has more than one entry that means that this query
            # executed and no recursion was needed. We can end this iteration of the 
            # for loop and continue running the other queries.
            if len(re_scrape_results[full_search]) > 0:
                continue
            
            # If the ouput is an empty list, this means that recursion was needed.
            # we make the recursive call to make sure this query is complete.
            # Our new search is now the old search that the next call will build upon,
            # we pass the list of parameters which should no longer have the last query
            # and we pass the post_data, so that any updates to the post_data are done
            # within this recursive call only.
            else:
                recursive_re_scraper(new_search, new_parameters, post_data)
                continue                

        #Before we make the post we print what query we are using so we know from
        # the terminal where in the process our scraper is.
        print(full_search)
        r = make_post(search_page_url, post_data)

        # Within the for loop, we don't want our variables to varry over between
        # posts.
        post_data[new_query] = ""

        doc_list = r.json()
        doc_count = 0
        for doc in doc_list:
            if doc["locationZipCode"] == new_search['searchAddress'][0:5]:
                doc_count += 1
        print(doc_count)
        if doc_count < 250 or len(new_parameters) == 0:
            print("skip recursion")
            print(doc_count < 250)
            print(len(new_parameters))
            re_scrape_results[full_search] = r.json()
            with open("re_scrape_ccare.json", "w") as f:
                json.dump(re_scrape_results, f, indent=4, sort_keys=True)
        else:
            print("recurse!")
            re_scrape_results[full_search] = []
            print(new_parameters)
            recursive_re_scraper(new_search, new_parameters, post_data)
  

def scrape_annalyzer(file_path = "ccare_scrape.json"):
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