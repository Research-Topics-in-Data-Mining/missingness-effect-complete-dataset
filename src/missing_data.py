import numpy as np
import pandas as pd
from .md_utils import *
import torch
from scipy.stats import t
from typing import Any, List

def cl(df: pd.DataFrame) ->List:
    cls = []
    for col in df:
        m = df[col].mean() 
        s = df[col].std() 
        dof = len(df[col])-1 
        confidence = 0.95
        t_crit = np.abs(t.ppf((1-confidence)/2,dof))
        confidence_interval = (m-s*t_crit/np.sqrt(len(df[col])), m+s*t_crit/np.sqrt(len(df[col])))
        cls.append(confidence_interval)
    #print(cls)
    return cls


def cr(df: pd.DataFrame, means: pd.Series, missingness: str, perc: float, n: int = 1000):
    sum = [0 for x in range(len(means))]
    for i in range(n):
        amputed_df = get_missing_df(df, perc, missingness)
        amputed_cl = cl(amputed_df)
        j = 0
        for m in means:
            if m >= amputed_cl[j][0] and m <= amputed_cl[j][1]:
                sum[j] += 1
            j += 1
    return [x/n for x in sum]


def get_missing_df(X, p_miss, mecha):
    X_values = produce_NA(X.to_numpy(), p_miss=p_miss, mecha=mecha)["X_incomp"]
    return pd.DataFrame(X_values.tolist(), columns=X.columns)


def apply_metrics(complete_df: pd.DataFrame, missing_df: pd.DataFrame, missingness: str = "MCAR", perc: float = 0.05) -> pd.DataFrame:
    metrics = pd.DataFrame(columns = complete_df.columns)
    # mean
    metrics = metrics.append(complete_df.mean(), ignore_index=True)
    metrics = metrics.append(missing_df.mean(), ignore_index=True)
    # bias
    bias = abs(missing_df.mean()-complete_df.mean())
    metrics = metrics.append(bias, ignore_index=True)
    # confidence interval
    metrics.loc[len(metrics)] = cl(missing_df)
    # coverage rate
    metrics.loc[len(metrics)] = cr(complete_df, complete_df.mean(), missingness, perc)

    metrics.rename(index={0: "Real Mean", 1: "Predicted Mean", 2: "Bias", 3: "Confidence Interval", 4: "Coverage Rate"}, inplace=True)

    return metrics

# See https://rmisstastic.netlify.app/how-to/python/generate_html/how%20to%20generate%20missing%20values for reference
# Function produce_NA for generating missing values ------------------------------------------------------
def produce_NA(X, p_miss, mecha="MCAR", opt=None, q=None):
    """
    Generate missing values for specifics missing-data mechanism and proportion of missing values. 
    
    Parameters
    ----------
    X : torch.DoubleTensor or np.ndarray, shape (n, d)
        Data for which missing values will be simulated.
        If a numpy array is provided, it will be converted to a pytorch tensor.
    p_miss : float
        Proportion of missing values to generate for variables which will have missing values.
    mecha : str, 
            Indicates the missing-data mechanism to be used. "MCAR" by default, "MAR", "MNAR" or "MNARsmask"
    opt: str, 
         For mecha = "MNAR", it indicates how the missing-data mechanism is generated: using a logistic regression ("logistic"), quantile censorship ("quantile") or logistic regression for generating a self-masked MNAR mechanism ("selfmasked").
    p_obs : float
            If mecha = "MAR", or mecha = "MNAR" with opt = "logistic" or "quanti", proportion of variables with *no* missing values that will be used for the logistic masking model.
    q : float
        If mecha = "MNAR" and opt = "quanti", quantile level at which the cuts should occur.
    
    Returns
    ----------
    A dictionnary containing:
    'X_init': the initial data matrix.
    'X_incomp': the data with the generated missing values.
    'mask': a matrix indexing the generated missing values.s
    """
    
    p_obs = 1-p_miss
    to_torch = torch.is_tensor(X) ## output a pytorch tensor, or a numpy array
    if not to_torch:
        X = X.astype(np.float32)
        X = torch.from_numpy(X)
    
    if mecha == "MAR":
        mask = MAR_mask(X, p_miss, p_obs).double()
    elif mecha == "MNAR" and opt == "logistic":
        mask = MNAR_mask_logistic(X, p_miss, p_obs).double()
    elif mecha == "MNAR" and opt == "quantile":
        mask = MNAR_mask_quantiles(X, p_miss, q, 1-p_obs).double()
    elif mecha == "MNAR" and opt == "selfmasked":
        mask = MNAR_self_mask_logistic(X, p_miss).double()
    else:
        mask = (torch.rand(X.shape) < p_miss).double()
    
    X_nas = X.clone()
    X_nas[mask.bool()] = np.nan
    
    return {'X_init': X.double(), 'X_incomp': X_nas.double(), 'mask': mask}