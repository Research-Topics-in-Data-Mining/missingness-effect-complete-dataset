import pandas as pd
import numpy as np

results_mean = pd.DataFrame(columns = ["mean_of_means", "mean_of_biases", "mean_of_miss_percent", "mean_of_std", "mean_of_accuracy_a", "mean_of_accuracy_b"])
results_std = pd.DataFrame(columns = ["std_of_means", "std_of_biases", "std_of_miss_percent", "std_of_std", "std_of_accuracy_a", "std_of_accuracy_b"])

dic_m = {}
dic_s = {}
pd_m = []

percentages = [0, 10, 20]
m_types = ["sigmoid-right", "sigmoid-left", "sigmoid-tail", "sigmoid-mid"]

for m_type in m_types:
    for i_mcar in percentages:
        for i_mar in percentages:
            for i_mnar in percentages:
                if i_mcar == 0 and i_mar == 0 and i_mnar == 0:
                    continue
                csv_name = "./csvs/" + str(m_type) + "/MCAR" + str(i_mcar) + "_" + "MAR" + str(i_mar) + "_" + "MNAR" + str(i_mnar) + ".csv"
                df = pd.read_csv(csv_name)
                
                #print(df.head(3))
                dffull = df.copy()
                N = dffull.shape[0]
                dffull['type'] = np.repeat([m_type], N)
                dffull['MCAR'] = np.repeat([i_mcar], N)
                dffull['MAR'] = np.repeat([i_mar], N)
                dffull['MNAR'] = np.repeat([i_mnar], N)
                #print(dffull.head(3))
                pd_m.append(dffull)            

                n = df.shape[1]
                # print(n, df.dtypes)
                m = [0] * (n - 1)
                s = [0] * (n - 1)
                idx = 0
                for i in range(0, n):
                    if i == 2:
                        continue
                    m[idx] = np.round(df.iloc[:, i].mean(),4)
                    s[idx] = np.round(df.iloc[:, i].std(),4)
                    idx += 1

                series_m = pd.Series({"mean_of_means": m[0], "mean_of_biases": m[1], "mean_of_miss_percent": m[2], "mean_of_std": m[3], "mean_of_accuracy_a": m[4], "mean_of_accuracy_b": m[5], "mean_of_percent_bias": m[6],
                "mean_of_medians": m[7], "mean_of_bias_medians": m[8],
                "mean_of_percent_bias_median": m[9], 
                "mean_of_iqr": m[10], "mean_of_bias_iqr": m[11],
                "mean_of_percent_bias_iqr": m[12], "mean_of_bias_std": m[13]})
                results_mean = pd.concat([results_mean, series_m.to_frame().T], ignore_index=True)
                series_s = pd.Series({"std_of_means": s[0], "std_of_biases": s[1], "std_of_miss_percent": s[2], "std_of_std": s[3], "std_of_accuracy_a": s[4], "std_of_accuracy_b": s[5], "std_of_percent_bias": s[6],
                "std_of_medians": s[7], "std_of_bias_medians": s[8],
                "std_of_percent_bias_median": s[9], 
                "std_of_iqr": s[10], "std_of_bias_iqr": s[11],
                "std_of_percent_bias_iqr": s[12], "std_of_bias_std": s[13]})
                results_std = pd.concat([results_std, series_s.to_frame().T], ignore_index=True)

                tup = (m_type, i_mcar, i_mar, i_mnar)
                dic_m[tup] = m
                dic_s[tup] = s

pd_mm = pd.concat(pd_m)
pd_mm.to_csv("./csvs/final/values_all.csv", index=False)

pd_m = pd.DataFrame.from_dict(dic_m, orient='index')
pd_m_wide = pd_m.reset_index()
pd_m_index = pd.DataFrame(pd_m_wide['index'].tolist(), index=pd_m_wide.index, columns=['type', 'MCAR', 'MAR', 'MNAR'])
pd_m = result = pd.concat([pd_m_index, pd_m.reset_index(drop=True)], axis=1)
pd_m = pd_m.rename(columns={0:'mean', 1:'bias', 2:'miss_percent', 3:'std', 4:'accuracy_a', 5:'accuracy_b', 6:'percent_bias', 7:'median', 8:'bias_median', 9:'percent_bias_median', 10:'iqr', 11:'bias_iqr', 12:'percent_bias_iqr', 13:'bias_std'})

pd_m.to_csv("./csvs/final/averages.csv", index=False)

pd_s = pd.DataFrame.from_dict(dic_s, orient='index')
pd_s_wide = pd_s.reset_index()
pd_s_index = pd.DataFrame(pd_s_wide['index'].tolist(), index=pd_s_wide.index, columns=['type', 'MCAR', 'MAR', 'MNAR'])
pd_s = result = pd.concat([pd_s_index, pd_s.reset_index(drop=True)], axis=1)
pd_s = pd_s.rename(columns={0:'mean', 1:'bias', 2:'miss_percent', 3:'std', 4:'accuracy_a', 5:'accuracy_b', 6:'percent_bias', 7:'median', 8:'bias_median', 9:'percent_bias_median', 10:'iqr', 11:'bias_iqr', 12:'percent_bias_iqr', 13:'bias_std'})

pd_s.to_csv("./csvs/final/stds.csv", index=False)


