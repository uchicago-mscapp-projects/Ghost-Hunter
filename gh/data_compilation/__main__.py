import pathlib
from .scrapers.county_care.ccare_scrape_clean import scrape_to_merge
from .clean.clean_scrap import clean_scrap
from .linkage.match import match

if __name__ == "__main__":
    FRESH = False
    final_scrape = (
        pathlib.Path(__file__).parent
        / "scrapers/county_care/scraped_data/ccare_results_clean.json"
    )
    if final_scrape.exists():
        print(
            """Data from the last scrape is saved at 
            gh/data_compilation/scrapers/scraped_data/ccare_results_clean.json. 
            Would you like to overwrite this file? [y/n]"""
        )
        if input().lower == "y":
            FRESH = True
        else:
            FRESH = False
    print(
        """Please keep your computer plugged into a power source and connected to the internet. The scrape can take up to 24 hours.
            If possible, check every four hours to ensure the scrape has not been interrupted. Would you like to see the scrape 
            result appear live in your terminal? [y/n]"""
    )
    if input().lower == "y":
        MONITORING = True
    else:
        MONITORING = False

    scrape_to_merge(fresh=FRESH, monitoring=MONITORING)

    selected_npi = pathlib.Path(__file__).parent / "data_input/selected_columns.csv"
    selected_scrap = pathlib.Path(__file__).parent / "data_input/selected_columns_s.csv"

    npi = pathlib.Path(__file__).parent / "data_input/npi.csv"
    impact = pathlib.Path(__file__).parent / "data_input/impact.txt"

    cleaned_scrape = pathlib.Path(__file__).parent / "data_output/county_care.csv"

    clean_scrap(final_scrape, selected_scrap).to_csv(
    cleaned_scrape, index=False)
    match(npi, final_scrape, impact, selected_npi, selected_scrap).to_csv(
        pathlib.Path(__file__).parent / "data_output/merge.csv", index=False
)