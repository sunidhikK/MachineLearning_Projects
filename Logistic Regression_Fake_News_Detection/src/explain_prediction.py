

from typing import List, Tuple

from preprocessing import clean_text


def explain_prediction(text: str, model, vectorizer, top_n: int = 15) -> List[Tuple[str, float]]:
    

    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])

    feature_names = vectorizer.get_feature_names_out()
    coefficients = model.coef_[0]

    nonzero_indices = vector.nonzero()[1]

    contributions = []

    for idx in nonzero_indices:
        tfidf_value = vector[0, idx]
        weight = coefficients[idx]
        contribution = float(tfidf_value * weight)
        contributions.append((feature_names[idx], contribution))

    contributions.sort(key=lambda item: abs(item[1]), reverse=True)

    return contributions[:top_n]
