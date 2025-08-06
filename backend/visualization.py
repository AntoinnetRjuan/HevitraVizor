import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram(df, column):
    plt.figure(figsize=(8, 5))
    sns.histplot(df[column].dropna(), kde=True, color="#1891EE")
    plt.title(f"Histogram of {column}", fontsize=14)
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()