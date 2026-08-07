<div align="center">

# 📰 Fake News Detection using Machine Learning

**A machine learning-powered web app that classifies news articles as Real or Fake using NLP and Logistic Regression.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B?style=for-the-badge)
![License](https://img.shields.io/badge/License-Educational-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

<br/>

<!-- Add a banner image or GIF here, e.g. screenshots/banner.png -->
<img src="screenshots/banner.png" alt="Fake News Detection banner" width="800"/>

</div>

---

## 📑 Table of Contents

- [Overview](#-project-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-project-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Installation](#️-installation)
- [Usage](#️-run-application)
- [ML Workflow](#-machine-learning-workflow)
- [Model Performance](#-model-performance)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)
- [License](#-license)

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

## 🎥 Demo

<div align="center">

<!-- Replace with an actual recording — record your Streamlit app with ScreenToGif / Kap / Peek and drop it in screenshots/ -->
<img src="screenshots/demo.gif" alt="App demo" width="800"/>

*A short walkthrough: paste or search a news article → get an instant Real/Fake prediction with confidence score.*

</div>

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

<sub>Dataset sourced from [Kaggle Fake and Real News Dataset](https://www.kaggle.com/) — update this link with your actual source.</sub>

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

## 📈 Model Performance

<div align="center">

| Metric | Score |
|---|:---:|
| Accuracy | `xx%` |
| Precision | `xx%` |
| Recall | `xx%` |
| F1-Score | `xx%` |

*(Replace with your actual evaluation metrics from `train.py`)*

</div>

---

## 📸 Screenshots

<div align="center">

| Home Screen | Prediction Result |
|---|---|
| <img src="screenshots/home.png" width="380"/> | <img src="screenshots/prediction.png" width="380"/> |

</div>

> Save your screenshots into a `screenshots/` folder in the repo root with the filenames above — GitHub will render them automatically.

---

## 🔮 Future Enhancements

- Deep Learning models (LSTM/RNN)
- BERT Transformer-based classification
- News URL detection (auto-scrape and classify)
- Explainable AI (SHAP / LIME integration)
- Live News API integration
- Model comparison dashboard

---

## 👩‍💻 Author

<div align="center">

**K. Sunidhi Sai**
B.Tech CSE Student · SAP Certified ABAP Cloud Developer · AI & Machine Learning Enthusiast

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

</div>

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub — it helps a lot and supports future work!

---

## 📄 License

This project is created for educational and learning purposes.

<div align="center">

<sub>Built with 🧠 and ☕ by K. Sunidhi Sai</sub>

</div>
