
import sys
from pathlib import Path
import pandas as pd
import subprocess


def main():
    if len(sys.argv) != 2:
        print("Usage: python ingest.py <dataset_path>")
        sys.exit(1)

    dataset_path = Path(sys.argv[1])

    if not dataset_path.exists():
        print(f"Error: file not found -> {dataset_path}")
        sys.exit(1)

    df = pd.read_csv(dataset_path)
    raw_output = Path("data_raw.csv")
    df.to_csv(raw_output, index=False)

    print(f"Raw dataset loaded from: {dataset_path}")
    print(f"Saved raw copy as: {raw_output.resolve()}")

    subprocess.run(["python", "preprocess.py","Chicago_Crimes.csv"], check=True)


if __name__ == "__main__":
    main()