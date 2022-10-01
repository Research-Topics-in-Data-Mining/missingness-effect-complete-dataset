from typing import Tuple

import pandas as pd


LABEL = "diagnosis"
NON_FEATURE_COLS = [LABEL, "id"]


def read_data(path="") -> Tuple[pd.Series, pd.Series]:
    """
    Read CSV and return X and y.
    """
    df = pd.read_csv(path)
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
    pass
