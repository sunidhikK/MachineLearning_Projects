

from typing import Optional, Tuple

import pandas as pd

from preprocessing import clean_text


def prepare_search_index(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df["clean_content"] = (df["title"].fillna(
        "") + " " + df["text"].fillna("")).apply(clean_text)
    return df


def search_dataset(user_text: str, indexed_df: pd.DataFrame) -> Tuple[bool, Optional[int], Optional[pd.Series]]:

    if "clean_content" not in indexed_df.columns:
        raise ValueError(
            "indexed_df must be built using prepare_search_index() first.")

    cleaned_input = clean_text(user_text)

    if cleaned_input == "":
        return False, None, None

    matches = indexed_df[indexed_df["clean_content"] == cleaned_input]

    if matches.empty:
        return False, None, None

    matched_row = matches.iloc[0]
    actual_label = int(matched_row["label"])

    return True, actual_label, matched_row
