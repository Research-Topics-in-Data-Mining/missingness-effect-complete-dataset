from unittest import skip
import numpy as np
import pandas as pd
from .md_utils import *
from scipy.stats import t
import scipy.stats as st
import statistics
import statsmodels.stats.api as sms

# All these functions take a data frame column.
# Metrics are applied on a data frame column.


def confidence_interval(df_column: pd.Series) -> tuple:
    # The total number of values in the column does not consider NaNs.
    n = df_column.size - df_column.isna().sum()
    m = df_column.mean()
    s = df_column.std()
    dof = n - 1
    confidence = 0.95
    t_crit = np.abs(t.ppf((1.0 - confidence) / 2.0, dof))
    confidence_interval = (m - t_crit * s / np.sqrt(n),
                           m + t_crit * s / np.sqrt(n))
    return confidence_interval


def coverage_rate(df_column: pd.Series, x_bar_true: float) -> float:
    L = df_column.size
    sum = 0
    for i in range(L):
        if df_column[i][0] <= x_bar_true and x_bar_true <= df_column[i][1]:
            sum += 1
    return sum / L


# Computes the metrics we use per repetition in Monte Carlo.
# The metrics are: mean, bias, confidence interval, missingness percentage,
# standard deviation and accuracy (received as parameter).
def append_metrics_per_repetition(metrics_df: pd.DataFrame, df_column: pd.Series, acc_a: float, acc_b: float, x_bar_true: float, x_median_true: float, x_iqr_true: float, x_std_true: float) -> pd.DataFrame:
    x_bar = df_column.mean()
    x_median = df_column.median()
    q1 = df_column.quantile(0.25)
    q3 = df_column.quantile(0.75)
    iqr = q3 - q1
    std = df_column.std()

    bias = x_bar - x_bar_true
    bias_median = x_median - x_median_true
    bias_iqr = iqr - x_iqr_true
    bias_std = std - x_std_true

    bias_perc = np.abs(bias) / x_bar_true
    bias_median_perc = np.abs(bias_median) / x_median_true    
    bias_iqr_perc = np.abs(bias_iqr) / x_iqr_true

    conf_int = confidence_interval(df_column)
    miss_percent = df_column.isna().sum() / df_column.size
    
    series = pd.Series({"mean": x_bar, "bias": bias, "CI": conf_int,
                       "miss_percent": miss_percent, "std": std, 
                       "accuracy_a": acc_a, "accuracy_b": acc_b, 
                       "bias_perc": bias_perc, 
                       "median": x_median, "bias_median": bias_median, "bias_median_perc": bias_median_perc, 
                       "iqr": iqr, "bias_iqr": bias_iqr, "bias_iqr_perc": bias_iqr_perc, "bias_std": bias_std})
    return pd.concat([metrics_df, series.to_frame().T], ignore_index=True)


# Computes the metric we use per configuration, after the Monte Carlo
# repetitions.
# The metric is: coverage rate.
def metric_per_missingness_config(df_column: pd.Series, x_bar_true: float) -> int:
    return coverage_rate(df_column, x_bar_true)
