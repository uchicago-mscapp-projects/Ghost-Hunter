import pandas as pd
import jellyfish
from clean.clean_impact import clean_impact
from clean.clean_npi import match_npi
from clean.clean_scrap import match_scrap

columns_impact = ["npi", "first_name", "last_name", "zip_code", "address"]

THRESHOLD = 0.7

def match(npi, scrap, impact, selected_npi, selected_scrap):
    df_npi = match_npi(npi, selected_npi)
    df_impact = clean_impact(impact)[columns_impact]
    df_scrap = match_scrap(scrap, selected_scrap)

    # 1. merge by last-name and phone number with npi, only keep npi
    df_scrap = pd.merge(
        df_scrap,
        df_npi[["last_name", "phone_number", "npi"]],
        on=["phone_number", "last_name"],
        how="left",
    )

    # 2. merge by last name and zip code with impact,check similarity of name. Only keep npi
    # Filter the subset where 'npi' is NaN
    subset_df_scrap = df_scrap[df_scrap["npi"].isna()]
    df_scrap = df_scrap[df_scrap["npi"].notna()]
    # Merge only on the subset
    df_scrap_2 = pd.merge(
        subset_df_scrap,
        df_impact[["last_name", "first_name", "zip_code", "npi"]],
        on=["zip_code", "last_name"],
        how="left",
    )
    for index, row in df_scrap_2.iterrows():
        if pd.notna(row["first_name_y"]):
            # Calculate Jaro-Winkler similarity
            sim_name_prob = jellyfish.jaro_winkler_similarity(
                row["first_name_y"], row["first_name_x"]
            )
            # Check the condition and fill 'npi'
            if sim_name_prob >= THRESHOLD:
                df_scrap_2.at[index, "npi_x"] = df_scrap_2.at[index, "npi_y"]

    df_scrap_2.rename(
        columns={"npi_x": "npi", "first_name_x": "first_name"}, inplace=True
    )
    df_scrap_2.drop(columns=["npi_y", "first_name_y"], inplace=True)

    df_scrap = df_scrap.astype(str)
    df_scrap_2 = df_scrap_2.astype(str)

    df_scrap = pd.concat([df_scrap, df_scrap_2], ignore_index=True)
    df_scrap.drop_duplicates(inplace=True)

    # 3. Subset impact by zip-code and check for similarity in last name, first name and address
    # Filter the subset where 'npi' is NaN
    subset_df_scrap = df_scrap[df_scrap["npi"] == "nan"]
    df_scrap = df_scrap[df_scrap["npi"] != "nan"]

    #Check similarity if they are in the same zip-code
    for _, row in subset_df_scrap.iterrows():
        zip_df_impact = df_impact[df_impact["zip_code"] == row["zip_code"]].astype(str)
        for _, zip_row in zip_df_impact.iterrows():
            sim_name_prob = jellyfish.jaro_winkler_similarity(
                row["first_name"], zip_row["first_name"]
            )
            sim_last_prob = jellyfish.jaro_winkler_similarity(
                row["last_name"], zip_row["last_name"]
            )
            sim_address_prob = jellyfish.jaro_winkler_similarity(
                row["address"], zip_row["address"]
            )
            if (
                sim_name_prob >= THRESHOLD
                and sim_last_prob >= THRESHOLD
                and sim_address_prob >= THRESHOLD
            ):
                df_scrap.at[index, "npi"] = zip_row["npi"]

    df_scrap = df_scrap.astype(str)
    df_scrap_2 = subset_df_scrap.astype(str)

    df_scrap = pd.concat([df_scrap, df_scrap_2], ignore_index=True)
    df_scrap.drop(columns=["zip_code", "address"], inplace=True)
    df_scrap.sort_values(by="npi", ascending=True, inplace=True)
    df_scrap.drop_duplicates(
        subset=["first_name", "last_name", "phone_number"], keep="first", inplace=True
    )

    return df_scrap
