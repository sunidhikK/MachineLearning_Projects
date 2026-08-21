# 🧞 Mini-Akinator — Guess the Character using a Decision Tree

**A machine learning-powered guessing game inspired by the classic Akinator — think of a character, answer a handful of Yes/No questions, and watch a trained Decision Tree narrow down exactly who you're thinking of. Instead of hardcoding a decision flow by hand, the game trains a `DecisionTreeClassifier` on a dataset of characters and their traits, then walks that tree live — one answer at a time — asking whichever question best splits the remaining possibilities, tracking a confidence score and progress bar as it goes, and gracefully recovering if it guesses wrong.**

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

- **Adaptive questioning** — the order of questions isn't scripted; it's whatever the trained tree decided was most discriminating for the remaining set of characters
- **Live confidence + progress** — every response includes a confidence score (how "sure" the current node's majority vote is) and a rough progress percentage based on how deep into the tree you are relative to its max depth
- **Wrong-guess recovery** — if the final guess is wrong, the game excludes that character and restarts from the root instead of just admitting defeat
- **Stateful, multi-player sessions** — each game gets a unique `session_id`, so the backend can track many simultaneous games in memory without them interfering
- **Human-readable questions** — raw feature names like `WicketKeeper` are mapped to full questions ("Is your player a wicketkeeper?") via a template dictionary, so the game never leaks column names to the player
- **Health/debug endpoint** — a `/health` route exposes how many characters the model knows and its training accuracy, handy for sanity-checking after retraining
- **Animated, genie-themed frontend** — a lightweight HTML/CSS/JS UI (no framework, no build step) that talks to the FastAPI backend over plain REST calls
- **Fully retrainable** — swap in a bigger dataset with more characters and trait columns, rerun `train.py`, and the game instantly knows a whole new set of characters with zero code changes to the tree-walking logic

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

The key design decision here is that the *game logic* (tree-walking, sessions, excluded characters) lives entirely in the backend, separate from the *model logic* (the trained sklearn tree). `model_utils.py` only knows how to answer "what feature is at this node" and "what's the majority guess here" — the actual game rules (session tracking, exclusion on wrong guesses, progress calculation) sit in `GameSession`, which wraps the model instead of being baked into it.

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

A few things worth knowing about how the dataset is actually used:

- **Every row must be uniquely identifiable by its traits.** `train.py` trains on the *entire* dataset (no train/test split — see the note below) and expects 100% training accuracy. If two characters share an identical trait signature, the tree can't tell them apart and `train.py` will print a warning listing exactly which characters are ambiguous, so you know which trait columns need to be added.
- **No train/test split, on purpose.** This isn't a model meant to generalize to characters it's never seen — it's closer to a lookup table disguised as a classifier. Splitting the data would just mean the tree "forgets" some characters, and with small datasets sklearn's stratified split can't even run when a class has only one row.
- **Adding a trait is a one-line change.** Add a new `0/1` column to the CSV, give it a friendlier phrasing in `model_utils.py`'s `QUESTION_TEMPLATES` dict (otherwise it falls back to a generic `"Is your character '<TraitName>'?"`), and rerun `train.py`. No other code needs to change — the tree-walking logic reads feature names dynamically.
- **Swapping themes entirely is just as easy.** Nothing about the code is cricket-specific; replace the CSV with, say, Marvel characters and matching traits (`Superhero`, `HasPowers`, `FromEarth`...) and the same pipeline trains a completely different game.

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

## 🧠 How the Tree-Walking Actually Works

This is the part that makes the project more than "train a model, call `.predict()`" — worth spelling out because it's the core trick:

1. **Training** (`train.py`) fits a standard `DecisionTreeClassifier` on the full dataset and saves it with Joblib, alongside metadata (feature names, the sorted character list, and training accuracy).
2. **Loading** (`model_utils.AkinatorModel`) reaches into sklearn's internal `tree_` structure directly — the arrays `tree_.feature`, `tree_.children_left`, `tree_.children_right`, and `tree_.value` — rather than treating the model as a black box you only call `.predict()` on.
3. **Reading a node**: `tree_.feature[node_id]` gives the index of the trait that node splits on (or `-2` if it's a leaf). That index is mapped back to a human name and passed through `QUESTION_TEMPLATES` to produce the actual question text shown to the player.
4. **Advancing**: because sklearn splits binary (0/1) features at the threshold 0.5, a **Yes** answer (1) always means "go right" (`X > 0.5`) and a **No** answer (0) always means "go left" (`X <= 0.5`). `next_child()` encodes exactly that rule.
5. **Guessing at a leaf**: `tree_.value[node_id]` holds the class distribution of training examples that landed at that node. The majority class is the guess; dividing its count by the total gives the confidence score returned to the frontend.
6. **Recovering from a wrong guess**: `GameSession.reject_current_guess()` adds the guessed character to an `excluded_characters` set and resets `node_id` back to the root — since the tree has no way to "resume" past a leaf, restarting the walk (now silently avoiding the excluded character once it's reached again) is the simplest correct fix.

The result is a decision tree that's driven interactively instead of all at once — the classic ML training/inference split, just with the inference step spread out over several HTTP requests instead of one.

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

*(<img width="1842" height="862" alt="Screenshot 2026-08-21 173314" src="https://github.com/user-attachments/assets/2b0abeb6-c0cf-4a57-8812-f6b38b628519" />

)*

**Question in Progress**

*(<img width="1842" height="866" alt="Screenshot 2026-08-21 173615" src="https://github.com/user-attachments/assets/3fe6f956-9ea1-40c5-ac77-d2c43f6f966d" />
)*

**Final Guess**

*(<img width="1766" height="877" alt="Screenshot 2026-08-21 173756" src="https://github.com/user-attachments/assets/24404066-21ce-4faa-bacd-8338b9ba3e73" />
)*

**Guessed Ans**
*(<img width="1837" height="850" alt="Screenshot 2026-08-21 173857" src="https://github.com/user-attachments/assets/6a68054c-8be4-4660-b690-ff5f80991f9b" />
)*

**Aligning with the dataset**
*(<img width="1351" height="407" alt="Screenshot 2026-08-21 174130" src="https://github.com/user-attachments/assets/858401ed-0645-41a4-8d9b-4f9bfaeaeb72" />
)*


---

<div align="center">

<sub>Built with 🧠 and ☕ by K. Sunidhi Sai</sub>

</div>
