# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt 
# from sklearn.cluster import KMeans

# df = pd.read_csv('data_preprocessed.csv')

# bool_cols = df.select_dtypes(include=["bool"]).columns
# for col in bool_cols:
#     df[col] = df[col].apply(lambda x: 0.0 if x is False else 1.0)
# numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
# X = df[numeric_cols]
# print(list(numeric_cols))

# kmeans = KMeans(n_clusters=4, random_state=1)
# df["cluster"] = kmeans.fit_predict(X)

# cluster_counts = df["cluster"].value_counts().sort_index()
# print("Cluster counts:\n", cluster_counts)

# df.groupby("cluster")[numeric_cols].mean()


# cluster_profiles = df.groupby("cluster")[numeric_cols].mean()
# for cluster_id in cluster_profiles.index:
#     print(f"\nTop features for Cluster {cluster_id}:")
#     print(cluster_profiles.loc[cluster_id].sort_values(ascending=False))


# with open("clusters.txt", "w") as f:
#     for cluster_id in cluster_profiles.index:
#         f.write(f"\nTop features for Cluster {cluster_id}:\n")
#         sorted_features = cluster_profiles.loc[cluster_id].sort_values(ascending=False)
#         for feature, value in sorted_features.items():
#             f.write(f"{feature:40} {value:.6f}\n")





import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def main():
    if len(sys.argv) != 2:
        print("Usage: python cluster.py <input_csv>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: file not found -> {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)

    # ✅ Fix 1: Convert boolean columns exactly like original code
    bool_cols = df.select_dtypes(include=["bool"]).columns
    for col in bool_cols:
        df[col] = df[col].apply(lambda x: 0.0 if x is False else 1.0)

    # ✅ Fix 2: Select numeric columns (same as original)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    # 🚨 CRITICAL FIX: sample the data to avoid memory crash
    df_sample = df.sample(min(50000, len(df)), random_state=1)

    X = df_sample[numeric_cols]

    print(list(numeric_cols))

    # ✅ Same KMeans config as original
    kmeans = KMeans(n_clusters=4, random_state=1)
    df_sample["cluster"] = kmeans.fit_predict(X)

    cluster_counts = df_sample["cluster"].value_counts().sort_index()
    print("Cluster counts:\n", cluster_counts)

    cluster_profiles = df_sample.groupby("cluster")[numeric_cols].mean()

    # Print top features per cluster (same logic)
    for cluster_id in cluster_profiles.index:
        print(f"\nTop features for Cluster {cluster_id}:")
        print(cluster_profiles.loc[cluster_id].sort_values(ascending=False))

    # Save to file (same format)
    with open("clusters.txt", "w", encoding="utf-8") as f:
        for cluster_id in cluster_profiles.index:
            f.write(f"\nTop features for Cluster {cluster_id}:\n")
            sorted_features = cluster_profiles.loc[cluster_id].sort_values(ascending=False)
            for feature, value in sorted_features.items():
                f.write(f"{feature:40} {value:.6f}\n")

    print("Clustering complete. Results saved to clusters.txt")


if __name__ == "__main__":
    main()