import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from src.missing_data import produce_NA
from sklearn.metrics import confusion_matrix


matplotlib.rcParams['figure.dpi'] = 110
# matplotlib.style.use('fivethirtyeight')
style = "fivethirtyeight"
plt.style.use(style)

# sns.set_theme()


def plot_feature_importance(feature_scores):
    with plt.style.context(style):
        ax = sns.barplot(x=feature_scores, y=feature_scores.index)
        ax.set_title("Visualize feature scores of the features")
        ax.set_yticklabels(feature_scores.index)
        ax.set_xlabel("Feature importance score")
        ax.set_ylabel("Features")
        plt.show()


def plot_correlation_matrix(df):
    corr_df = df.corr()

    with plt.style.context(style):
        sns.heatmap(corr_df, annot=True, cmap="rocket", fmt=".1f")
        plt.show()


def plot_distribution(df_column):
    with plt.style.context(style):
        sns.displot(df_column, kde=True)
        plt.show()


def plot_multiple_distribution_grid(df, columns):
    with plt.style.context(style):
        plt.figure(figsize=(16, 12))
        for i, column in enumerate(columns, 1):
            plt.subplot(3,3,i)
            sns.histplot(df[column], kde=True)
        plt.show()

def plot_pairplot(df, columns):
    with plt.style.context(style):
        sns.pairplot(df, vars=columns)
        plt.show()

def plot_boxplot(df):
    with plt.style.context(style):
        sns.boxplot(data=df)
        plt.show()


def plot_missing_data(df):
    with plt.style.context(style):
        sns.heatmap(df.isnull(), cbar=False)
        plt.show()

def plot_confusion_matrix(y_true, y_pred, labels):
    with plt.style.context(style):
        sns.heatmap(confusion_matrix(y_true, y_pred, labels=labels), annot=True, fmt="d")
        plt.show()
