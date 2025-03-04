import pandas as pd
import json

COLUMNS_TO_MATCH = [
    "first_name",
    "last_name",
    "phone_number",
    "zip_code",
    "address",
]

def match_scrap(scrap, columns):
    """
    Extract and match relevant columns from preprocessed scrap data.

    Parameters:
    - scrap (str): Path to the JSON file containing scrap data.
    - columns (str): Path to the CSV file specifying selected columns.

    Returns:
    - DataFrame: Extracted and matched DataFrame with relevant columns from scrap data.
    """
    df = clean_scrap(scrap, columns)[COLUMNS_TO_MATCH]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    return df

def clean_scrap(json_path, columns_path):
    """
    Clean and preprocess scrap data (CountyCare) from a JSON file based on selected columns.

    Parameters:
    - json_path (str): Path to the JSON file containing scrap data.
    - columns_path (str): Path to the CSV file specifying selected columns.

    Returns:
    - DataFrame: Cleaned and preprocessed DataFrame with selected columns and standardized phone numbers.
    """
    # Before we clean the data we report how many unique search results we retrieved.
    count_search_results(json_path)

    with open(json_path, "r") as file:
        data = json.load(file)
    selected_columns = pd.read_csv(columns_path)
    df = pd.DataFrame(data)[selected_columns["var"].tolist()]

    # Read file only with selected columns
    column_mapping = dict(zip(selected_columns["var"], selected_columns["new_names"]))

    df.rename(columns=column_mapping, inplace=True)

    # Check atypical phone numbers and replace with NaN
    df["phone_number"] = df["phone_number"].where(
        ~df["phone_number"].map(
            lambda x: isinstance(x, str) and (len(x) != 10 or len(set(x)) == 1), None
        )
    )
    # Drop duplicates
    df.drop_duplicates(inplace=True)

    return df


def count_search_results(json_path):
    """
    This function counts the unique search results captured by the scrape.
    """
    data = json.load(json_path)
    sr = pd.DataFrame(data)
    sr = sr.drop('DISTANCE', axis=1)
    sr.drop_duplicates(inplace=True)
    with open('gh/data_compilation/data_output/total_retrieved_searches.json','w') as f:
        json.dump({"total_retrieved_searches":len(sr)},f, indent=4)
