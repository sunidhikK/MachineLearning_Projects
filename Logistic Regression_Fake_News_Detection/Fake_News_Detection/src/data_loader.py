
import pandas as pd


def load_data(path) -> pd.DataFrame:
    

    df = pd.read_csv(path)

    required_columns = {"title", "text", "label"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required column(s): {missing}")

    df = df.dropna(subset=["title", "text", "label"]).reset_index(drop=True)
    df = df.drop_duplicates(subset=["title", "text"]).reset_index(drop=True)

    df["label"] = df["label"].astype(int)

    return df


if __name__ == "__main__":
    from utils import DATASET_PATH

    data = load_data(DATASET_PATH)

    print("=" * 50)
    print("Dataset Loaded Successfully")
    print("=" * 50)
    print("\nShape:", data.shape)
    print("\nColumns:", data.columns.tolist())
    print("\nLabel Counts:\n", data["label"].value_counts())
