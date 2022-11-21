from sklearn import metrics
from src.preprocess import read_data
from src.missing_data import append_metrics_per_repetition, coverage_rate, metric_per_missingness_config
from sklearn.model_selection import train_test_split
from src.model import train
import pandas as pd
from pyampute.exploration.md_patterns import mdPatterns
from pyampute import *


# This function from pyampute plots the patterns of missingness it notices.
# Maybe we can use it on an amputed data set.
# mdp = mdPatterns()
# mypatterns = mdp.get_patterns(X_amputed)
# print(mypatterns)


def scheme_a(X, y, c1, ma):
    X_amputed = ma.fit_transform(X)
    df_column = X_amputed.iloc[:, c1]

    # Create a temporary dataset that is the concatenation of X_amputed and y.
    temp_data_set = pd.concat([X_amputed, y], axis=1)
    # Drop the rows with missing data.
    temp_data_set.dropna(inplace=True, axis=0)
    # Reset indices after dropping.
    temp_data_set.reset_index(inplace=True)
    # Split the temporary dataset into X_dropped_miss and y_dropped_miss.
    X_dropped_miss = temp_data_set.loc[:, "radius":"fractal_dimension"]
    y_dropped_miss = temp_data_set.loc[:, "diagnosis"]
    X_train, X_test, y_train, y_test = train_test_split(X_dropped_miss, y_dropped_miss,
                                        random_state=42,
                                        stratify=y_dropped_miss,
                                        train_size=0.7,
                                        test_size=0.3)
    rf = train(X_train, y_train)
    acc = rf.score(X_test, y_test)
    return df_column, acc


def scheme_b(X, y, ma):
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                        random_state=42,
                                        stratify=y,
                                        train_size=0.7,
                                        test_size=0.3)
    X_train_amputed = ma.fit_transform(X_train)
    # Create a temporary dataset that is the concatenation of X_train_amputed and y_train.
    temp_data_set = pd.concat([X_train_amputed, y_train], axis=1)
    # Drop the rows with missing data.
    temp_data_set.dropna(inplace=True, axis=0)
    # Reset indices after dropping.
    temp_data_set.reset_index(inplace=True)
    # Split the temporary dataset into X_train_dropped and y_train_dropped.
    X_train_dropped = temp_data_set.loc[:, "radius":"fractal_dimension"]
    y_train_dropped = temp_data_set.loc[:, "diagnosis"]
    rf = train(X_train_dropped, y_train_dropped)
    return rf.score(X_test, y_test)


X, y = read_data("./data/data.csv")

# Smoothness feature.
c1 = 4
c1_name = "smoothness"
# Symmetry feature.
c2 = 8
c2_name = "symmetry"

# Sample mean of the smoothness column from the complete data set.
x_bar_true = X.iloc[:, c1].mean()
x_median_true =X.iloc[:, c1].median()

# Sample std of the smoothness column from the complete data set.
std_true = X.iloc[:, c1].std()
q1 = X.iloc[:, c1].quantile(0.25)
q3 = X.iloc[:, c1].quantile(0.75)
iqr = q3 - q1
x_iqr_true = q3 - q1
skew_true= (3*(x_bar_true - x_median_true))/std_true

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=42,
                                                    stratify=y,
                                                    train_size=0.7,
                                                    test_size=0.3)
rf = train(X_train, y_train)
# Accuracy with RF on the complete data set.
acc_true = rf.score(X_test, y_test)
with open("true_metrics.txt", "w") as myfile:
    myfile.write("true sample mean: " + str(x_bar_true) + "\n")
    myfile.write("true sample std: " + str(std_true) + "\n")
    myfile.write("true accuracy: " + str(acc_true) + "\n")
    myfile.write("true sample median: " + str(x_median_true) + "\n")
    myfile.write("true sample iqr: " + str(x_iqr_true) + "\n")
    myfile.write("true skew: " + str(skew_true) + "\n")

# Monte Carlo simulation.
percentages = [0, 10, 20]
m_types = ["sigmoid-right", "sigmoid-left", "sigmoid-tail", "sigmoid-mid"]

for m_type in m_types: 
    for mcar_p in percentages:
        for mar_p in percentages:
            for mnar_p in percentages:
            
                # So far we have a unique configuration: a% MCAR, b% MAR, c% MNAR.
                # We are not interested in this case, since it is exactly the complete data set.
                if mcar_p == 0 and mar_p == 0 and mnar_p == 0:
                    continue
                # print("mcar, mar, mnar", mcar_p, mar_p, mnar_p)
            
                metrics_df = pd.DataFrame(columns = ["mean", "bias", "CI", "miss_percent", "std", "accuracy_a", "accuracy_b"])
            
                for rep in range(0, 2):
                
                    prop = mcar_p + mar_p + mnar_p
                    pattern0 = {"incomplete_vars": [c1], "mechanism": "MCAR", "freq": mcar_p / prop, "score_to_probability_func": m_type}
                    pattern1 = {"incomplete_vars": [c1], "mechanism": "MAR", "weights": {c2: 1}, "freq": mar_p / prop, "score_to_probability_func": m_type}
                    pattern2 = {"incomplete_vars": [c1], "mechanism": "MNAR", "freq": mnar_p / prop, "score_to_probability_func": m_type}
                    patterns = []
                
                    # If percentage is greater than 0, include the pattern.
                    if mcar_p != 0:
                        patterns.append(pattern0)
                    if mar_p != 0:
                        patterns.append(pattern1)
                    if mnar_p != 0:
                        patterns.append(pattern2)
                    ma = MultivariateAmputation(prop=prop, patterns=patterns)
                
                    # df_column is the column from X_amputed where all amputation was done. 
                    # We need it for computing the statistical metrics.
                    # acc_a is the accuracy of the model with the train-test scheme a.
                    df_column, acc_a = scheme_a(X, y, c1, ma)

                    # acc_a is the accuracy of the model with the train-test scheme b.
                    acc_b = scheme_b(X, y, ma)

                    # These are metrics computed per repetition. There are L=1000 
                    # repetitions, so metrics_df can have a maximum of L rows.
                    # All L repetitions have the same percentages of missing patterns.
                    metrics_df = append_metrics_per_repetition(metrics_df=metrics_df, df_column=df_column, acc_a=acc_a, acc_b=acc_b, x_bar_true=x_bar_true,x_median_true=x_median_true, 
                    x_iqr_true=x_iqr_true,x_std_true=std_true)
                    #print(metrics_df.shape)
            
                metrics_df.to_csv("./csvs/" + str(m_type) + "/MCAR" + str(mcar_p) + "_" + "MAR" + str(mar_p) + "_" + "MNAR" + str(mnar_p) + ".csv", index=False)
            
                # So far we have 1000 repetitions of amputed data sets with the same configuration: a% MCAR, b% MAR, c% MNAR.
                # The column corresponds to the confidence intervals from metrics_df.
                df_column = metrics_df.iloc[:, 2]
                # This metric is computed for L repetitions of CIs.
                cr = metric_per_missingness_config(df_column=df_column, x_bar_true=x_bar_true)
                with open("coverage_rates.txt", "a") as myfile:
                    myfile.write("MCAR" + str(mcar_p) + "_" + "MAR" + str(mar_p) + "_" + "MNAR" + str(mnar_p) + " " + str(cr) + "\n")