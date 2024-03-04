import pandas as pd


def clean_impact(data):
    data_list = []
    record = {"npi": None, "name": None, "address": None, "speciality": []}

    with open(data, "r") as file:
        for row in file:
            cols = row.split("\t")

            if cols[0] == "00":
                if record["npi"] is not None:
                    data_list.append(record)

                # Reset record for a new entry
                record = {
                    "npi": int(cols[1]),
                    "name": cols[3].strip(),
                    "address": None,
                    "speciality": [],
                }
            elif cols[0] == "10":
                record["address"] = cols[3].strip()
            elif cols[0] == "20":
                record["speciality"].append(cols[4].strip())

    # Check if the last record is non-empty and append it to the list
    if record["npi"] is not None:
        data_list.append(record)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Separate name (to have last_name and first_name)
    df[["last_name", "first_name"]] = df["name"].str.extract(r"(\S+)\s+([\w\s]+)")

    # Separate address (to have city, state, zip-code)
    df[["address", "city", "state", "zip_code"]] = df["address"].str.extract(
        r"(.+?)\s+([A-Z]+)\s+([A-Z]{2})\s+(\d+)"
    )

    df.drop_duplicates(subset="npi", keep="first", inplace=True)
    df.drop(columns="name", inplace=True)
    df["zip_code"] = df["zip_code"].str[:5]
    df = df[df["zip_code"].str.len() == 5]

    return df
