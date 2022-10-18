import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("MCAR:0_MAR:20_MNAR:0")
print(df)
n = df.shape[0]
print("mean of means: ", df.iloc[:, 0].mean())
plt.scatter(range(0, n), df.iloc[:, 0])
plt.axhline(y=0.096360, color='r', linestyle='-')
plt.show()
plt.clf()

print("mean of biases: ", df.iloc[:, 1].mean())
plt.scatter(range(0, n), df.iloc[:, 1])
plt.axhline(y=0.0, color='r', linestyle='-')
plt.show()
plt.clf()

print("mean of misssingness percentages: ", df.iloc[:, 3].mean())
print("mean of standard deviations: ", df.iloc[:, 4].mean())

print("mean of accuracies: ", df.iloc[:, 5].mean())
plt.scatter(range(0, n), df.iloc[:, 5])
plt.axhline(y=0.94, color='r', linestyle='-')
plt.show()
plt.clf()