"""
model_utils.py
---------------
Loads the trained Decision Tree and lets the game "walk" down the tree
one answer at a time — this is what makes the question order feel smart
instead of random.

How it works:
- Every internal node of the tree asks about ONE feature (e.g. "Male").
- sklearn splits binary features at threshold 0.5, so:
    answer YES (1) -> go to the RIGHT child (X > 0.5)
    answer NO  (0) -> go to the LEFT  child (X <= 0.5)
- When we land on a leaf node, the tree's majority class at that leaf
  is our best guess.
"""

import os
import joblib

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "akinator_model.pkl")
META_PATH = os.path.join(MODEL_DIR, "akinator_meta.pkl")

# Friendlier phrasing for feature names -> questions.
QUESTION_TEMPLATES = {
    "Real": "Is your character a real person (not fictional)?",
    "Male": "Is your character male?",
    "Indian": "Is your character Indian?",
    "Actor": "Is your character an actor?",
    "Singer": "Is your character a singer?",
    "Athlete": "Is your character an athlete?",
    "Politician": "Is your character a politician?",
    "YouTuber": "Is your character a YouTuber?",
    "Cricketer": "Is your character associated with cricket?",
    "Footballer": "Is your character associated with football (soccer)?",
    "Fictional": "Is your character fictional?",
    "Superhero": "Is your character a superhero?",
    "Animated": "Is your character from a cartoon/animation?",
    "Comedian": "Is your character a comedian?",
    "Scientist": "Is your character a scientist or inventor?",
    # --- cricket differentiator columns (10-cricketer dataset) ---
    "Batsman": "Is your player primarily known as a batsman?",
    "Bowler": "Is your player primarily known as a bowler?",
    "AllRounder": "Is your player known as an all-rounder (bats and bowls)?",
    "WicketKeeper": "Is your player a wicketkeeper?",
    "IsCurrentCaptain": "Is your player currently their team's captain?",
}


def question_for_feature(feature_name: str) -> str:
    return QUESTION_TEMPLATES.get(feature_name, f"Is your character '{feature_name}'?")


class AkinatorModel:
    """Wraps the trained sklearn DecisionTreeClassifier for tree-walking."""

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        meta = joblib.load(META_PATH)
        self.feature_names = meta["feature_names"]
        self.characters = meta["characters"]
        self.accuracy = meta["accuracy"]
        self.tree = self.model.tree_
        self.classes_ = self.model.classes_
        # Rough max depth, used only to render a progress bar.
        self.max_depth = self.model.get_depth()

    def is_leaf(self, node_id: int) -> bool:
        return self.tree.feature[node_id] == -2

    def feature_at(self, node_id: int) -> str:
        idx = self.tree.feature[node_id]
        return self.feature_names[idx]

    def next_child(self, node_id: int, answer: bool) -> int:
        """answer=True (YES/1) -> right child, answer=False (NO/0) -> left child."""
        return self.tree.children_right[node_id] if answer else self.tree.children_left[node_id]

    def guess_at(self, node_id: int):
        """Return (character, confidence) for the majority class at this node."""
        values = self.tree.value[node_id][0]
        total = values.sum()
        best_idx = values.argmax()
        confidence = float(values[best_idx] / total) if total > 0 else 0.0
        character = self.classes_[best_idx]
        return character, confidence


_model_singleton = None


def get_model() -> AkinatorModel:
    global _model_singleton
    if _model_singleton is None:
        _model_singleton = AkinatorModel()
    return _model_singleton


class GameSession:
    """Tracks one player's progress walking down the tree."""

    def __init__(self, akinator: AkinatorModel):
        self.akinator = akinator
        self.node_id = 0  # root
        self.questions_asked = 0
        self.excluded_characters = set()  # characters the user already said "no" to
        self.finished = False

    def reset(self):
        self.node_id = 0
        self.questions_asked = 0
        self.excluded_characters = set()
        self.finished = False

    def current_step(self):
        """
        Returns a dict describing what the frontend should show next:
        either a question, or a final guess.
        """
        node_id = self.node_id
        akinator = self.akinator

        # Skip past any leaf whose guess we've already ruled out (wrong-guess flow).
        while akinator.is_leaf(node_id) and akinator.guess_at(node_id)[0] in self.excluded_characters:
            # No further tree info available past a leaf -> fall back to "unknown".
            break

        if akinator.is_leaf(node_id):
            character, confidence = akinator.guess_at(node_id)
            if character in self.excluded_characters:
                return {
                    "done": True,
                    "prediction": None,
                    "confidence": 0.0,
                    "question": None,
                    "progress": 100,
                    "message": "I'm out of guesses! You stumped me.",
                }
            self.finished = True
            progress = 100
            return {
                "done": True,
                "prediction": character,
                "confidence": round(confidence, 2),
                "question": None,
                "progress": progress,
            }

        feature_name = akinator.feature_at(node_id)
        progress = min(
            95, int((self.questions_asked / max(akinator.max_depth, 1)) * 100))
        return {
            "done": False,
            "prediction": None,
            "confidence": None,
            "question": question_for_feature(feature_name),
            "feature": feature_name,
            "progress": progress,
            "question_number": self.questions_asked + 1,
            "max_questions": akinator.max_depth,
        }

    def answer(self, is_yes: bool):
        """Advance the tree according to the user's answer."""
        akinator = self.akinator
        if akinator.is_leaf(self.node_id):
            return self.current_step()
        self.node_id = akinator.next_child(self.node_id, is_yes)
        self.questions_asked += 1
        return self.current_step()

    def reject_current_guess(self):
        """Called when the user says the final guess was WRONG."""
        character, _ = self.akinator.guess_at(self.node_id)
        self.excluded_characters.add(character)
        return self.current_step()
