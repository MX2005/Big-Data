import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans

df = pd.read_csv('data_preprocessed.csv')

bool_cols = df.select_dtypes(include=["bool"]).columns
for col in bool_cols:
    df[col] = df[col].apply(lambda x: 0.0 if x is False else 1.0)
numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
X = df[numeric_cols]
print(list(numeric_cols))

kmeans = KMeans(n_clusters=4, random_state=1)
df["cluster"] = kmeans.fit_predict(X)

cluster_counts = df["cluster"].value_counts().sort_index()
print("Cluster counts:\n", cluster_counts)

df.groupby("cluster")[numeric_cols].mean()


cluster_profiles = df.groupby("cluster")[numeric_cols].mean()
for cluster_id in cluster_profiles.index:
    print(f"\nTop features for Cluster {cluster_id}:")
    print(cluster_profiles.loc[cluster_id].sort_values(ascending=False))


with open("clusters.txt", "w") as f:
    for cluster_id in cluster_profiles.index:
        f.write(f"\nTop features for Cluster {cluster_id}:\n")
        sorted_features = cluster_profiles.loc[cluster_id].sort_values(ascending=False)
        for feature, value in sorted_features.items():
            f.write(f"{feature:40} {value:.6f}\n")

