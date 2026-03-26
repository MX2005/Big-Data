

import sys
from pathlib import Path
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <input_csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: file not found -> {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)

    plt.figure(figsize=(20, 6))

    # Plot 1: Histogram of crimes by hour
    plt.subplot(1, 3, 1)
    if "Hour" in df.columns:
        sns.histplot(data=df, x="Hour", bins=24, kde=True)
        plt.title("Crimes by Hour")
        plt.xlabel("Hour")
        plt.ylabel("Frequency")
    else:
        plt.text(0.5, 0.5, "Hour column not found", ha="center", va="center")
        plt.title("Crimes by Hour")

    # Plot 2: Countplot of arrests
    plt.subplot(1, 3, 2)
    if "Arrest" in df.columns:
        sns.countplot(data=df, x="Arrest")
        plt.title("Arrest Distribution")
        plt.xlabel("Arrest")
        plt.ylabel("Count")
    else:
        plt.text(0.5, 0.5, "Arrest column not found", ha="center", va="center")
        plt.title("Arrest Distribution")

    # Plot 3: Correlation heatmap
    plt.subplot(1, 3, 3)
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    if not numeric_df.empty:
        corr_matrix = numeric_df.corr(numeric_only=True)
        sns.heatmap(corr_matrix, cmap="coolwarm", center=0)
        plt.title("Correlation Heatmap")
    else:
        plt.text(0.5, 0.5, "No numeric columns", ha="center", va="center")
        plt.title("Correlation Heatmap")

    plt.tight_layout()
    plt.savefig("summary_plot.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("Visualization saved as summary_plot.png")

    subprocess.run(["python", "cluster.py", str(input_path)], check=True)


if __name__ == "__main__":
    main()