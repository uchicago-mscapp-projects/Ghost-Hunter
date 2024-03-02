# Ghost-Hunter
Looking for Ghosts in Medicaid Provider Directories

## Team 

Gabriel Barrett, Magdalena Barros, Paula Cadena

## Project Abstract

A pervasive problem in the American Healthcare system is the existence of “ghost networks.” These are lists of providers that a health insurance plan falsely present to health care consumers as “in-network.” This project will attempt to use web scraping to partially audit the in-network provider list of one of Illinois Medicaid plans. We will scrape the public page of one of the insurance plans for the names, phone numbers, business addresses and National Provider Identification (NPI) numbers for each physician listed as in-network. Depending on the size of the data we may narrow the focus to Licensed Counselors who provide therapy since this problem is particularly pernicious in behavioral health. We will use these variables to identify these providers in the NPI enumeration database, which includes additional information on each provider, particularly their license number. We will then use the license number in tandem with Illinois’ license number validation tool to validate whether the provider's license is current and whether the contact information the insurer lists is accurate. We are considering other validation strategies such as checking phone numbers against the white pages and, in the case of counselors, checking that they list themselves as in-network on public websites such as APA’s find a therapist tool. We will use this data to create visualizations that display their percentage of physicians for each specialty that we can validate are accurately presented by the Illinois Medicaid plan and by each validation metric.  

## Getting Started:

python ./app.py

## Matching Data: 
 

**NPI Registry**

Description: This is a dataset of National Provider Identification Numbers. All health care providers need to apply for one in order to bill.  

**Data access:** 

API: https://npiregistry.cms.hhs.gov/api-page  

Downloadable Data: https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination  

Description: https://www.cms.gov/outreach-and-education/medicare-learning-network-mln/mlnproducts/downloads/npi-what-you-need-to-know.pdf  

Illinois Medicaid Health Insurance Providers: 

Overview: https://hfs.illinois.gov/medicalclients/managedcare.html  

Scrapable Data: 

Aetna (Best option): https://www.aetnabetterhealth.com/Illinois-medicaid/find-provider   

Blue Cross Blue Shield: https://my.providerfinderonline.com/?ci=il-med-cchp&network_id=11152019&geo_location=41.780399999999986,-87.6027&locale=en  

**County Care** 

https://countycare.valence.care/member/#findAProvider

**Molina** 

Illinois License Look-Up 

Overview on counselor licenses in Illionois: https://www.thechicagoschool.edu/insight/career-development/difference-lpc-lcpc-licensing-illinois/#:~:text=According%20to%20the%20Illinois%20General,%2C%20substance%20abuse%2C%20and%20more.  

Bulk Data Lookup: https://idfpr.illinois.gov/licenselookup/bulklookup.html  

Data (with Captcha): https://www.illinois.gov/services/service.professional-license-look-up.html  

Physician Data for Researchers: https://www.ilsos.gov/departments/archives/databases/physearch.html  

APA Psychologist Locator 

Overview: The American Psychology Association’s Portal to help patients find therapists. 

Data: https://locator.apa.org/results/1/60615/25/  

National Register of Psychologists 

https://www.findapsychologist.org/  

 

 

**How can we validate providers?** 

Requirements for Illinois Medicaid Providers 

Source: https://hfs.illinois.gov/content/dam/soi/en/web/hfs/sitecollectiondocuments/Chapter100GeneralHandbook.pdf  

 
