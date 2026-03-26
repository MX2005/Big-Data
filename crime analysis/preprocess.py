

import sys
from pathlib import Path
import subprocess
import pandas as pd
import numpy as np


def group_location_final(loc):
    if pd.isnull(loc):
        return "Other"
    loc = loc.upper()
    if any(word in loc for word in [
        "RESIDENCE", "APARTMENT", "HOUSE", "HOME", "PORCH",
        "YARD", "GARAGE", "BASEMENT", "ROOMING", "CHA APARTMENT",
        "RESIDENTIAL"
    ]):
        return "Residential"
    elif any(word in loc for word in [
        "STORE", "SHOP", "RETAIL", "RESTAURANT", "BAR", "TAVERN",
        "BANK", "OFFICE", "BUSINESS", "HOTEL", "MOTEL",
        "GAS STATION", "DRUG STORE", "CURRENCY EXCHANGE",
        "DEALERSHIP", "LAUNDROMAT", "CLEANERS", "PAWN"
    ]):
        return "Commercial"
    elif any(word in loc for word in [
        "CTA", "TRAIN", "BUS", "PLATFORM", "TAXI",
        "VEHICLE", "AIRPORT", "AIRCRAFT", "BOAT",
        "TRUCK", "HIGHWAY", "EXPRESSWAY", "RAILROAD",
        "SUBWAY"
    ]):
        return "Transportation"
    elif any(word in loc for word in [
        "SCHOOL", "COLLEGE", "UNIVERSITY",
        "HOSPITAL", "MEDICAL", "POLICE",
        "JAIL", "GOVERNMENT", "CHURCH",
        "FACILITY", "LIBRARY", "FIRE STATION",
        "DAY CARE"
    ]):
        return "Institution"
    elif any(word in loc for word in [
        "STREET", "SIDEWALK", "ALLEY",
        "PARK", "LOT", "FOREST", "LAKE",
        "RIVER", "FIELD", "PRAIRIE",
        "BRIDGE", "DUMPSTER", "GANGWAY"
    ]):
        return "Public"
    else:
        return "Other"


def main():
    if len(sys.argv) != 2:
        print("Usage: python preprocess.py <input_csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: file not found -> {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)

    cols_to_drop = [
        "Unnamed: 0",
        "ID",
        "Case Number"
    ]

    df = df.drop(columns=cols_to_drop, errors="ignore")

    df = df.drop(columns=["X Coordinate", "Y Coordinate"], errors="ignore")

    df = df.drop(columns=["IUCR", "FBI Code"], errors="ignore")

    cat_cols = [
        "Date",
        "Block",
        "Primary Type",
        "Description",
        "Location Description",
        "Arrest",
        "Domestic",
        "Beat",
        "District",
        "Ward",
        "Community Area",
        "Year",
        "Updated On",
        "Location"
    ]

    existing_cat_cols = [col for col in cat_cols if col in df.columns]

    missing_percent_cat = df[existing_cat_cols].isnull().mean() * 100
    cols_with_missing_cat = missing_percent_cat[missing_percent_cat > 0].index.tolist()

    for col in cols_with_missing_cat:
        mode_value = df[col].mode()[0]
        df[col].fillna(mode_value, inplace=True)

    if "Community Area" in df.columns and "Latitude" in df.columns:
        df["Latitude"] = df.groupby("Community Area")["Latitude"].transform(
            lambda x: x.fillna(x.median())
        )

    if "Community Area" in df.columns and "Longitude" in df.columns:
        df["Longitude"] = df.groupby("Community Area")["Longitude"].transform(
            lambda x: x.fillna(x.median())
        )

    df = df.drop_duplicates()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%m/%d/%Y %I:%M:%S %p",
            errors="coerce"
        )

        df["Month"] = df["Date"].dt.month
        df["DayOfWeek"] = df["Date"].dt.dayofweek
        df["Hour"] = df["Date"].dt.hour

        df = df.drop(columns=["Date"], errors="ignore")

    if "Location Description" in df.columns:
        df["Location_Group"] = df["Location Description"].apply(group_location_final)

    df = pd.get_dummies(
        df,
        columns=["Location_Group", "Primary Type"],
        prefix=["Loc", "Crime"]
    )

    output_path = Path("data_preprocessed.csv")
    df.to_csv(output_path, index=False)

    print(f"Preprocessing complete. Saved to: {output_path.resolve()}")

    subprocess.run(["python", "analytics.py", str(output_path)], check=True)


if __name__ == "__main__":
    main()