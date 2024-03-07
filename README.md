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

To view the dashboard visualizations run 

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
repository and run: git clone https://github.com/Jibbie17/Ghost-Hunter

2)_ Run poetry install to 


 
