"""
utils.py
--------
Shared constants and small helper functions used across the project.
Keeping paths in one place means no file path is ever hardcoded
inside the individual modules.
"""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "dataset" / "news_dataset.csv"

MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "fake_news_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"


LABEL_MAP = {0: "Fake", 1: "Real"}


def build_content(df: pd.DataFrame) -> pd.Series:

    content = df["title"].fillna("") + " " + df["text"].fillna("")

    if "subject" in df.columns:
        content = content + " " + df["subject"].fillna("")

    return content
