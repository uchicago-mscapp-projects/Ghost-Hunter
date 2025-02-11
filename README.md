# Ghost-Hunter
Looking for Ghosts in Medicaid Provider Directories

## Team 

Gabriel Barrett, Magdalena Barros, Paula Cadena

## Project Abstract

A pervasive problem in the American Healthcare system is the existence of “ghost networks.” These are lists of providers that a health insurance plan falsely presents to healthcare consumers as “in-network.” Ghost Hunter is an application that audits the provider network of County Care, one of Illinois five Medicaid Managed Care Organizations. The goal is to see how what percentage of County Care’s network can be independently verified. First, we scraped County Care’s [find a provider](https://countycare.valence.care/member/#findAProvider) intermittently from February 16th until March 6th, 2024 to construct an original sample database of their healthcare service provider network.  Second, we attempt to verify that each located provider is accurately represented by matching them either in the State of Illinois’ [IMPACT database](https://ext2.hfs.illinois.gov/hfsindprovdirectory) or in the [National NPI Registry](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination). IMPACT is a state database that tracks all providers approved to bill Illinois Medicaid. If no trace of a provider exists in IMPACT, the provider is not eligible to treat patients on Medicaid. The NPI registry is a registry of all individual or corporate entities that need to bill health insurance. Matching on the NPI is important as a way to verify a provider’s contact information and residence in Illinois, as well as a source for future researchers as NPI numbers, are very close to unique identifiers in the healthcare space. From this analysis, we estimate groups of providers that while listed in County Care’s directory are not actually seeing or billing Medicaid patients, and whose presence in County Care’s directory is misleading to patients and inflates the strength of their network. Our initial match percentages reflect the difficulty of linking records with inconsistent identifiers, but we hope that this data can be of use to us and future researchers examining health insurance network adequacy.


## Getting Started:


## Using Ghost Hunter

The main uses of Ghost Hunter are (1) to access the original datasets, "merge.csv" and "scrap.csv", (2)
to view the dashboard visualizations that depict trends in matches across Illinois geography
and specific healthcare provider types, and (3) to re-run the web-scrape and matching process
we used to construct our data set.

## Merge and Scrap

Merge.csv and Scrap.csv are two subsets of County Care's provider network. Merge is the data that we were able to
link with NPI numbers. While we have provided a limited number of variables in Merge that is because the first name, 
last name, NPI number combination should allow researchers to easily link this data with external data. 

Scrap.csv encompasses all of the unique providers that we were able to scrape from County Care's website, after removing duplicates. Each row is a provider, not a person. Some providers are people (such as doctors, dentists, etc.) However, some
are healthcare companies such as hospital groups and long-term-care facilities. We recommend using the "type" column for
additional clarity.


## Viewing Summary Visualizations

We created a simple set of visualizations to understand how our scraper performed
and to check if there was any obvious variation in provider matches (i.e.ghosts/non-ghosts).
To view these, do the following:

1) If you haven't already, open up your terminal to the directory where you want to save the Ghost-Hunter
repository and run:
    ```git clone https://github.com/Jibbie17/Ghost-Hunter```

2) Run:
    ```poetry install ```
and then
    ```poetry shell```
to ensure that all your packages are installed and your virtual environment is working.

3) In order to create and view a unique link where our visualizations are hosted navigate to the root of your
the repository where "gh should be the only folder. Then run:
```python -m gh```
If you haven't activated your poetry shell you might need to run:
```poetry python -m gh```.
You should get a response that looks something like:
```Dash is running on http://###.#.#.##```
You might also get a large red warning about it being a development server. Don't worry about

## Re-Running the Webscraping and Matching Process

Provider networks change month to month as doctors and insurers evaluate
their relationships in relation to the market. Depending on the permanence of
County Care's Website, Ghost Hunter is a useful tool for getting point source information
about the size and strength of County Care's provider Network. Before using the web scraper,
make sure that your computational needs are minimal and that you are able to leave your computer alone
and connected to a power source. The previous web scrape combined took approximately 24 hours to complete.
If possible, check your computer frequently in the event that the website doesn't answer the scraper or 
a request is hanging for more than 3 minutes. County Care's website is slow, so Ghost Hunters is built to
be re-run until all specified searches are complete.

1) Open up your terminal in the directory where you want to save the Ghost-Hunter
repository and run: ```git clone https://github.com/Jibbie17/Ghost-Hunter```

2) Run: ``` poetry install ``` and then ``` poetry shell ```
to ensure that all your packages are installed and your virtual environment is working.

3) Before you launch the scraper you should make sure you have the write data files. The two data files we use on matching,
the NPI monthly download file and the IMPACT database, are very large and cannot be stored in git. In addition, they
both update regularly with the information of new doctors, so it is worth re-running the merge every couple of months.
Before you open the terminal download the NPI monthly file [here](https://download.cms.gov/nppes/NPI_Files.html). You will need to click on the link that usually starts "Full Replacement Monthly NPI File" to get a zipped folder and then from that zipped folder you will want to copy the file titled "npidata_pfile_20050523-<LAST RELEASE>.csv", put it in folder titled
"gh/data_compilation/data_input." AND BE SURE TO RENAME IT TO npi.csv. We have a .gitignore set up for this file, but its name changes every month. Then DO THE SAME with the [IMPACT database](https://ext2.hfs.illinois.gov/hfsindprovdirectory). For that file we have our .gitignore set to impact.txt. If you change either file to something else, be sure to update the .gitignore.

4) To launch the scraper, start in the root of the repository where you should see the folder "gh". From the terminal run:
    ```python -m gh.data_compilation ```
Or, if you have not run poetry shell, you will need to run:
    ```poetry python -m gh.data_compilation```

5) If this is not your first scrape you will be asked if you want to overwrite your previous
scrape. You should see:

"Data from the last scrape is saved at gh/data_compilation/scrapers/scraped_data/ccare_results_clean.json. 
Would you like to overwrite this file? [y/n]"

If so, we recommend that you answer n. If you answer y, the scraper will clean out your last file and 
The scrape takes a long time and is built such that each query adds data to the same file UNLESS you specify at the first prompt that you want to overwrite.

6) You will then be asked if you want to monitor during the search. Specifically:

"Would you like to see the scrape result appear live in your terminal? [y/n]"

If you select yes, MONITORING, will be turned on and the scraper will provide intermittent
progress updates to your terminal.

7) Sit back, relax, and let the computer do the work!




 
