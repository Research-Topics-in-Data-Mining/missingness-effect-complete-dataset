import pandas as pd
import statsmodels.api as sm
import seaborn as sns
from matplotlib import pyplot as plt

from src.preprocess import read_data
from src.visualization import plot_distribution, plot_qqplot, plot_correlation_matrix, plot_confusion_matrix, plot_feature_importance

from sklearn.model_selection import train_test_split
from src.model import train
from sklearn.metrics import classification_report

X, y = read_data("./data/data.csv")

# Plots for each feature the corresponding qq plot.
# Comment plt.show() in plot_qqplot function before saving as .svg.
for col in X:
    plot_qqplot(X[col])
    # plt.savefig("qq_plot_" + str(col) + ".svg", bbox_inches='tight')
plt.clf()

# Plots for each feature the corresponding distribution plot.
# Comment plt.show() in plot_distribution function before saving as .svg.
for col in X:
    plot_distribution(X[col])
    # plt.savefig("distr_plot_" + str(col) + ".svg", bbox_inches='tight')
plt.clf()

# Plots the correlation matrix for the features.
# Comment plt.show() in plot_correlation_matrix function before saving as .svg.
plot_correlation_matrix(X)
# plt.savefig("corr_matrix" + ".svg", bbox_inches='tight')
plt.clf()

print(X.mean())

X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=42,
                                                    stratify=y,
                                                    train_size=0.7)
rf = train(X_train, y_train)

pred = rf.predict(X_test)
print(classification_report(y_test, pred))
# Plots the confusion matrix for RF.
# Comment plt.show() in plot_confusion_matrix function before saving as .svg.
plot_confusion_matrix(y_test, pred, [0, 1])
# plt.savefig("conf_matrix" + ".svg", bbox_inches='tight')
plt.clf()

feature_scores = pd.Series(rf["rf"].feature_importances_, index=X_train.columns).sort_values(ascending=False)
print(feature_scores)
# Plots the confusion matrix for RF.
# Comment plt.show() in plot_confusion_matrix function before saving as .svg.
plot_feature_importance(feature_scores)
# plt.savefig("feature_imp" + ".svg", bbox_inches='tight')
plt.clf()