import json
from .ccare_scraper import scrape_ccare, re_scrape

def scrape_to_merge(fresh = False):
    """
    This function runs all scrape and clean functions and saves the final .json
    output into linkage.
    """

    scrape_ccare(fresh)
    re_scrape(fresh)

    ccare_scrape_unpacker()



def ccare_scrape_unpacker():
    """
    This function takes the json data from the first round of scrapes
    and writes it into a list of dictionaries so that it can be processed
    for the merge.
    Inputs:
    file_path(str): The file path of the raw json data straight from the search.
    This variable is set to "ccare_scrape.json" as a default.
    Returns: Nothing. This function writes the output to 
    "ccare_results_clean.json."
    """

    with open("ccare_scrape.json") as f:
        scrape_data = json.load(f)
    
    clean_data = []
    
    for _, doc_dict in scrape_data.items():
        for _, doc_list in doc_dict.items():
            clean_data.extend(doc_list)
    
    with open("re_scrape_ccare.json") as d:
        re_scrape = json.load(d)
    
    for _, value in re_scrape.items():
        clean_data.extend(value)

    with open("ccare_results_clean.json", "w") as f:
        json.dump(clean_data, f, indent=4, sort_keys=True)    
