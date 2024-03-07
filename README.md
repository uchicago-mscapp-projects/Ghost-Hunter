# Ghost-Hunter
Looking for Ghosts in Medicaid Provider Directories

## Team 

Gabriel Barrett, Magdalena Barros, Paula Cadena

## Project Abstract

A pervasive problem in the American Healthcare system is the existence of “ghost networks.” These are lists of providers that a health insurance plan falsely present to health care consumers as “in-network.” Ghost Hunter is an application which audits the provider network of County Care, one of Illinois five Medicaid Managed Care Organizations. The goal is to see how what percentage of County Care’s network can be independently verified. First, we scraped County Care’s [find a provider](https://countycare.valence.care/member/#findAProvider) intermittently from February 16th until March 6th, 2024 to construct an original sample database of their health care service provider network.  Second, we attempt to verify that each located provider is accurately represented by matching them either in the State of Illinois’ [IMPACT database](https://ext2.hfs.illinois.gov/hfsindprovdirectory) or in the [National NPI Registry](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination). IMPACT is a state database that tracks all providers approved to bill Illinois Medicaid. If no trace of a provider exists in IMPACT, the provider is not eligible to treat patients on Medicaid. The NPI registry is a registry of all individual or corporate entities that need to bill health insurance. Matching on the NPI is important as a way to verify a provider’s contact information and residence in Illinois as well as a source for future researchers as NPI numbers are very close to unique identifiers in the health care space. From this analysis we estimate groups of providers that while listed in County Care’s directory are not actually seeing or billing Medicaid patients, and whose presence in County Care’s directory is misleading to patients and inflates the strength of their network. Our initial match percentages reflect the difficulty of linking records with inconsistent identifiers, but we hope that this data can be of use to us and future researchers examining health insurance network adequacy.


## Getting Started:

python -m gh (Press CTRL+C to quit)

URL http://127.0.0.1:8060/ 

## Using Ghost Hunter

The main uses of Ghost Hunter are (1) to access the original dataset, "data_set_name", (2)
to view the dashboard visualizations which depict trends in matches accross Illinois geography
and specific health care provider types, and (3) to re-run the web-scrape and matching process
we used to construt our data set.

## Understanding "dataset name"

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
to ensure that all your pacakages are installed and your virtual environment is working.

3) In order to create view a unique link where our visualizations are hosted navigate to the root of your
repository where "gh should be the only folder. Then run:
```python -m gh```
If you haven't activated your poetry shell you might need to run:
```poetry python -m gh```.
You should get a response that looks something like:
```Dash is running on http://###.#.#.##```
You might also get a large red warning about it being a development server. Don't worry about

## Re-Running the Webscraping and Matching Process

Provider networks chnage month to month as doctors and insurers evaluate
their relationships in relation to the market. Depending on the permanance of
County Care's Website, Ghost Hunter is a useful tool for getting point source infromation
about the size and strength of County Care's provider Network. Before using the web scraper,
make sure that your computational needs are minimal and that you are able to leave your computer alone
and connected to a power source. The previous web scrape combined took approximately 24 hours to complete.
If possible, check your computer frequently in the event that the website doesn't answer the scraper or 
a request is hanging for more than 3 minutes. County Care's website is slow, so Ghost Hunters is built to
be re-run until all specified searches are complete.



1) Open up your terminal in the directory where you want to save the Ghost-Hunter
repository and run: ```git clone https://github.com/Jibbie17/Ghost-Hunter```

2) Run: ``` poetry install ``` and then ``` poetry shell ```
to ensure that all your pacakages are installed and your virtual environment is working.

3) Before you launch the scraper you should make sure you have the write data files. The two data files we use on matching,
the NPI monthly download file and the IMPACT database, are very large and cannot be stored in git. In addition, they
both update regularly with the information of new doctors, so it is worth re-running the merge every couple of months.
Before you open the terminal download the NPI monthly file [here](https://download.cms.gov/nppes/NPI_Files.html). You will need to click on the link that usually starts "Full Replacement Monthly NPI File" to get a zipped folder and then from that zipped folder you will want to copy the file titled "npidata_pfile_20050523-<LAST RELEASE>.csv", put it in folder titled
"gh/data_compilation/data_input." AND BE SURE TO RENAME IT TO npi.csv. We have a .gitignore set up for this file, but its name changes every month. Then do the same with the [IMPACT database](https://ext2.hfs.illinois.gov/hfsindprovdirectory). 

3. To launch the scraper, start in the root of the repository where you should see the folder "gh". From the terminal run:
    ```python -m gh.data_compilation ```
Or, if you have not run poetry shell, you will need to run:
    ```poetry python -m gh.data_compilation```

 
