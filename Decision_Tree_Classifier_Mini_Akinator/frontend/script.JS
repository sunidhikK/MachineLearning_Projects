// ============================================================
// Mini Akinator — frontend logic
// Talks to the FastAPI backend at API_BASE and drives the
// screens defined in index.html purely by toggling the
// "active" class on <section class="screen" id="screen-...">.
// ============================================================

const API_BASE = "http://127.0.0.1:8000";

// ---- element refs ----
const screens = {
    landing: document.getElementById("screen-landing"),
    question: document.getElementById("screen-question"),
    guess: document.getElementById("screen-guess"),
    correct: document.getElementById("screen-correct"),
    wrong: document.getElementById("screen-wrong"),
    stumped: document.getElementById("screen-stumped"),
};

const genie = document.getElementById("genie");
const thinkingOverlay = document.getElementById("thinking-overlay");
const apiStatus = document.getElementById("api-status");

const speechBubble = document.getElementById("speech-bubble");
const questionText = document.getElementById("question-text");
const btnYes = document.getElementById("btn-yes");
const btnNo = document.getElementById("btn-no");
const progressLabel = document.getElementById("progress-label");
const progressFill = document.getElementById("progress-fill");

const guessName = document.getElementById("guess-name");
const guessConfidence = document.getElementById("guess-confidence");
const btnGuessYes = document.getElementById("btn-guess-yes");
const btnGuessNo = document.getElementById("btn-guess-no");

const correctName = document.getElementById("correct-name");
const confettiLayer = document.getElementById("confetti-layer");

const btnStart = document.getElementById("btn-start");
const btnContinue = document.getElementById("btn-continue");
const btnPlayAgain1 = document.getElementById("btn-play-again-1");
const btnPlayAgain2 = document.getElementById("btn-play-again-2");
const btnPlayAgain3 = document.getElementById("btn-play-again-3");

// ---- state ----
let sessionId = null;
let pendingStep = null; // step to reveal after the "wrong" screen's Continue click

// ---- screen helpers ----
function showScreen(name) {
    Object.values(screens).forEach((el) => el.classList.remove("active"));
    screens[name].classList.add("active");
}

function setGenieState(state) {
    genie.classList.remove("thinking", "excited", "correct", "wrong");
    if (state) genie.classList.add(state);
}

function setThinking(isThinking) {
    thinkingOverlay.classList.toggle("active", isThinking);
    setGenieState(isThinking ? "thinking" : null);
}

// ---- API helper ----
async function api(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body || {}),
    });
    if (!res.ok) {
        throw new Error(`Request to ${path} failed: ${res.status}`);
    }
    return res.json();
}

// ---- render a "step" returned by the backend ----
function renderStep(step) {
    if (step.session_id) sessionId = step.session_id;

    if (step.done) {
        if (step.prediction) {
            renderGuess(step);
        } else {
            renderStumped();
        }
        return;
    }

    renderQuestion(step);
}

function renderQuestion(step) {
    setGenieState("excited");
    questionText.textContent = step.question;
    progressLabel.textContent = `Question ${step.question_number || 1}`;
    progressFill.style.width = `${step.progress || 0}%`;
    speechBubble.textContent = "Hmm...";
    showScreen("question");
}

function renderGuess(step) {
    setGenieState("excited");
    guessName.textContent = String(step.prediction).toUpperCase();
    const pct = Math.round((step.confidence || 0) * 100);
    guessConfidence.textContent = `${pct}% sure`;
    showScreen("guess");
}

function renderStumped() {
    setGenieState(null);
    showScreen("stumped");
}

function launchConfetti() {
    confettiLayer.innerHTML = "";
    const colors = ["#8b5cf6", "#22d3ee", "#fbbf24", "#34d399", "#f87171"];
    for (let i = 0; i < 24; i++) {
        const piece = document.createElement("div");
        piece.className = "confetti-piece";
        piece.style.left = `${Math.random() * 100}%`;
        piece.style.background = colors[i % colors.length];
        piece.style.animationDelay = `${Math.random() * 0.4}s`;
        confettiLayer.appendChild(piece);
    }
}

// ---- flow actions ----
async function startGame() {
    try {
        setThinking(true);
        apiStatus.textContent = "";
        const step = await api("/start");
        setThinking(false);
        renderStep(step);
    } catch (err) {
        setThinking(false);
        apiStatus.textContent = "Could not reach the backend. Is uvicorn running?";
        console.error(err);
    }
}

async function sendAnswer(isYes) {
    try {
        setThinking(true);
        const step = await api("/answer", { session_id: sessionId, answer: isYes });
        setThinking(false);
        renderStep(step);
    } catch (err) {
        setThinking(false);
        apiStatus.textContent = "Something went wrong talking to the backend.";
        console.error(err);
    }
}

async function confirmGuess(wasCorrect) {
    try {
        setThinking(true);
        const step = await api("/guess-feedback", { session_id: sessionId, correct: wasCorrect });
        setThinking(false);

        if (wasCorrect) {
            setGenieState("correct");
            correctName.textContent = guessName.textContent;
            showScreen("correct");
            launchConfetti();
        } else {
            // Stash whatever the backend wants to show next (another guess,
            // or "stumped"), and reveal it once the user clicks Continue.
            pendingStep = step;
            setGenieState("wrong");
            showScreen("wrong");
        }
    } catch (err) {
        setThinking(false);
        apiStatus.textContent = "Something went wrong talking to the backend.";
        console.error(err);
    }
}

function continueAfterWrong() {
    if (pendingStep) {
        renderStep(pendingStep);
        pendingStep = null;
    } else {
        startGame();
    }
}

// ---- wire up events ----
btnStart.addEventListener("click", startGame);

btnYes.addEventListener("click", () => sendAnswer(true));
btnNo.addEventListener("click", () => sendAnswer(false));

btnGuessYes.addEventListener("click", () => confirmGuess(true));
btnGuessNo.addEventListener("click", () => confirmGuess(false));

btnContinue.addEventListener("click", continueAfterWrong);

btnPlayAgain1.addEventListener("click", startGame);
btnPlayAgain2.addEventListener("click", startGame);
btnPlayAgain3.addEventListener("click", startGame);