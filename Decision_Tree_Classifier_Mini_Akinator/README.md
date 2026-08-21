# 🧞 Mini-Akinator — Guess the Character using a Decision Tree

**A machine learning-powered guessing game inspired by Akinator. It uses a trained Decision Tree Classifier to ask Yes/No questions, narrow down possible characters, and predict the character you're thinking of based on their traits.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)

<br/>

---

## 📖 Project Overview

The classic Akinator game feels almost magical — a handful of questions and it somehow knows exactly who's in your head. Under the hood, though, that "magic" is really just a decision tree: a structure that repeatedly splits a set of candidates in half based on the most informative yes/no question available at each step.

Mini-Akinator recreates that experience from scratch. A `DecisionTreeClassifier` is trained on a small CSV of characters, each described by a set of binary traits (e.g. *Indian, Batsman, WicketKeeper*). Scikit-learn's tree-building algorithm figures out, for every node, which single trait best separates the remaining characters — so the game doesn't ask questions in a fixed order, it asks whatever question is most useful given everything you've already answered.

At runtime, the FastAPI backend doesn't call `.predict()` on the whole tree at once. Instead, it "walks" the tree node by node in step with the player:

- Start the game and you land on the tree's root node
- The backend reads which feature that node splits on, and turns it into a natural-language question (`Male` → *"Is your character male?"*)
- You answer Yes or No, and the game moves to the right or left child accordingly
- This repeats until you hit a leaf node — at which point the leaf's majority class becomes the guess, along with a confidence score based on how "pure" that leaf is
- If the guess is wrong, that character gets excluded and the session resets to the root to try again — so the game can recover instead of just giving up

Each player gets their own session (tracked by a UUID), so the game can support multiple people playing at once without their progress colliding.

---

## 🚀 Features

- **Adaptive Questions** — Decision Tree selects the best questions dynamically
- **Confidence + Progress** — Shows prediction confidence and game progress
- **Wrong-Guess Recovery** — Excludes wrong guesses and tries again
- **Multi-Player Sessions** — Each game has a unique session ID
- **Human-Readable Questions** — Converts feature names into natural questions
- **Health Endpoint** — Shows model accuracy and character count
- **Animated Frontend** — Simple HTML/CSS/JS genie-themed interface
- **Fully Retrainable** — Add characters and retrain without changing the game logic

---

## 🏗 Project Architecture

```
User Starts Game  (POST /start)
    │
    ▼
New Session Created → node = ROOT of Decision Tree
    │
    ▼
Is Current Node a Leaf? ──── Yes ──► Return Guess + Confidence
    │ No                                     │
    ▼                                        ▼
Look Up Feature at This Node         Guess Correct?  (POST /guess-feedback)
    │                                   ├── Yes → 🎉 Game Over
    ▼                                   └── No  → Add character to
Translate Feature → Question               excluded set → back to ROOT
    │
    ▼
Return Question to Player (POST /answer sends the reply)
    │
    ▼
Yes (1) → Go to RIGHT child
No  (0) → Go to LEFT child
    │
    ▼
(loop back to "Is Current Node a Leaf?")
```

---

## 🛠 Tech Stack

<div align="center">

| Category | Tools | Why |
|---|---|---|
| 🐍 Language | Python | Core logic, training, and API |
| ⚡ Backend / API | FastAPI, Uvicorn | Async-friendly, auto-generates docs, fast to iterate on |
| 🤖 Machine Learning | Scikit-learn (`DecisionTreeClassifier`) | Built-in tree structure is directly walkable node-by-node — no need to hand-roll a decision engine |
| 📊 Data Handling | Pandas | Reading and shaping the trait CSV before training |
| 💾 Model Persistence | Joblib | Saving/loading the trained tree + metadata between runs |
| 🌐 Frontend | HTML, CSS, JavaScript | Lightweight, no build tooling, easy to theme and animate |

</div>

---

## 📂 Project Structure

