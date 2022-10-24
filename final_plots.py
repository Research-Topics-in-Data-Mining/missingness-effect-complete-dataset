import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.suggested_plots import *


results_mean = pd.DataFrame(columns = ["mean_of_means", "mean_of_biases", "mean_of_miss_percent", "mean_of_std", "mean_of_accuracy_a", "mean_of_accuracy_b"])
results_std = pd.DataFrame(columns = ["std_of_means", "std_of_biases", "std_of_miss_percent", "std_of_std", "std_of_accuracy_a", "std_of_accuracy_b"])

dic_m = {}
dic_s = {}

for i_mcar in [0, 10, 20]:
    for i_mar in [0, 10, 20]:
        for i_mnar in [0, 10, 20]:
            if i_mcar == 0 and i_mar == 0 and i_mnar == 0:
                continue
            csv_name = "./csvs/MCAR:" + str(i_mcar) + "_" + "MAR:" + str(i_mar) + "_" + "MNAR:" + str(i_mnar) + ".csv"
            df = pd.read_csv(csv_name)
            # print(df.head(3))
            n = df.shape[1]
            # print(n, df.dtypes)
            m = [0] * (n - 1)
            s = [0] * (n - 1)
            idx = 0
            for i in range(0, n):
                if i == 2:
                    continue
                m[idx] = df.iloc[:, i].mean()
                s[idx] = df.iloc[:, i].std()
                idx += 1
            # print(m)
            # print(s)

            series_m = pd.Series({"mean_of_means": m[0], "mean_of_biases": m[1], "mean_of_miss_percent": m[2], "mean_of_std": m[3], "mean_of_accuracy_a": m[4], "mean_of_accuracy_b": m[5]})
            results_mean = pd.concat([results_mean, series_m.to_frame().T], ignore_index=True)
            series_s = pd.Series({"std_of_means": s[0], "std_of_biases": s[1], "std_of_miss_percent": s[2], "std_of_std": s[3], "std_of_accuracy_a": s[4], "std_of_accuracy_b": s[5]})
            results_std = pd.concat([results_std, series_s.to_frame().T], ignore_index=True)

            tup = (i_mcar, i_mar, i_mnar)
            dic_m[tup] = m
            dic_s[tup] = s

# print(results_mean)
# print(dic_m)

txt_name = "./coverage_rates.txt"
df = pd.read_csv(txt_name, delim_whitespace=True)
df.drop(df.columns[[0]], axis = 1, inplace=True)
# print(df)

# Final plots

# print(results_mean.iloc[:, 0])

# barplot_type1(dic_m, dic_s, x_axis_miss_type="MNAR", legend_miss_type="MCAR", title_miss_type="MAR", percentage=20, column=0)

barplot_type3(dic_m)
