"""
train.py
--------
Reads data/mini_akinator_dataset.csv, trains a Decision Tree that maps
trait-combinations to characters, and saves the result to model/.

Run this once, and again any time you edit the CSV:
    python train.py

NOTE ON TRAIN/TEST SPLITTING:
This game works by having the tree MEMORIZE an exact question-path for
every character (it's a lookup structure, not a model meant to
generalize to unseen people). With small datasets -- especially ones
where every character is a unique row -- a stratified train/test split
will crash, since sklearn can't stratify a class that only has 1
member. So we train on 100% of the data on purpose.
"""

import os
import joblib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "mini_akinator_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "akinator_model.pkl")
META_PATH = os.path.join(MODEL_DIR, "akinator_meta.pkl")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    if "Character" not in df.columns:
        raise ValueError("CSV must have a 'Character' column.")

    feature_names = [c for c in df.columns if c != "Character"]
    X = df[feature_names]
    y = df["Character"]

    print(f"Loaded {len(df)} characters with {len(feature_names)} traits.")
    print("Traits:", feature_names)

    # Train on the FULL dataset -- see note above.
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X, y)

    # "Accuracy" here is just how well the tree fits the data it saw
    # (training accuracy). With unique rows per character this should
    # be 1.0 -- if it's not, some characters still share an identical
    # trait signature and need more differentiating columns.
    preds = model.predict(X)
    accuracy = accuracy_score(y, preds)
    print(f"Training accuracy: {accuracy:.2f}")
    if accuracy < 1.0:
        mismatched = df.loc[y != preds, "Character"].tolist()
        print("WARNING: these characters are not perfectly separable "
              f"with the current traits: {mismatched}")

    characters = sorted(y.unique().tolist())

    joblib.dump(model, MODEL_PATH)
    joblib.dump(
        {
            "feature_names": feature_names,
            "characters": characters,
            "accuracy": accuracy,
        },
        META_PATH,
    )

    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metadata to {META_PATH}")


if __name__ == "__main__":
    main()
