🧞 Mini-Akinator — Guess the Character using a Decision Tree

A machine learning-based web game that guesses \*\*who you're thinking of\*\* by asking a series of Yes/No questions, inspired by the classic Akinator. The game is powered by a \*\*Decision Tree Classifier\*\* trained on a small dataset of characters and their binary trait features (e.g. \*Indian, Batsman, WicketKeeper\*), served through a \*\*FastAPI\*\* backend and presented with an animated, genie-themed \*\*HTML/CSS/JS\*\* frontend.



!\[Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)

!\[FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)

!\[Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge\&logo=scikitlearn\&logoColor=white)

!\[Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)

!\[JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge\&logo=javascript\&logoColor=F7DF1E)



\## 📖 Project Overview

This project walks a trained Decision Tree one node at a time to figure out which character the user is thinking of. Each internal node of the tree represents a Yes/No question about a trait; each leaf represents a guess. Users can:

\- Answer a sequence of Yes/No questions about their character

\- Get a live confidence score and progress bar as the game narrows down the answer

\- Reject a wrong guess and let the model try again, excluding that character

\- See the model's final guess once it reaches a leaf node



\## 🚀 Features

\- Guesses a character from a series of Yes/No questions

\- Tree-walking logic that adapts the question order to previous answers

\- Confidence score and progress indicator shown live

\- "Wrong guess" flow — reject a guess and get a new one

\- Session-based gameplay (supports multiple concurrent players)

\- Animated, genie-styled frontend

\- REST API backend built with FastAPI



\## 🏗 Project Architecture

```

User Starts Game

&#x20;     │

&#x20;     ▼

Walk Decision Tree (root node)

&#x20;     │

&#x20;     ▼

Ask Question for Current Node's Feature

&#x20;     │

&#x20;     ▼

User Answers Yes / No

&#x20;     │

&#x20;     ▼

Move to Right Child (Yes) or Left Child (No)

&#x20;     │

&#x20;     ▼

Leaf Node Reached?

&#x20;  ├── No  → Ask Next Question (repeat)

&#x20;  └── Yes → Show Guess + Confidence

&#x20;                │

&#x20;                ▼

&#x20;        Guess Correct?

&#x20;           ├── Yes → 🎉 Game Over

&#x20;           └── No  → Exclude Character → Re-walk Tree → New Guess

```



\## 🛠 Tech Stack

| Category | Tools |

|---|---|

| 🐍 Language | Python |

| ⚡ Backend / API | FastAPI, Uvicorn |

| 🤖 Machine Learning | Scikit-learn (Decision Tree Classifier) |

| 📊 Data Handling | Pandas |

| 💾 Model Persistence | Joblib |

| 🌐 Frontend | HTML, CSS, JavaScript |



\## 📂 Project Structure

```

Mini-Akinator/

│

├── train.py

│

├── data/

│   └── mini\_akinator\_dataset.csv

│

├── model/

│   ├── akinator\_model.pkl

│   └── akinator\_meta.pkl

│

├── backend/

│   ├── main.py

│   ├── model\_utils.py

│   └── requirements.txt

│

└── frontend/

&#x20;   ├── index.html

&#x20;   ├── style.css

&#x20;   └── script.js

```



\## 📊 Dataset

The dataset (`data/mini\_akinator\_dataset.csv`) contains characters described by a set of \*\*binary trait columns\*\* (`1` = yes, `0` = no). The current version is a cricket-themed dataset with 10 players and 6 traits:



| Column | Meaning |

|---|---|

| `Character` | Name of the player/character being guessed |

| `Indian` | Whether the player is Indian |

| `Batsman` | Whether the player is primarily known as a batsman |

| `Bowler` | Whether the player is primarily known as a bowler |

| `AllRounder` | Whether the player is known as an all-rounder |

| `WicketKeeper` | Whether the player is a wicketkeeper |

| `IsCurrentCaptain` | Whether the player currently captains their team |



Each row is a unique character with a unique combination of traits, so the tree can perfectly memorize a question-path to every one of them. The dataset is fully customizable — add more rows and trait columns to expand the character pool (see `model\_utils.py`'s `QUESTION\_TEMPLATES` for how trait names are turned into friendlier questions, and add an entry there for any new trait column you introduce).



\## ⚙️ Installation

\*\*1. Clone the repository\*\*

```

git clone https://github.com/sunidhikK/MachineLearning\_Projects.git```

\*\*2. Move into the project directory\*\*

```

cd Mini-Akinator/backend

```

\*\*3. Install dependencies\*\*

```

pip install -r requirements.txt

```



\## ▶️ Run Application

\*\*1. (Re)train the model\*\* — run this once, and again any time you edit the dataset:

```

python train.py

```

\*\*2. Start the backend API\*\*

```

cd backend

uvicorn main:app --reload --port 8000

```

\*\*3. Open the frontend\*\*

Open `frontend/index.html` in your browser (it talks to the API at `http://localhost:8000`).



\## 🧠 Machine Learning Workflow

1\. Load `mini\_akinator\_dataset.csv`

2\. Separate trait columns (features) from the `Character` column (target)

3\. Train a `DecisionTreeClassifier` on the \*\*full\*\* dataset (this is a lookup structure per character, not a model meant to generalize — see the note in `train.py`)

4\. Save the trained tree and metadata (`feature\_names`, `characters`, `accuracy`) with Joblib

5\. At game time, walk the tree node by node:

&#x20;  - Each internal node asks about one trait

&#x20;  - \*\*Yes (1)\*\* → right child · \*\*No (0)\*\* → left child

&#x20;  - Reaching a leaf returns the majority-class character as the guess, with a confidence score

6\. If the guess is rejected, that character is excluded and the tree is re-walked from the root for a new guess



\## 🌐 API Endpoints

| Endpoint | Method | Description |

|---|---|---|

| `/start` | POST | Begin a new game session, returns the first question |

| `/answer` | POST | Submit a Yes/No answer, returns the next question or a final guess |

| `/predict` | POST | Get the current best guess without advancing |

| `/guess-feedback` | POST | Tell the model whether its guess was correct |

| `/reset` | POST | Reset a session back to the start |

| `/health` | GET | Health check — returns character count and model accuracy |



\## 📸 Screenshots

\*(Add screenshots of the game here — home screen, a question in progress, and the final guess.)\*



\---

Built with 🧠 and ☕ by K. Sunidhi Sai

