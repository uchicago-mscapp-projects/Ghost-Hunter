import pathlib
from .scrapers.county_care.ccare_scrape_clean import scrape_to_merge
from .clean_scrap import clean_scrap
from .match import match

if __name__ == "__main__":
    final_scrape = (
        pathlib.Path(__file__).parent
        / "scrapers/county_care/scraped_data/ccare_results_clean.json"
    )
    if final_scrape.exists():
        print(
            """Data from the last scrape is saved at 
            gh/data_compilation/scrapers/scraped_data/ccare_results_clean.json. 
            Would you like to fill in holes from the last search? Otherwise,
            we will start fresh. [y/n]"""
        )
        if input().lower == "y":
            FRESH = False
        else:
            """Please be advised that a full scrape can take as long as 24 hours
            to run. Are you sure you want to proceed and overwrite the last save?
            """
            if input().lower == "y":
                FRESH = True
    print(
        """Please keep your computer plugged into a power source and connected to the internet.
            If possible, check every four hours to ensure
            the scrape has not been interrupted. Would you like to see the scrape 
            result appear live in your terminal? [y/n]"""
    )
    if input().lower == "y":
        MONITORING = True
    else:
        MONITORING = False

    scrape_to_merge(fresh=True, monitoring=MONITORING)

selected_npi = pathlib.Path(__file__).parent / "data_input/selected_columns.csv"
selected_scrap = pathlib.Path(__file__).parent / "data_input/selected_columns_s.csv"

npi = pathlib.Path(__file__).parent / "data_input/npi.csv"
impact = pathlib.Path(__file__).parent / "data_input/impact.txt"

cleaned_scrape = pathlib.Path(__file__).parent / "data_output/county_care.csv"

clean_scrap(final_scrape, selected_scrap).to_csv(
    cleaned_scrape, index=False
)
match(npi, final_scrape, impact, selected_npi, selected_scrap).to_csv(
    pathlib.Path(__file__).parent / "data_output/merge.csv", index=False
)

    
