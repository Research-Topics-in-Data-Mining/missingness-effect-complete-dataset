from sklearn import metrics
from src.preprocess import read_data
from src.missing_data import append_metrics_per_repetition, metric_per_missingness_config
from sklearn.model_selection import train_test_split
from src.model import train
import pandas as pd
from pyampute.exploration.md_patterns import mdPatterns
from pyampute import *


# This function from pyampute plots the patterns of missingness it notices.
# Maybe we can use it on an amputated data set.
# mdp = mdPatterns()
# mypatterns = mdp.get_patterns(X_amputated)
# print(mypatterns)

# This is code for dropping the rows with missing values. We might need it.
# print(X.shape, y.shape)
# temp_data_set = pd.concat([X_amputated1, y], axis=1)
# temp_data_set = temp_data_set.dropna(axis=1)
# # print(temp_data_set)
# X_dropped_miss = temp_data_set.loc[:, "radius":"fractal_dimension"]
# y_dropped_miss = temp_data_set.loc[:, "diagnosis"]
# print(X_dropped_miss.shape, y_dropped_miss.shape)


X, y = read_data("./data/data.csv")

# Smoothness feature.
c1 = 4
c1_name = "smoothness"
# Symmetry feature.
c2 = 8
c2_name = "symmetry"
# Mean of the complete data set.
x_bar_true = X.iloc[:, c1].mean()
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=42,
                                                    stratify=y,
                                                    train_size=0.7)
rf = train(X_train, y_train)
# Accuracy with RF on the complete data set.
acc_true = rf.score(X_test, y_test)

# Monte Carlo simulation.
percentages = [0, 10, 20]

for mcar_p in percentages:
    for mar_p in percentages:
        for mnar_p in percentages:
            
            # So far we have a unique configuration: a% MCAR, b% MAR, c% MNAR.
            # We are not interested in this case, since it is exactly the complete data set.
            if mcar_p == 0 and mar_p == 0 and mnar_p == 0:
                continue
            # print("mcar, mar, mnar", mcar_p, mar_p, mnar_p)
            
            metrics_df = pd.DataFrame(columns = ["mean", "bias", "CI", "miss_percent", "std", "accuracy"])
            for rep in range(0, 1000):
                
                prop = mcar_p + mar_p + mnar_p
                pattern0 = {"incomplete_vars": [c1], "mechanism": "MCAR", "freq": mcar_p / prop}
                pattern1 = {"incomplete_vars": [c1], "mechanism": "MAR", "weights": {c2: 1}, "freq": mar_p / prop}
                pattern2 = {"incomplete_vars": [c1], "mechanism": "MNAR", "freq": mnar_p / prop}
                patterns = []
                # If percentage is greater than 0, include the pattern.
                if mcar_p != 0:
                    patterns.append(pattern0)
                if mar_p != 0:
                    patterns.append(pattern1)
                if mnar_p != 0:
                    patterns.append(pattern2)
                ma = MultivariateAmputation(prop=prop, patterns=patterns)
                X_amputated = ma.fit_transform(X)
                
                # This is the column from the data frame where all amputation was done.
                df_column = X_amputated.iloc[:, c1]
                # Here I chose to drop the column with missing values from both X_train and X_test.
                # If needed, we can change what to drop, or impute.
                X_train, X_test, y_train, y_test = train_test_split(X_amputated.drop([c1_name], axis=1), y,
                                                    random_state=42,
                                                    stratify=y,
                                                    train_size=0.7,
                                                    test_size=0.3)
                rf = train(X_train, y_train)
                acc = rf.score(X_test, y_test)
                # These are metrics computed per repetition. There are L=1000 repetitions, so metrics_df can have a maximum of L rows.
                # All L repetitions have the same percentages of missing patterns.
                metrics_df = append_metrics_per_repetition(metrics_df=metrics_df, df_column=df_column, acc=acc, x_bar_true=x_bar_true)
                print(metrics_df.shape)
            
            # So far we have 1000 repetitions of amputated data sets with the same configuration: a% MCAR, b% MAR, c% MNAR.
            # The column corresponds to the confidence intervals from metrics_df.
            df_column = metrics_df.iloc[:, 2]
            # This metric is computed for L repetitions of CIs.
            metric_per_missingness_config(df_column=df_column, x_bar_true=x_bar_true)