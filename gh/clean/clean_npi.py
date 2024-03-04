import pandas as pd

columns_to_check = ["phone_number", "phone_number1", "phone_number2"]
columns_to_match = [
    "npi",
    "first_name",
    "last_name",
    "phone_number",
    "phone_number1",
    "phone_number2",
]
columns_to_keep = ["npi", "first_name", "last_name"]


def clean_npi(csv_path, columns_path):

    # Read files only with selected columns
    selected_columns = pd.read_csv(columns_path)
    df = pd.read_csv(csv_path, dtype=str, usecols=selected_columns["var"].tolist())

    # Rename columns
    column_mapping = dict(zip(selected_columns["var"], selected_columns["new_names"]))
    df.rename(columns=column_mapping, inplace=True)

    # Check for atypical phone-numbers and replace them with NaN
    atypical_mask = df[columns_to_check].map(
        lambda x: (
            isinstance(x, str) and len(x) != 10
            if isinstance(x, (str, float))
            else False
        )
    )
    df[columns_to_check] = df[columns_to_check].where(~atypical_mask, None)

    # Fill missing phone numbers
    df["phone_number"] = (
        df["phone_number"]
        .fillna(df["phone_number1"])
        .combine_first(df["phone_number2"])
    )

    return df


def match_npi(csv_path, columns_path):
    df = clean_npi(csv_path, columns_path)[columns_to_match]

    df = pd.melt(
        df,
        id_vars=columns_to_keep,
        value_vars=["phone_number1", "phone_number2", "phone_number"],
        value_name="unique_phone_number",
    )

    df.rename(columns={"unique_phone_number": "phone_number"}, inplace=True)
    df.drop(columns=["variable"], inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    return df
