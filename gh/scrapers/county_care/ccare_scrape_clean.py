import json


def ccare_scrape_unpacker(file_path = "ccare_scrape.json"):
    """
    This function takes the json data and writes it into a list of dictionaries
    so that it can be processed for the merge.
    Inputs:
    file_path(str): The file path of the raw json data straight from the search.
    This variable is set to "ccare_scrape.json" as a default.
    Returns: Nothing. 
    """

    with open("ccare_scrape.json") as f:
        scrape_data = json.load(f)
    
    clean_data = []
    
    for _, doc_dict in scrape_data.items():
        for _, doc_list in doc_dict.items():
            clean_data.extend(doc_list)
    
    with open("ccare_results_clean.json", "w") as f:
        json.dump(clean_data, f, indent=4, sort_keys=True)


    
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