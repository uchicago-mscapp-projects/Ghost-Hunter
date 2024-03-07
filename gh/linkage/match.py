import pandas as pd
import jellyfish
from clean.clean_impact import clean_impact
from clean.clean_npi import match_npi
from clean.clean_scrap import match_scrap

COLUMNS_IMPACT = ["npi", "first_name", "last_name", "zip_code", "address"]

THRESHOLD = 0.7

def match(npi, scrap, impact, selected_npi, selected_scrap):
    """
    Perform matching operations on scrap (CountyCare) dataset using oficial information
    to identify health care providers.

    Parameters:
    - npi (DataFrame): DataFrame containing NPI data.
    - scrap (DataFrame): DataFrame containing scrap data.
    - impact (DataFrame): DataFrame containing impact data.
    - selected_npi (DataFrame): DataFrame with selected columns in NPI data.
    - selected_scrap (DataFrame): DataFrame with selected columns in scrap data.

    Returns:
    - DataFrame: Cleaned and matched DataFrame with the results.
    """
    df_npi = match_npi(npi, selected_npi)
    df_impact = clean_impact(impact)[COLUMNS_IMPACT]
    df_scrap = match_scrap(scrap, selected_scrap)

    # 1. Merge by last name and phone number with npi.
    df_scrap = first_approach(df_scrap,df_npi)

    # 2. Merge by last name and zip code with impact, update, or drop based on the similarity of names.
    df_scrap = second_approach(df_scrap,df_impact)

    # 3. Subset impact by zip code and check for similarity in last name, first name, and address
    df_scrap = third_approach(df_scrap,df_impact)
    
    df_scrap.drop(columns=["zip_code", "address"], inplace=True)
    df_scrap.sort_values(by="npi", ascending=True, inplace=True, key=lambda x: x.astype(str))
    df_scrap.drop_duplicates(
        subset=["first_name", "last_name", "phone_number"], keep="first", inplace=True
    )

    return df_scrap

def first_approach(df_scrap,df_npi):
    """
    Perform a primary matching approach to fill missing 'npi' values in df_scrap 
    using df_npi based on exact matches of last name and phone number.

    Parameters:
    - df_scrap (DataFrame): Scrap DataFrame.
    - df_npi (DataFrame): NPI DataFrame.

    Returns:
    - DataFrame: Merged DataFrame.
    """
    return pd.merge(
        df_scrap,
        df_npi[["last_name", "phone_number", "npi"]],
        on=["phone_number", "last_name"],
        how="left",
    )

def second_approach(df_scrap,df_impact):
    """
    Perform a secondary matching approach to fill missing 'npi' values in df_scrap 
    with df_impact, exact zip codes, last name, and similar first name.

    Parameters:
    - df_scrap (DataFrame): Scrap DataFrame containing 'npi' values to be filled.
    - df_impact (DataFrame): Impact DataFrame containing additional information for matching.

    Returns:
    - DataFrame: Updated df_scrap with filled 'npi' values based on similarity with df_impact.
    """
    subset_df_scrap = df_scrap[df_scrap["npi"].isna()]
    df_scrap = df_scrap[df_scrap["npi"].notna()]
    df_scrap_2 = pd.merge(
        subset_df_scrap,
        df_impact[["last_name", "first_name", "zip_code", "npi"]],
        on=["zip_code", "last_name"],
        how="left",
    )

    # Calculate Jaro-Winkler similarity using vectorized operations
    name_similarity = df_scrap_2.apply(
        lambda row: jellyfish.jaro_winkler_similarity(str(row["first_name_y"]), str(row["first_name_x"])),
        axis=1
    )

    # Fill 'npi' based on the condition
    df_scrap_2.loc[name_similarity >= THRESHOLD, "npi_x"] = df_scrap_2.loc[
        name_similarity >= THRESHOLD, "npi_y"
    ]

    df_scrap_2.rename(columns={"npi_x": "npi", "first_name_x": "first_name"}, inplace=True)
    df_scrap_2.drop(columns=["npi_y", "first_name_y"], inplace=True)

    df_scrap = pd.concat([df_scrap, df_scrap_2], ignore_index=True)
    df_scrap.drop_duplicates(inplace=True)

    return df_scrap

def third_approach(df_scrap,df_impact):
    """
    Perform a tertiary matching approach to fill missing 'npi' values in df_scrap 
    with df_impact, subsetting by zip code and looking for similarities in first
    name, last name, and address. 

    Parameters:
    - df_scrap (DataFrame): Scrap DataFrame containing 'npi' values to be filled.
    - df_impact (DataFrame): Impact DataFrame containing additional information for matching.

    Returns:
    - DataFrame: Updated df_scrap with filled 'npi' values based on similarity with df_impact.
    """
    subset_df_scrap = df_scrap[df_scrap["npi"] == "nan"]
    df_scrap = df_scrap[df_scrap["npi"] != "nan"]

    for _, row in subset_df_scrap.iterrows():
        zip_df_impact = df_impact[df_impact["zip_code"] == row["zip_code"]].astype(str)

        # Vectorized similarity calculations
        name_similarity = jellyfish.jaro_winkler_similarity(
            row["first_name"], zip_df_impact["first_name"]
        )
        last_similarity = jellyfish.jaro_winkler_similarity(
            row["last_name"], zip_df_impact["last_name"]
        )
        address_similarity = jellyfish.jaro_winkler_similarity(
            row["address"], zip_df_impact["address"]
        )

        # Update when it finds a match
        match_index = (name_similarity >= THRESHOLD) & (last_similarity >= THRESHOLD) & (address_similarity >= THRESHOLD)
        
        if match_index.any():
            first_match_index = match_index.idxmax()
            df_scrap.at[row.name, "npi"] = zip_df_impact.loc[first_match_index, "npi"]
            break

    df_scrap = pd.concat([df_scrap, subset_df_scrap], ignore_index=True)
    
    return df_scrap
