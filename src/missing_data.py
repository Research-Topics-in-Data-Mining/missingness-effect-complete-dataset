import numpy as np
import pandas as pd
from .md_utils import *
import torch
from scipy.stats import t
from typing import Any, List
from pyampute import *

# 
def get_missing_df(dataframe, p_miss, mechanism, columns):
    target_columns = []

    for col in columns:
        if col in dataframe.columns:
            target_columns.append([dataframe.columns.get_loc(col)])

    patterns = [{"incomplete_vars": target_columns, "mechanism": mechanism}]

    df_incomplete = MultivariateAmputation(prop=p_miss, patterns=patterns)
    return df_incomplete.fit_transform(dataframe)


def confidence_interval(df_column: pd.Series) -> tuple:
    n = df_column.size
    m = df_column.mean() 
    s = df_column.std() 
    dof = n - 1 
    confidence = 0.95
    t_crit = np.abs(t.ppf((1 - confidence) / 2, dof))
    confidence_interval = (m - t_crit * s / np.sqrt(n), m + s * t_crit / np.sqrt(n))
    return confidence_interval


def coverage_rate(df_column: pd.Series, x_bar_true: float) -> float:
    L = df_column.size
    sum = 0
    for i in range(L):
        if df_column[i][0] <= x_bar_true and x_bar_true <= df_column[i][1]:
            sum += 1
    return sum / L


def append_metrics_per_repetition(metrics_df: pd.DataFrame, df_column: pd.Series, acc: float, x_bar_true: float) -> pd.DataFrame:
    x_bar = df_column.mean()
    bias = x_bar - x_bar_true
    conf_int = confidence_interval(df_column)
    miss_percent = df_column.isna().sum() / df_column.size
    std = df_column.std()

    series = pd.Series({"mean": x_bar, "bias": bias, "CI": conf_int, "miss_percent": miss_percent, "std": std, "accuracy": acc})
    # print(series)
    return pd.concat([metrics_df, series.to_frame().T], ignore_index=True)


def metric_per_missingness_config(df_column: pd.Series, x_bar_true: float) -> int:
    return coverage_rate(df_column, x_bar_true)
