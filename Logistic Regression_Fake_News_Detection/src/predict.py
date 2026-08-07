"""
predict.py
-----------
Loads the trained model + vectorizer from disk and exposes simple
functions for predicting on new text.
"""

import pickle

from preprocessing import clean_text
from utils import MODEL_PATH, VECTORIZER_PATH


def load_model():
    

    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        raise FileNotFoundError(
            "Trained model files not found. Run `python train_model.py` "
            "inside the src/ folder first to generate them."
        )

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer


def predict_news(text: str, model, vectorizer) -> int:
    """Return the predicted label: 0 = Fake, 1 = Real."""

    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = int(model.predict(vector)[0])
    return prediction


def predict_probability(text: str, model, vectorizer):
    """
    Return [fake_probability, real_probability] for the given text.
    Assumes the model's classes are ordered [0, 1], which is how
    sklearn's LogisticRegression sorts them by default.
    """

    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    probabilities = model.predict_proba(vector)[0]
    return probabilities
