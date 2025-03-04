import json
from .ccare_scraper import scrape_ccare, re_scrape

def scrape_to_merge(fresh=False, monitoring=True):
    """
    This function runs all scrape and clean functions and saves the final .json
    output to scraped_data/ccare_scrape_clean.py.
    """

    scrape_ccare(fresh, monitoring)
    re_scrape(fresh, monitoring)

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
    "scraped_data/ccare_results_clean.json."
    """
    first_scrape_file = pathlib.Path(__file__).parent / "scraped_data/ccare_scrape.json"
    scnd_scrape_file = (
        pathlib.Path(__file__).parent / "scraped_data/re_scrape_ccare.json"
    )
    final_file = pathlib.Path(__file__).parent / "scraped_data/ccare_results_clean"
    with open(first_scrape_file) as f:
        scrape_data = json.load(f)

    clean_data = []

    for _, doc_dict in scrape_data.items():
        for _, doc_list in doc_dict.items():
            clean_data.extend(doc_list)

    with open(scnd_scrape_file) as d:
        re_scrape = json.load(d)

    for _, value in re_scrape.items():
        clean_data.extend(value)

    with open(final_file) as f:
        json.dump(clean_data, f, indent=4, sort_keys=True)
