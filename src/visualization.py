import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


matplotlib.rcParams['figure.figsize'] = (20, 10)
matplotlib.style.use('ggplot')


def plot_feature_importance(feature_scores):
    plt.figure(dpi=120)
    ax = sns.barplot(x=feature_scores, y=feature_scores.index)
    ax.set_title("Visualize feature scores of the features")
    ax.set_yticklabels(feature_scores.index)
    ax.set_xlabel("Feature importance score")
    ax.set_ylabel("Features")
    plt.show()


def plot_correlation_matrix(df):
    corr_df = df.corr()
    sns.heatmap(corr_df, annot=True)
    plt.show()


def plot_distribution(df_column):
    sns.displot(df_column)
    plt.show()
