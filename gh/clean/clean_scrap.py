import pandas as pd
import json

columns_to_match = [
    "first_name",
    "last_name",
    "phone_number",
    "zip_code",
    "address",
]


def clean_scrap(json_path, columns_path):

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


def match_scrap(scrap, columns):
    df = clean_scrap(scrap, columns)[columns_to_match]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    return df
