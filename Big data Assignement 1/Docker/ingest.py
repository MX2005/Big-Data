import sys
import pandas as pd

dataset_path = sys.argv[1]

df = pd.read_csv(dataset_path)

df.to_csv("data_raw.csv", index=False)