import pandas as pd

COLUMNS_TO_CHECK = ["phone_number", "phone_number1", "phone_number2"]
COLUMNS_TO_MATCH = [
    "npi",
    "first_name",
    "last_name",
    "phone_number",
    "phone_number1",
    "phone_number2",
]
COLUMNS_TO_KEEP = ["npi", "first_name", "last_name"]


def clean_npi(csv_path, columns_path):
    """
    Clean and preprocess NPI data from a CSV file based on selected columns.

    Parameters:
    - csv_path (str): Path to the CSV file containing NPI data.
    - columns_path (str): Path to the CSV file specifying selected columns.

    Returns:
    - DataFrame: Cleaned and preprocessed DataFrame with selected columns and standardized phone numbers.
    """
    # Read files only with selected columns
    selected_columns = pd.read_csv(columns_path)
    df = pd.read_csv(csv_path, dtype=str, usecols=selected_columns["var"].tolist())

    # Rename columns
    column_mapping = dict(zip(selected_columns["var"], selected_columns["new_names"]))
    df.rename(columns=column_mapping, inplace=True)

    # Check for atypical phone numbers and replace them with NaN
    atypical_mask = df[COLUMNS_TO_CHECK].map(
        lambda x: (
            isinstance(x, str) and len(x) != 10
            if isinstance(x, (str, float))
            else False
        )
    )
    df[COLUMNS_TO_CHECK] = df[COLUMNS_TO_CHECK].where(~atypical_mask, None)

    # Fill in missing phone numbers
    df["phone_number"] = (
        df["phone_number"]
        .fillna(df["phone_number1"])
        .combine_first(df["phone_number2"])
    )

    return df


def match_npi(csv_path, columns_path):
    """
    Extract and match unique phone numbers from preprocessed NPI data.

    Parameters:
    - csv_path (str): Path to the CSV file containing NPI data.
    - columns_path (str): Path to the CSV file specifying selected columns.

    Returns:
    - DataFrame: Extracted and matched DataFrame with unique phone numbers from NPI data.
    """
    df = clean_npi(csv_path, columns_path)[COLUMNS_TO_MATCH]

    df = pd.melt(
        df,
        id_vars=COLUMNS_TO_KEEP,
        value_vars=["phone_number1", "phone_number2", "phone_number"],
        value_name="unique_phone_number",
    )

    df.rename(columns={"unique_phone_number": "phone_number"}, inplace=True)
    df.drop(columns=["variable"], inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    return df
