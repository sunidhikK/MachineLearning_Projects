📰 Fake News Detection using Machine Learning
<br/> <!-- Add a banner image or GIF here, e.g. screenshots/banner.png --> <img src="screenshots/banner.png" alt="Fake News Detection banner" width="800"/> </div>
A machine learning-based web application that detects whether a news article is Real or Fake using NLP techniques such as text cleaning, lowercasing, punctuation removal, stopword removal, and tokenization. The processed text is converted into numerical features using TF-IDF vectorization and classified using a Logistic Regression model.

🚀 Features
Detects Fake and Real news
Dataset search functionality
Prediction for new, unseen articles
NLP preprocessing pipeline
TF-IDF Vectorization
Logistic Regression model
User-friendly Streamlit interface

🏗 Project Architecture
<div align="center">
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
  </div>

🛠 Tech Stack
<div align="center">
Category	Tools
🐍 Language	Python
🌐 Web App	Streamlit
🤖 Machine Learning	Scikit-learn
📊 Data Handling	Pandas, NumPy
📝 NLP	NLTK
💾 Model Persistence	Pickle
</div>

📂 Project Structure
<div>
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
</div>

📊 Dataset
<div>
The dataset contains news articles labeled as:
Label	Meaning
🟥 0	Fake News
🟩 1	Real News
</div>
<sub>Dataset sourced from Kaggle Fake and Real News Dataset — https://www.kaggle.com/datasets/hurualqayeva/news-dataset.</sub>

⚙️ Installation

1. Clone the repository

bash
git clone https://github.com/yourusername/Fake_News_Detection.git

2. Move into the project directory

bash
cd Fake_News_Detection

3. Install dependencies

bash
pip install -r requirements.txt
▶️ Run Application
bash
streamlit run app.py
🧠 Machine Learning Workflow
Load dataset
Clean text
Tokenize
Remove stopwords
Apply TF-IDF vectorization
Train Logistic Regression model
Save model
Predict on new news input



📸 Screenshots
<div align="center">
Home Screen
<img width="1920" height="796" alt="Screenshot 2026-08-07 230054" src="https://github.com/user-attachments/assets/28397ba3-cdcf-4a65-b10e-3e8974857b03" />

prediction Screen 
<img width="1920" height="760" alt="Screenshot 2026-08-07 230109" src="https://github.com/user-attachments/assets/69fc20cb-ac76-4333-bb77-33acb6edb6b7" />

explainable_ai
<img width="1920" height="863" alt="Screenshot 2026-08-07 230128" src="https://github.com/user-attachments/assets/3e3777bd-c04c-43a9-af60-853c2fb00a52" />
</div>






