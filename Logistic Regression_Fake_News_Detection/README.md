
# 📰 Fake News Detection using Machine Learning

**A machine learning-based web application that detects whether a news article is Real or Fake using NLP techniques such as text cleaning, lowercasing, punctuation removal, stopword removal, and tokenization. The processed text is converted into numerical features using TF-IDF vectorization and classified using a Logistic Regression model. The app also includes an Explainable AI module that shows which words influenced each prediction.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B?style=for-the-badge)


<br/>


---

## 📖 Project Overview

This project classifies news articles as Real or Fake using TF-IDF Vectorization and a Logistic Regression model. Users can either:

- Search whether an article already exists in the dataset
- Predict the authenticity of a completely new news article
- Compare the prediction with the actual dataset label (if found)

---

## 🚀 Features

- Detects Fake and Real news
- Dataset search functionality
- Prediction for new, unseen articles
- NLP preprocessing pipeline
- TF-IDF Vectorization
- Logistic Regression model
- User-friendly Streamlit interface

---

## 🏗 Project Architecture

```
User Input
    │
    ▼
Clean Text
    │
    ▼
Search Dataset
    │
    ▼
Article Found?
    ├── Yes → Show Actual Label → Compare with Prediction
    └── No  → Predict New Article → Display Result
```

---

## 🛠 Tech Stack

<div align="center">

| Category | Tools |
|---|---|
| 🐍 Language | Python |
| 🌐 Web App | Streamlit |
| 🤖 Machine Learning | Scikit-learn |
| 📊 Data Handling | Pandas, NumPy |
| 📝 NLP | NLTK |
| 💾 Model Persistence | Pickle |

</div>

---

## 📂 Project Structure

```
Fake_News_Detection/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── news_dataset.csv
│
├── models/
│   ├── logistic_model.pkl
│   └── tfidf_vectorizer.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── predict.py
│   ├── explain_prediction.py
│   └── train.py
│
└── screenshots/
    ├── home.png
    └── prediction.png
```

---

## 📊 Dataset

The dataset contains news articles labeled as:

| Label | Meaning |
|:---:|---|
| 🟥 `0` | Fake News |
| 🟩 `1` | Real News |

<sub>Dataset sourced from [Kaggle Fake and Real News Dataset](https://www.kaggle.com/) — (https://www.kaggle.com/datasets/hurualqayeva/news-dataset).</sub>

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/Fake_News_Detection.git
```

**2. Move into the project directory**
```bash
cd Fake_News_Detection
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 🧠 Machine Learning Workflow

1. Load dataset
2. Clean text
3. Tokenize
4. Remove stopwords
5. Apply TF-IDF vectorization
6. Train Logistic Regression model
7. Save model
8. Predict on new news input


---

## 📸 Screenshots

**Home Screen**

<img width="1920" height="796" alt="Screenshot 2026-08-07 230054" src="https://github.com/user-attachments/assets/b58dd00d-b8b8-45fc-9589-e9e2c1e43211" />

**Prediction Result**

<img width="1920" height="760" alt="Screenshot 2026-08-07 230109" src="https://github.com/user-attachments/assets/3d92b986-8a46-43ac-baca-21917bcd4b75" />

**Explainable AI — Word Contribution**

<img width="1920" height="863" alt="Screenshot 2026-08-07 230128" src="https://github.com/user-attachments/assets/10d8277a-7849-41a2-909d-14a31bf3267b" />

---

<div align="center">

<sub>Built with 🧠 and ☕ by K. Sunidhi Sai</sub>

</div>
