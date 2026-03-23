import sys
import pandas as pd
import numpy as np
import subprocess

def group_location_final(loc):
    if pd.isnull(loc):
        return 'Other'
    loc = loc.upper()
    if any(word in loc for word in [
        'RESIDENCE', 'APARTMENT', 'HOUSE', 'HOME', 'PORCH',
        'YARD', 'GARAGE', 'BASEMENT', 'ROOMING', 'CHA APARTMENT',
        'RESIDENTIAL'
    ]):
        return 'Residential'
    elif any(word in loc for word in [
        'STORE', 'SHOP', 'RETAIL', 'RESTAURANT', 'BAR', 'TAVERN',
        'BANK', 'OFFICE', 'BUSINESS', 'HOTEL', 'MOTEL',
        'GAS STATION', 'DRUG STORE', 'CURRENCY EXCHANGE',
        'DEALERSHIP', 'LAUNDROMAT', 'CLEANERS', 'PAWN'
    ]):
        return 'Commercial'
    elif any(word in loc for word in [
        'CTA', 'TRAIN', 'BUS', 'PLATFORM', 'TAXI',
        'VEHICLE', 'AIRPORT', 'AIRCRAFT', 'BOAT',
        'TRUCK', 'HIGHWAY', 'EXPRESSWAY', 'RAILROAD',
        'SUBWAY'
    ]):
        return 'Transportation'
    elif any(word in loc for word in [
        'SCHOOL', 'COLLEGE', 'UNIVERSITY',
        'HOSPITAL', 'MEDICAL', 'POLICE',
        'JAIL', 'GOVERNMENT', 'CHURCH',
        'FACILITY', 'LIBRARY', 'FIRE STATION',
        'DAY CARE'
    ]):
        return 'Institution'
    elif any(word in loc for word in [
        'STREET', 'SIDEWALK', 'ALLEY',
        'PARK', 'LOT', 'FOREST', 'LAKE',
        'RIVER', 'FIELD', 'PRAIRIE',
        'BRIDGE', 'DUMPSTER', 'GANGWAY'
    ]):
        return 'Public'
    else:
        return 'Other'

input_path = sys.argv[1]

df = pd.read_csv(input_path)

cols_to_drop = [
    'Unnamed: 0',
    'ID',
    'Case Number'
]

df = df.drop(columns=cols_to_drop, errors='ignore')

df = df.drop(columns=['X Coordinate', 'Y Coordinate'])

df = df.drop(columns=['IUCR', 'FBI Code'])

cat_cols = [
    'Date',
    'Block',
    'Primary Type',
    'Description',
    'Location Description',
    'Arrest',
    'Domestic',
    'Beat',
    'District',
    'Ward',
    'Community Area',
    'Year',
    'Updated On',
    'Location'
]

missing_percent_cat = df[cat_cols].isnull().mean() * 100

cols_with_missing_cat = missing_percent_cat[missing_percent_cat > 0].index.tolist()

for col in cols_with_missing_cat:
    mode_value = df[col].mode()[0]
    df[col].fillna(mode_value, inplace=True)

df['Latitude'] = df.groupby('Community Area')['Latitude'].transform(
    lambda x: x.fillna(x.median())
)

df['Longitude'] = df.groupby('Community Area')['Longitude'].transform(
    lambda x: x.fillna(x.median())
)

df = df.drop_duplicates()

df['Date'] = pd.to_datetime(
    df['Date'],
    format='%m/%d/%Y %I:%M:%S %p',
    errors='coerce'
)

df['Month'] = df['Date'].dt.month

df['DayOfWeek'] = df['Date'].dt.dayofweek

df['Hour'] = df['Date'].dt.hour

df = df.drop(columns=['Date'])

df['Location_Group'] = df['Location Description'].apply(group_location_final)

df = pd.get_dummies(
    df,
    columns=['Location_Group', 'Primary Type'],
    prefix=['Loc', 'Crime']
)

df.to_csv("data_preprocessed.csv", index=False)

subprocess.run(["python", "analytics.py", "data_preprocessed.csv"], check=True)