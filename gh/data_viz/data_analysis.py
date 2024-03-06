import pandas as pd


def merge_data_visualization():
    """
    Generates the dataframe used for visualizations

    Returns: dataframe
    """
    # Load data from linkage
    df_merge = pd.read_csv("gh/merge.csv")
    df_scrap = pd.read_csv("gh/scrap.csv")

    # Merge the df_merge and the df_scrape data with 'first_name','last_name','phone_number'
    df = pd.merge(
        df_merge, df_scrap, how="left", on=["first_name", "last_name", "phone_number"]
    )

    # Only keep unique providers/drop duplicate
    df.drop_duplicates(
        subset=["first_name", "last_name", "type"], keep="first", inplace=True
    )

    # Only consider primary care providers and specialist (if they do not have first name they are institutions).
    df = df[df["first_name"].notna()]

    # Not consider unusual situations (institutions with first name)
    total_count = len(df)
    type_counts = df["type"].value_counts()
    filtered_types = type_counts[type_counts / total_count >= 0.01].index
    df = df[df["type"].isin(filtered_types)]

    return df


def get_matches_percentage_data(df, analysis_column):
    """
    Helper funtion to calculate the percentage of match and non_match for a given
    analysis column(subgroup) of the dataset to be analyze.

    Inputs:
    df(dataframe): used the merge and clean dataframe for vizulizacion
    analysis_column(str): the name of the column used to create the especial visualization.

    Returns: dataframe
    """

    list_of_tuples = []

    for observation in df[analysis_column].unique():
        # total for each provider type
        total = df.loc[df[analysis_column] == observation].shape[0]
        df_provider = df.loc[df[analysis_column] == observation]
        # Match / Non-Match (if have an 'npi' it matches)
        num_match = df_provider["npi"].count()
        num_nonmatch = df_provider["npi"].isna().sum()
        percentage_match = num_match / total
        percentage_nonmatch = num_nonmatch / total

        list_of_tuples.append(
            (
                observation,
                total,
                num_match,
                num_nonmatch,
                percentage_match,
                percentage_nonmatch,
            )
        )

    # sorted descending by Total
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1])

    data = pd.DataFrame(
        list_of_tuples,
        columns=[
            analysis_column,
            "Total",
            "Match",
            "Non-Match",
            "Percentage Match",
            "Percentage Non-Match",
        ],
    )
    return data
