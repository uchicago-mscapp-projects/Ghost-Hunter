import pathlib
from .scrapers.county_care.ccare_scrape_clean import scrape_to_merge
from .clean import clean_scrap, clean_npi, clean_impact


if __name__ == "__main__":
    final_scrape = (
        pathlib.Path(__file__).parent
        / "scrapers/county_care/scraped_data/ccare_results_clean.json"
    )
    if final_scrape.exists():
        print(
            """Data from the last scrape is saved at 
            gh/data_compilation/scrapers/scraped_data/ccare_results_clean.json. 
            Would you like to fill in holes from the last search? Otherwise
            we will start fresh. [y/n]"""
        )
        if input().lower == "y":
            fresh = False
        else:
            """Please be advised that a full scrape can take as long as 24 hours
            to run. Are you sure you want to proceede and overwrite the last save?
            """
            if input().lower == "y":
                fresh = True

        print(
            """Please keep you computer plugged into a power source and connected to the internet.
               If possible check every four hours to ensure
               that the scrape has not been interrupted. Would you like to see the scrape 
               result appear live in your terminal? [y/n]"""
        )
        if input().lower == "y":
            monitoring = True
        else:
            monitoring = False

    scrape_to_merge(fresh=True, monitoring=monitoring)

    