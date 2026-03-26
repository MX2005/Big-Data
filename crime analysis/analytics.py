




















from __future__ import annotations

import calendar
import sys
from pathlib import Path
import subprocess

import pandas as pd

MIN_CASES_FOR_RATE = 500


def indicator_mask(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)

    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").fillna(0).astype(float) > 0

    normalized = series.astype(str).str.strip().str.lower()
    return normalized.isin({"true", "1", "yes"})


def indicator_total(series: pd.Series) -> int:
    return int(indicator_mask(series).sum())


def indicator_mean(series: pd.Series) -> float:
    return float(indicator_mask(series).mean())


def category_counts(df: pd.DataFrame, raw_column: str, prefix: str) -> pd.Series:
    if raw_column in df.columns:
        return df[raw_column].dropna().astype(str).value_counts()

    prefixed_columns = [column for column in df.columns if column.startswith(prefix)]
    if not prefixed_columns:
        return pd.Series(dtype="int64")

    counts = {
        column[len(prefix):]: indicator_total(df[column])
        for column in prefixed_columns
    }
    return pd.Series(counts, dtype="int64").sort_values(ascending=False)


def crime_arrest_rates(
    df: pd.DataFrame, minimum_cases: int = MIN_CASES_FOR_RATE
) -> list[tuple[str, int, float]]:
    if "Arrest" not in df.columns:
        return []

    if "Primary Type" in df.columns:
        grouped = (
            df.groupby("Primary Type", dropna=True)["Arrest"]
            .agg(["count", lambda values: indicator_mean(values)])
            .rename(columns={"<lambda_0>": "arrest_rate"})
        )
        filtered = grouped[grouped["count"] >= minimum_cases]
        return sorted(
            (
                (index, int(row["count"]), float(row["arrest_rate"]))
                for index, row in filtered.iterrows()
            ),
            key=lambda item: item[2],
            reverse=True,
        )

    prefixed_columns = [column for column in df.columns if column.startswith("Crime_")]
    rates: list[tuple[str, int, float]] = []
    arrest_indicator = indicator_mask(df["Arrest"])

    for column in prefixed_columns:
        mask = indicator_mask(df[column])
        count = int(mask.sum())
        if count < minimum_cases:
            continue
        rate = float(arrest_indicator[mask].mean())
        rates.append((column[len("Crime_"):], count, rate))

    return sorted(rates, key=lambda item: item[2], reverse=True)


def build_insights(df: pd.DataFrame) -> list[str]:
    total_rows = len(df)
    insights: list[str] = []

    crime_counts = category_counts(df, "Primary Type", "Crime_")
    if not crime_counts.empty and total_rows:
        top_crime = crime_counts.index[0]
        top_crime_count = int(crime_counts.iloc[0])
        first_sentence = (
            f"The most frequent crime in the dataset is {top_crime}, with "
            f"{top_crime_count:,} incidents out of {total_rows:,} total records "
            f"({top_crime_count / total_rows:.2%})."
        )

        if len(crime_counts) > 1:
            second_crime = crime_counts.index[1]
            second_crime_count = int(crime_counts.iloc[1])
            first_sentence += (
                f" The second most common category is {second_crime} with "
                f"{second_crime_count:,} incidents ({second_crime_count / total_rows:.2%})."
            )

        insights.append(first_sentence)

    location_counts = category_counts(df, "Location_Group", "Loc_")
    time_parts: list[str] = []

    if not location_counts.empty and total_rows:
        top_location = location_counts.index[0]
        top_location_count = int(location_counts.iloc[0])
        time_parts.append(
            f"{top_location} locations contain the largest share of incidents, with "
            f"{top_location_count:,} records ({top_location_count / total_rows:.2%})"
        )

    if "Hour" in df.columns and total_rows:
        top_hour = int(pd.to_numeric(df["Hour"], errors="coerce").mode().iloc[0])
        top_hour_count = int((pd.to_numeric(df["Hour"], errors="coerce") == top_hour).sum())
        time_parts.append(
            f"the busiest hour is {top_hour:02d}:00, when {top_hour_count:,} incidents were recorded"
        )

    if "DayOfWeek" in df.columns and total_rows:
        top_day_index = int(pd.to_numeric(df["DayOfWeek"], errors="coerce").mode().iloc[0])
        top_day_count = int(
            (pd.to_numeric(df["DayOfWeek"], errors="coerce") == top_day_index).sum()
        )
        day_name = calendar.day_name[top_day_index]
        time_parts.append(
            f"{day_name} is the peak day with {top_day_count:,} incidents ({top_day_count / total_rows:.2%})"
        )

    if time_parts:
        insights.append(". ".join(part.capitalize() for part in time_parts) + ".")

    arrest_rates = crime_arrest_rates(df, minimum_cases=MIN_CASES_FOR_RATE)
    if arrest_rates and "Arrest" in df.columns:
        overall_arrest_rate = indicator_mean(df["Arrest"])
        top_arrest_crime, case_count, arrest_rate = arrest_rates[0]
        insights.append(
            f"The overall arrest rate in the dataset is {overall_arrest_rate:.2%}. "
            f"Among crime categories with at least {MIN_CASES_FOR_RATE:,} incidents, {top_arrest_crime} "
            f"has the highest arrest rate at {arrest_rate:.2%} across {case_count:,} cases."
        )
    elif "Community Area" in df.columns and total_rows:
        top_area = df["Community Area"].value_counts().idxmax()
        top_area_count = int(df["Community Area"].value_counts().max())
        insights.append(
            f"Community Area {top_area} appears most often in the cleaned data, with "
            f"{top_area_count:,} incidents ({top_area_count / total_rows:.2%} of the dataset)."
        )

    while len(insights) < 3:
        insights.append("The dataset contains enough cleaned fields for additional analysis if needed.")

    return insights[:3]


def write_insights(insights: list[str], output_directory: Path) -> None:
    for index, insight in enumerate(insights, start=1):
        output_path = output_directory / f"insight{index}.txt"
        output_path.write_text(insight + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python analytics.py <input_csv>", file=sys.stderr)
        return 1

    input_path = Path(argv[1]).resolve()

    if not input_path.exists():
        print(f"Error: file not found -> {input_path}", file=sys.stderr)
        return 1

    df = pd.read_csv(input_path)
    insights = build_insights(df)
    write_insights(insights, input_path.parent)

    subprocess.run(["python", "visualize.py", str(input_path)], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))