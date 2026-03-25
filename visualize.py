from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


HEATMAP_COLUMNS = [
    "Arrest",
    "Domestic",
    "District",
    "Ward",
    "Community Area",
    "Month",
    "DayOfWeek",
    "Hour",
]


def add_placeholder(axis: plt.Axes, title: str, message: str) -> None:
    axis.set_title(title)
    axis.text(0.5, 0.5, message, ha="center", va="center", wrap=True)
    axis.set_axis_off()


def plot_hour_distribution(df: pd.DataFrame, axis: plt.Axes) -> None:
    if "Hour" not in df.columns:
        add_placeholder(axis, "Crimes by Hour", "Column 'Hour' is not available.")
        return

    hours = pd.to_numeric(df["Hour"], errors="coerce").dropna()
    if hours.empty:
        add_placeholder(axis, "Crimes by Hour", "No valid hour values were found.")
        return

    sns.histplot(hours, bins=24, kde=True, color="skyblue", ax=axis)
    axis.set_title("Distribution of Crimes by Hour")
    axis.set_xlabel("Hour of the Day")
    axis.set_ylabel("Frequency")
    axis.grid(axis="y", alpha=0.3)


def plot_month_counts(df: pd.DataFrame, axis: plt.Axes) -> None:
    if "Month" not in df.columns:
        add_placeholder(axis, "Incidents by Month", "Column 'Month' is not available.")
        return

    months = pd.to_numeric(df["Month"], errors="coerce").dropna().astype(int)
    if months.empty:
        add_placeholder(axis, "Incidents by Month", "No valid month values were found.")
        return

    month_counts = (
        months.value_counts()
        .sort_index()
        .rename_axis("Month")
        .reset_index(name="Incidents")
    )

    sns.barplot(data=month_counts, x="Month", y="Incidents", color="#4c72b0", ax=axis)
    axis.set_title("Incident Counts by Month")
    axis.set_xlabel("Month")
    axis.set_ylabel("Number of Incidents")
    axis.grid(axis="y", alpha=0.3)


def plot_correlation_heatmap(df: pd.DataFrame, axis: plt.Axes) -> None:
    available_columns = [column for column in HEATMAP_COLUMNS if column in df.columns]
    if len(available_columns) < 2:
        add_placeholder(
            axis,
            "Feature Correlation Heatmap",
            "Not enough numeric columns were found for a correlation matrix.",
        )
        return

    numeric_df = df[available_columns].apply(pd.to_numeric, errors="coerce")
    corr_matrix = numeric_df.corr()

    sns.heatmap(corr_matrix, annot=True, cmap="RdBu", fmt=".2f", center=0, ax=axis)
    axis.set_title("Correlation Matrix of Crime Features")


def main(argv: list[str]) -> int:
    if len(argv) > 2:
        print("Usage: python visualize.py [input_csv]", file=sys.stderr)
        return 1

    input_path = Path(argv[1]) if len(argv) == 2 else Path("data_preprocessed.csv")
    input_path = input_path.resolve()

    if not input_path.exists():
        print(f"Error: input file '{input_path}' does not exist.", file=sys.stderr)
        return 1

    df = pd.read_csv(input_path)

    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(18, 14), constrained_layout=True)
    grid = fig.add_gridspec(2, 2, height_ratios=[1, 1.15])

    ax1 = fig.add_subplot(grid[0, 0])
    ax2 = fig.add_subplot(grid[0, 1])
    ax3 = fig.add_subplot(grid[1, :])

    plot_hour_distribution(df, ax1)
    plot_month_counts(df, ax2)
    plot_correlation_heatmap(df, ax3)

    fig.suptitle("Crime Dataset Summary Plots", fontsize=18, fontweight="bold")

    output_path = input_path.parent / "summary_plot.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved summary plot to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
