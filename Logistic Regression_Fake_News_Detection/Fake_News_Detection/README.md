# 📰 AI Powered Fake News Detection System

A Streamlit app that detects whether a news article is **Fake** or **Real**
using a TF-IDF + Logistic Regression model, with a dataset lookup step and
coefficient-based explainable AI.

## Features

- Checks if a pasted article already exists in the training dataset and, if so,
  shows the real label alongside the model's prediction (with a correct/incorrect flag).
- If the article is new, predicts Fake/Real with a confidence score.
- Shows the top words that pushed the prediction towards Real or Fake, both as
  a table and as a horizontal bar chart.

## Project Structure

```
Fake_News_Detection/
├── app.py                     # Streamlit app (entry point)
├── requirements.txt
├── README.md
├── dataset/
│   └── news_dataset.csv
├── models/
│   ├── fake_news_model.pkl        # created by train_model.py
│   └── tfidf_vectorizer.pkl       # created by train_model.py
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   ├── explain_prediction.py
│   ├── search_dataset.py
│   └── utils.py
└── assets/
```

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Train the model (only needed once, or whenever the dataset changes):

   ```bash
   cd src
   python train_model.py
   cd ..
   ```

   This creates `models/fake_news_model.pkl` and `models/tfidf_vectorizer.pkl`.

3. Run the app:

   ```bash
   streamlit run app.py
   ```

## Dataset Format

The dataset CSV must contain at least these columns:

| column | description                  |
|--------|-------------------------------|
| title  | article headline              |
| text   | article body                  |
| label  | 0 = Fake, 1 = Real             |

An optional `subject` column, if present, is also used as a training signal.

## Notes

- The trained model files in `models/` are not tracked if you re-train — running
  `train_model.py` again will overwrite them with a fresh model on your dataset.
- The app only focuses on prediction + explanation, no accuracy/confusion-matrix
  dashboards are shown in the UI, by design.
