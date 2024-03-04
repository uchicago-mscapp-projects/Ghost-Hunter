import pandas as pd
import pathlib

def merge_data_visualization():
    '''
    Generates the basis database to be able to make visulizations 
    
    Returns: dataframe
    '''
    
    merge_path = pathlib.Path(__file__).parent / "merge.csv"
    scrap_path = pathlib.Path(__file__).parent / "scrap.csv"
    df_merge = pd.read_csv(merge_path)
    df_scrap = pd.read_csv(scrap_path)

    #merge the merge and the scrape data
    df= pd.merge(df_merge, df_scrap, how='left', on=['first_name','last_name','phone_number'])

    #We only want to work with people, so if they do not have first name they are institutions
    df = df[df['first_name'].notna()]

    #Not consider unusual situations (institutions with first name)
    total_count = len(df)
    type_counts = df['type'].value_counts()
    filtered_types = type_counts[type_counts / total_count >= 0.01].index
    df = df[df['type'].isin(filtered_types)]


    return df 

def get_match_providertype_data(df):
    '''
    Calculates the total match and non_match providers for each 
    provider type. 

    Returns: dataframe
    '''
    
    list_of_tuples = []

    for provider_type in df['type'].unique():
        #total for each provider type
        total = df.loc[df['type'] == provider_type].shape[0]
        df_provider = df.loc[df['type'] == provider_type]
        #Match / Non-Match
        num_match = df_provider['npi'].count()
        num_nonmatch = df_provider['npi'].isna().sum()
        prob_match = num_match/total 
        prob_nonmatch = num_nonmatch / total
    
        list_of_tuples.append((provider_type, total, num_match,num_nonmatch,
                                prob_match, prob_nonmatch ))

    #sorted descending by Total
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1])

    data = pd.DataFrame(list_of_tuples,
                    columns=['Provider Type','Total', 'Match', 'Non-Match',
                             'Prob Match', 'Prob Non-Match'])
    return data


def get_match_zipcode_data(df):
    '''
    Calculates the total match and non_match zipcode for each 
    zip code. 

    Returns: dataframe
    '''
    
    list_of_tuples = []

    for zip_code in df['zip_code'].unique():
        #total for each provider type
        total = df.loc[df['zip_code'] == zip_code].shape[0]
        df_zip = df.loc[df['zip_code'] == zip_code]
        #Match / Non-Match
        num_match = df_zip['npi'].count()
        num_nonmatch = df_zip['npi'].isna().sum()
        prob_match = num_match/total 
        prob_nonmatch = num_nonmatch / total
    
        list_of_tuples.append((zip_code, total, num_match,num_nonmatch,
                                prob_match, prob_nonmatch ))

    data = pd.DataFrame(list_of_tuples,
                    columns=['Zip Code','Total', 'Match', 'Non-Match',
                             'Prob Match', 'Prob Non-Match'])
    return data