```
Mini-Akinator/
│
├── train.py                    # Trains the tree from the CSV, saves model + metadata
│
├── data/
│   └── mini_akinator_dataset.csv   # Characters + their binary trait columns
│
├── model/
│   ├── akinator_model.pkl      # The trained DecisionTreeClassifier
│   └── akinator_meta.pkl       # Feature names, character list, training accuracy
│
├── backend/
│   ├── main.py                 # FastAPI routes (/start, /answer, /predict, /reset, ...)
│   ├── model_utils.py          # AkinatorModel (tree-walking) + GameSession (game state)
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

---

## 📊 Dataset

The dataset (`data/mini_akinator_dataset.csv`) is deliberately simple: one row per character, one column per trait, values are strictly `1` (yes) or `0` (no). The current build ships with a cricket-themed set — 10 well-known players described across 6 traits:

| Column | Meaning |
|:---:|---|
| `Character` | Name of the player being guessed (this is the prediction target, not a feature) |
| `Indian` | Whether the player is Indian |
| `Batsman` | Whether the player is primarily known as a batsman |
| `Bowler` | Whether the player is primarily known as a bowler |
| `AllRounder` | Whether the player is known as an all-rounder (bats *and* bowls) |
| `WicketKeeper` | Whether the player is a wicketkeeper |
| `IsCurrentCaptain` | Whether the player currently captains their team |

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/sunidhikK/MachineLearning_Projects.git
```

**2. Move into the project directory**
```bash
cd MachineLearning_Projects/Mini-Akinator
```

**3. Install dependencies**
```bash
pip install -r backend/requirements.txt
```

---

## ▶️ Run Application

**1. (Re)train the model** — do this once, and again any time the dataset changes:
```bash
python train.py
```
This prints how many characters and traits it loaded, the resulting training accuracy, and — if it's below 1.0 — which characters need more distinguishing traits.

**2. Start the backend API**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
The `--reload` flag is handy while developing the game logic; drop it for a production-style run.

**3. Open the frontend**

Open `frontend/index.html` directly in your browser — it's a static page that calls the API at `http://localhost:8000`, so no separate dev server is needed for it.

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|---|:---:|---|
| `/start` | POST | Begins a new game session, returns a fresh `session_id` and the first question |
| `/answer` | POST | Submits a Yes/No answer for the current question, advances the tree, and returns either the next question or a final guess |
| `/predict` | POST | Returns the current best guess for an existing session without advancing it |
| `/guess-feedback` | POST | Tells the backend whether the last guess was correct — `true` ends the game, `false` triggers the exclusion + retry flow |
| `/reset` | POST | Resets a session back to the root (or starts a brand-new one if the session doesn't exist) |
| `/health` | GET | Returns `{ status, characters, accuracy }` — a quick way to confirm the model loaded correctly after a retrain |

---

## 📸 Screenshots

**Home Screen**

<img width="1842" height="862" alt="Screenshot 2026-08-21 173314" src="https://github.com/user-attachments/assets/2b0abeb6-c0cf-4a57-8812-f6b38b628519" />

**Question in Progress**

<img width="1842" height="866" alt="Screenshot 2026-08-21 173615" src="https://github.com/user-attachments/assets/3fe6f956-9ea1-40c5-ac77-d2c43f6f966d" />

**Final Guess**

<img width="1766" height="877" alt="Screenshot 2026-08-21 173756" src="https://github.com/user-attachments/assets/24404066-21ce-4faa-bacd-8338b9ba3e73" />

**Guessed Ans**

<img width="1837" height="850" alt="Screenshot 2026-08-21 173857" src="https://github.com/user-attachments/assets/6a68054c-8be4-4660-b690-ff5f80991f9b" />

**Aligning with the dataset**

<img width="1351" height="407" alt="Screenshot 2026-08-21 174130" src="https://github.com/user-attachments/assets/858401ed-0645-41a4-8d9b-4f9bfaeaeb72" />

---

<div align="center">

<sub>Built with 🧠 and ☕ by K. Sunidhi Sai</sub>

</div>
