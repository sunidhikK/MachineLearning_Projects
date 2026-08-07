

import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from data_loader import load_data
from preprocessing import clean_text
from utils import DATASET_PATH, MODEL_DIR, MODEL_PATH, VECTORIZER_PATH, build_content


def train_model(save: bool = True):
    

    print("=" * 60)
    print("Loading Dataset...")
    print("=" * 60)

    df = load_data(DATASET_PATH)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")


    print("\nCleaning text...")
    df["content"] = build_content(df).apply(clean_text)
    print("Text cleaning completed")

    X_text = df["content"]
    y = df["label"]

    

    print("\nApplying TF-IDF vectorization...")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=50000,
    )

    X = vectorizer.fit_transform(X_text)

    print(f"Vocabulary size: {len(vectorizer.get_feature_names_out())}")


    print("\nSplitting dataset (80% train / 20% test)...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training samples: {X_train.shape[0]}")
    print(f"Testing samples : {X_test.shape[0]}")

    

    print("\nTraining Logistic Regression model...")

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    print("Model training completed")


    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nInternal test accuracy: {accuracy:.4f}")


    if save:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)

        with open(VECTORIZER_PATH, "wb") as f:
            pickle.dump(vectorizer, f)

        print(f"\nModel saved to      : {MODEL_PATH}")
        print(f"Vectorizer saved to : {VECTORIZER_PATH}")

    print("\n" + "=" * 60)
    print("Training Pipeline Completed Successfully")
    print("=" * 60)

    return model, vectorizer, accuracy


if __name__ == "__main__":
    train_model()
