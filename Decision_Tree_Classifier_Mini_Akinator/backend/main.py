"""
main.py
-------
FastAPI backend for Mini-Akinator.

Endpoints:
  POST /start   -> begin a new game, returns session_id + first question
  POST /answer  -> submit yes/no for the current question, returns next
                    question OR a final guess
  POST /predict -> get the current best guess without advancing
  POST /reset   -> reset a session back to the start (or wipe a wrong guess)

Run with:
    uvicorn main:app --reload --port 8000
"""

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_utils import get_model, GameSession

app = FastAPI(title="Mini-Akinator API")

# Allow the frontend (served separately / opened as a file) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

akinator = get_model()
SESSIONS: dict[str, GameSession] = {}


class AnswerRequest(BaseModel):
    session_id: str
    answer: bool  # True = YES, False = NO


class GuessFeedbackRequest(BaseModel):
    session_id: str
    correct: bool  # True = the guess was right, False = wrong


class ResetRequest(BaseModel):
    session_id: str | None = None


def _get_session(session_id: str) -> GameSession:
    session = SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=404, detail="Session not found. Call /start first.")
    return session


@app.post("/start")
def start_game():
    session_id = str(uuid.uuid4())
    session = GameSession(akinator)
    SESSIONS[session_id] = session
    step = session.current_step()
    return {"session_id": session_id, **step}


@app.post("/answer")
def answer_question(req: AnswerRequest):
    session = _get_session(req.session_id)
    step = session.answer(req.answer)
    return {"session_id": req.session_id, **step}


@app.post("/predict")
def predict(req: ResetRequest):
    if not req.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    session = _get_session(req.session_id)
    step = session.current_step()
    return {"session_id": req.session_id, **step}


@app.post("/guess-feedback")
def guess_feedback(req: GuessFeedbackRequest):
    """Call this after showing the final guess: was it correct?"""
    session = _get_session(req.session_id)
    if req.correct:
        return {"session_id": req.session_id, "message": "🎉 Got it right!"}
    step = session.reject_current_guess()
    return {"session_id": req.session_id, **step}


@app.post("/reset")
def reset_game(req: ResetRequest):
    if req.session_id and req.session_id in SESSIONS:
        SESSIONS[req.session_id].reset()
        step = SESSIONS[req.session_id].current_step()
        return {"session_id": req.session_id, **step}
    # No valid session -> just start a fresh one
    return start_game()


@app.get("/health")
def health():
    return {"status": "ok", "characters": len(akinator.characters), "accuracy": akinator.accuracy}
