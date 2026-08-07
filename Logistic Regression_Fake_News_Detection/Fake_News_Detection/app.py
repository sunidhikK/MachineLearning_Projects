"""
Run with:
    streamlit run app.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from data_loader import load_data  # noqa: E402
from search_dataset import prepare_search_index, search_dataset  # noqa: E402
from predict import load_model, predict_news, predict_probability  # noqa: E402
from explain_prediction import explain_prediction  # noqa: E402
from utils import DATASET_PATH, LABEL_MAP  # noqa: E402


st.set_page_config(
    page_title="AI Powered Fake News Detection System",
    page_icon="📰",
    layout="wide",
)


@st.cache_resource(show_spinner="Loading trained model...")
def get_model():
    try:
        return load_model()
    except FileNotFoundError as e:
        return None, str(e)


@st.cache_data(show_spinner="Loading dataset...")
def get_indexed_dataset():
    df = load_data(DATASET_PATH)
    return prepare_search_index(df)


st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }
    .result-card {
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1rem;
    }
    .card-real {
        background-color: #ecfdf5;
        border: 1px solid #10b981;
    }
    .card-fake {
        background-color: #fef2f2;
        border: 1px solid #ef4444;
    }
    .card-neutral {
        background-color: #f3f4f6;
        border: 1px solid #d1d5db;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="main-title">📰 AI Powered Fake News Detection System</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Detect whether a news article is Fake or Real using '
    "Machine Learning and Explainable AI.</div>",
    unsafe_allow_html=True,
)


model_result = get_model()

if model_result[0] is None:
    st.error(
        "⚠️ No trained model found.\n\n"
        "Please run the following command from inside the `src/` folder first, "
        "then restart the app:\n\n`python train_model.py`"
    )
    st.stop()

model, vectorizer = model_result

try:
    indexed_df = get_indexed_dataset()
except Exception as e:  # noqa: BLE001
    st.error(f"⚠️ Could not load the dataset: {e}")
    st.stop()


news_text = st.text_area(
    "Paste news article here...",
    height=220,
    placeholder="Paste the full news article text (or headline) you want to check...",
)

analyze_clicked = st.button("🔍 Analyze News", type="primary")


if analyze_clicked:

    if not news_text or not news_text.strip():
        st.warning("Please enter a news article before analyzing.")
        st.stop()

    with st.spinner("Analyzing article..."):

        found, actual_label, matched_row = search_dataset(
            news_text, indexed_df)

        prediction = predict_news(news_text, model, vectorizer)
        probabilities = predict_probability(news_text, model, vectorizer)
        fake_prob, real_prob = probabilities[0], probabilities[1]

        predicted_label_text = LABEL_MAP[prediction]

    st.divider()

    if found:
        actual_label_text = LABEL_MAP[actual_label]

        st.subheader("🔎 Dataset Match Found")
        st.info(f"**Actual Label:** {actual_label_text} News")

        st.subheader("🤖 Model Prediction")
        card_class = "card-real" if prediction == 1 else "card-fake"
        st.markdown(
            f'<div class="result-card {card_class}"><h3>Prediction: {predicted_label_text} News</h3></div>',
            unsafe_allow_html=True,
        )

        if prediction == actual_label:
            st.success(
                "✅ Correct Prediction — model agrees with the dataset label.")
        else:
            st.error(
                "❌ Incorrect Prediction — model disagrees with the dataset label.")

    else:
        st.subheader("🆕 New Article")
        st.info(
            "This article was not found in the dataset. Predicting using the trained AI model...")

        st.subheader("🤖 Prediction")
        card_class = "card-real" if prediction == 1 else "card-fake"
        st.markdown(
            f'<div class="result-card {card_class}"><h3>Prediction: {predicted_label_text} News</h3></div>',
            unsafe_allow_html=True,
        )

    st.subheader("📊 Confidence")

    confidence = max(fake_prob, real_prob)
    st.metric("Confidence", f"{confidence:.1%}")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Real** — {real_prob:.1%}")
        st.progress(float(real_prob))

    with col2:
        st.write(f"**Fake** — {fake_prob:.1%}")
        st.progress(float(fake_prob))

    st.divider()
    st.subheader("🧠 Explainable AI — Top Important Words")

    explanation = explain_prediction(news_text, model, vectorizer, top_n=15)

    if not explanation:
        st.write(
            "No overlapping vocabulary words were found to explain this prediction.")
    else:
        explain_df = pd.DataFrame(explanation, columns=[
                                  "Word", "Contribution"])
        explain_df["Supports"] = explain_df["Contribution"].apply(
            lambda x: "Real" if x > 0 else "Fake"
        )

        st.dataframe(
            explain_df.style.format({"Contribution": "{:.4f}"}),
            use_container_width=True,
            hide_index=True,
        )

        # Contribution graph
        plot_df = explain_df.sort_values("Contribution")
        colors = ["#10b981" if v >
                  0 else "#ef4444" for v in plot_df["Contribution"]]

        fig, ax = plt.subplots(figsize=(8, max(4, len(plot_df) * 0.35)))
        ax.barh(plot_df["Word"], plot_df["Contribution"], color=colors)
        ax.axvline(0, color="#9ca3af", linewidth=0.8)
        ax.set_xlabel(
            "Contribution (green = supports Real, red = supports Fake)")
        ax.set_title("Word Contribution to Prediction")
        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

    st.divider()
    st.subheader("📝 Prediction Summary")

    summary_lines = [
        f"- **Dataset Status:** {'Found in dataset' if found else 'New / not in dataset'}",
    ]
    if found:
        summary_lines.append(f"- **Actual Label:** {LABEL_MAP[actual_label]}")
    summary_lines.append(f"- **Model Prediction:** {predicted_label_text}")
    summary_lines.append(f"- **Confidence:** {confidence:.1%}")

    st.markdown("\n".join(summary_lines))

else:
    st.caption("Paste an article above and click **Analyze News** to get started.")
