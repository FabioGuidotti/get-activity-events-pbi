import pandas as pd


def json_to_df(json_file):

    list_organize = []
    for sublista in json_file:
        list_organize.extend(sublista)

    df = pd.DataFrame(list_organize)

    return df
