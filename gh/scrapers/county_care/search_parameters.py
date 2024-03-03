

PROVIDER_TYPES = {'Primary Care Doctors/Nurses': 'PCP',
'Transportation': '01',
'Hospitals': '02',
'Surgery': '04',
'Behavioral Health Providers & Specialists': '06',
'Medical Specialists': '08',
'Hearing Services': '09',
'Physical, Occupational and Speech Therapy': '10',
'Durable Medical Equipment Suppliers': '11',
'Other Facilities': '13',
'Home Health': '14',
'Long Term Care Facilities & Nursing Homes': '15',
'Dialysis Centers': '17',
'Pharmacy': '18',
'Primary Care Facilities': '19',
"Lab and Imaging": '38',
'Supportive Living Facilities': '32',
'Urgent Care': '39'}

POST_DATA = {"providerTypeSelect": "06",
"providerName": "",
"mileRadiusForSearch": "5",
"mileRadius": "5",
"gender": "",
"network": "",
"service": "",
"speciality": "",
"language": "",
"specialNeeds": "",
"handicapAccess" : "",
"acceptNewPatient": "",
"providerAddress": "41.80153,-87.60134",
"hospitalAffiliation": "",
"groupAffiliation": "",
"groupAffiliationName": "",
"providerFirstName": "",
"providerLastName": "",
"providerNumber": "",
"providerCity": "",
"providerState": "",
"providerPhone": "",
"lob": "",
"policyBenefitId": "",
"pcpOptions": "",
"affiliationType": "",
"errored": "",
"searchAddress": "60615, IL",
"patientAgeRangeSeen": "",
"networkPriority": "",
"accreditationTitle": "",
"accreditationOrganization": "",
"providerSelectOption": "LIKE",
"acceptsBlindVisuallyImpairedPatients": "",
"acceptsHearingImpairedPatients": "",
"dualDemonstrationPopulationTraining": "",
"acceptsHivAidsPatients": "",
"acceptsHomelessPatients": "",
"provAffiliation_specialNeeds": "",
"acceptsChronicIllnessPatients": "",
"acceptsSeriousMentalIllnessPatients": "",
"acceptsPhysicalDisabilitiesPatients": "",
"acceptsCoOccuringDisordersPatients": "",
"open24By7": "",
"adjustableExamTable": "",
"handicapSupport": "",
"handicapParking": "",
"culturalCompetencyTraining":"",
"accessibleByPublicTransportation": "",
"translationServices": "",
"wheelchairAccessibleExamRoom":"" ,
"wheelchairAccessibleRestroom":"" ,
"wheelchairRamps":"" ,
"ttyService": "" ,
"transactionsExcludedInd": 'false'
}

url_search_results_count = "https://countycare.valence.care/member/rest/findAProvider/searchResultSize"

search_page_url = "https://countycare.valence.care/member/rest/findAProvider/search"

SECOND_SEARCH_PARAMS = [("gender", ["M", "F"])]

BEHAVIORAL_SPECIALTIES = [ "103TA0400X", "101YA0400X", "115", "08", "101Y00000X",
"2084P0805X", "103G00000X", "114", "107"]

SURGERY_SPECIALTIES = ["208C00000X", "1223S0112X", "207NS0135X", "207YX0905X",
                       "135","16", "2086H0002X", "207T00000X", "138", "2086X0206X",
                         "204E00000X", "74", "207YS0123X", "73", "2082S0099X",
                           "2082S0105X", "112", "69", "32", "2088F0040X", "141"]

SPECIALIST_SPECIALTIES = ["2084P0802X", "207K00000X", "10", "171M00000X", "111N00000X",
                          "172V00000X", "122300000X", "207N00000X", "133V00000X",
                          "207RE0101X", "207Y00000X","332H00000X", "207RG0100X",
                          "207RI0008X", "207QH0002X", "207RI0001X", "207RI0200X",
                          "207R00000X", "171R00000X", "170100000X", "100",
                          "176B00000X", "207RN0300X", "60", "62", "207RB0002X",
                          "67", "207RX0202X", "207W00000X", "208VP0000X", "81",
                          "363A00000X","213E00000X", "207RP1001X", "207RR0500X",
                          "173F00000X", "174400000X", "208800000X"]

PHYSICAL_THERAPY_SPECIALTIES = ["2083X0100X", "2081P2900X", "106", "261QP2000X",
                                "208100000X", "235Z00000X", "2081P0004X", "363LX0106X"]

PRIMARY_CARE_SPECIALTIES =["207Q00000X", "208D00000X", "207QG0300X", "363LA2100X",
                           "363LA2200X", "363LF0000X", "363LG0600X", "363LX0001X",
                           "363LP2300X", "363LW0102X"]

IMAGING_SPECIALTIES = ["261QR0208X", "50", "291U00000X", "207RM1200X", "202K00000X",
                    "2085R0202X", "2085D0003X", "2085U0001X", "2085R0001X",
                    "2085R0204X"]

SPECIALTIES_BY_CODE = {"06": BEHAVIORAL_SPECIALTIES, "08": SPECIALIST_SPECIALTIES,
                       "10": PHYSICAL_THERAPY_SPECIALTIES, 'PCP': PRIMARY_CARE_SPECIALTIES,
                       '38': IMAGING_SPECIALTIES, '04': SURGERY_SPECIALTIES}