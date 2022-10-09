from typing import Tuple

import pandas as pd


LABEL = "diagnosis"
NON_FEATURE_COLS = [LABEL, "id"]


def read_data(path="") -> Tuple[pd.Series, pd.Series]:
    """
    Read CSV and return X and y.
    """
    df = pd.read_csv(path)

    df = preprocess_df(df)

    describe_df(df)

    feature_cols = set(df.columns) - set(NON_FEATURE_COLS)
    X = df[df.columns.intersection(feature_cols)]
    y = df.loc[:, LABEL]

    return X, y


def describe_df(df: pd.DataFrame):
    print("DataFrame shape:", df.shape)
    print("Label distribution:")
    print(df[LABEL].value_counts(normalize=True))


def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    initial_n_cols = df.shape[1]
    # drop unnamed column that appeared
    df = df[df.columns[:-1]]
    # drop features regarding dimensions that should not be used.
    df = df.iloc[:, :12]

    mapping = {'M': 1, 'B': 0}
    df = df.replace({'diagnosis': mapping})

    processed_n_cols = df.shape[1]

    print(f"Dropping {initial_n_cols - processed_n_cols} columns...")

    return df
