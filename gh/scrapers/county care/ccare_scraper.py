import json
import lxml
import requests
from utils import make_request, make_post

url = "https://countycare.valence.care/member/rest/findAProvider/search"

post_dictionary = {"providerTypeSelect":"06",
                   "providerName":"",
                   "mileRadiusForSearch":"5",
                   "mileRadius":"5",
                   "gender":"null",
                   "network":"null",
                   "service":"null",
                   "speciality":"null",
                   "language":"null",
                   "specialNeeds":"null",
                   "handicapAccess":"null",
                   "acceptNewPatient":"null",
                   "providerAddress":"41.80153,-87.60134",
                   "hospitalAffiliation":"null",
                   "groupAffiliation":"null",
                   "groupAffiliationName":"null",
                   "providerFirstName":"null",
                   "providerLastName":"null",
                   "providerNumber":"null",
                   "providerCity":"null",
                   "providerState":"null",
                   "providerPhone":"null",
                   "lob":"null",
                   "policyBenefitId":"null",
                   "pcpOptions":"null",
                   "affiliationType":"null",
                   "errored":"",
                   "searchAddress":"60615,IL",
                   "patientAgeRangeSeen":"null",
                   "networkPriority":"null",
                   "accreditationTitle":"null",
                   "accreditationOrganization":"null",
                   "providerSelectOption":"LIKE",
                   "acceptsBlindVisuallyImpairedPatients":"false",
                   "acceptsHearingImpairedPatients":"false",
                   "dualDemonstrationPopulationTraining":"false",
                   "acceptsHivAidsPatients":"false",
                   "acceptsHomelessPatients":"false",
                   "provAffiliation_specialNeeds":"false",
                   "acceptsChronicIllnessPatients":"false",
                   "acceptsSeriousMentalIllnessPatients":"false",
                   "acceptsPhysicalDisabilitiesPatients":"false",
                   "acceptsCoOccuringDisordersPatients":"false",
                   "open24By7":"false",
                   "adjustableExamTable":"false",
                   "handicapSupport":"false",
                   "handicapParking":"false",
                   "culturalCompetencyTraining":"false",
                   "accessibleByPublicTransportation":"false",
                   "translationServices":"false",
                   "wheelchairAccessibleExamRoom":"false",
                   "wheelchairAccessibleRestroom":"false",
                   "wheelchairRamps":"false",
                   "ttyService":"false",
                   "transactionsExcludedInd":"false"}

headers_dict = {'Connection': 'keep-alive',
                'Content-Type' : 'application/json',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': 'Android'}

def scrape_ccare():
    """
    Runs make_request with ccare data. 
    """
    return make_post(url, post_dictionary, headers_dict)

