"""
HintSystem module for OU Trivia App
----------------------------------

Key ideas
- One hint per question.
- Questions are loaded from a local text file during early development.
- Hints default to locally provided hints, but we *attempt* an AI-generated hint first.
- If AI is unavailable (no key, network fail, etc.), we gracefully fall back to the local hint.

File format for questions (JSONL recommended during dev):
Each line is a JSON object with fields: id, question, answer, hint_local

Example questions.jsonl (put in your repo root for now):
{"id": 1, "question": "Who is the current OU football head coach?", "answer": "Brent Venables", "hint_local": "Defensive-minded coach who returned in 2021."}
{"id": 2, "question": "What is the nickname of the University of Oklahoma?", "answer": "Sooners", "hint_local": "It comes from settlers who moved in a bit too early."}
{"id": 3, "question": "What city is the OU main campus located in?", "answer": "Norman", "hint_local": "South of OKC along I-35."}
{"id": 4, "question": "Which student newspaper covers OU campus news?", "answer": "The OU Daily", "hint_local": "It's the independent student-run outlet."}
{"id": 5, "question": "What are OU's school colors?", "answer": "Crimson and Cream", "hint_local": "Two colors—one deep red, one off-white."}

Drop this file path into QUESTIONS_PATH below.

Later: replace loader with a scraper that writes the same JSONL format so other code remains unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol
import json
import os

# === Config ===
# Point to your dev questions file here
QUESTIONS_PATH = Path("questions.jsonl")
# Toggle/override via env during testing: export USE_AI_HINTS=0/1
USE_AI_HINTS = os.getenv("USE_AI_HINTS", "1") not in {"0", "false", "False"}


# === Data model ===
@dataclass(slots=True)
class Question:
    id: int
    question: str
    answer: str
    hint_local: str


# === Loading ===
def load_questions_jsonl(path: Path = QUESTIONS_PATH) -> List[Question]:
    """Load questions from a JSONL file. One JSON object per line.
    """
    questions: List[Question] = []
    if not path.exists():
        raise FileNotFoundError(f"Questions file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                q = Question(
                    id=int(obj["id"]),
                    question=str(obj["question"]).strip(),
                    answer=str(obj["answer"]).strip(),
                    hint_local=str(obj["hint_local"]).strip(),
                )
                questions.append(q)
            except Exception as e:
                raise ValueError(f"Invalid JSON at line {lineno}: {e}")
    return questions


# === Hint strategies ===
class HintStrategy(Protocol):
    def get_hint(self, q: Question) -> Optional[str]:
        ...


class LocalHintStrategy:
    """Always returns the pre-authored local hint."""

    def get_hint(self, q: Question) -> Optional[str]:
        return q.hint_local or None


class AIHintStrategy:
    """Attempts to generate a hint using an AI API.

    IMPORTANT: During early development you can:
      - leave this class as-is (it will simulate an unavailable AI and raise), OR
      - wire it to your provider (OpenAI, etc.) and return the model's hint string.

    We *never* block the UI; failures route to fallback (LocalHintStrategy).
    """

    def __init__(self, model: str = "gpt-5", timeout_s: int = 6) -> None:
        self.model = model
        self.timeout_s = timeout_s

    def get_hint(self, q: Question) -> Optional[str]:
        # --- Greyed-out / placeholder AI call ---
        # Example skeleton if using OpenAI's python client:
        # import openai
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # if not openai.api_key:
        #     raise RuntimeError("AI unavailable: missing OPENAI_API_KEY")
        # prompt = f"Give a SHORT, non-spoiler hint for this trivia question: {q.question}\nOne sentence only."
        # resp = openai.chat.completions.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}],
        #     timeout=self.timeout_s,
        # )
        # return resp.choices[0].message.content.strip()

        # For now, we deliberately simulate an unavailable AI backend so the
        # fallback path is exercised during dev/testing:
        raise RuntimeError("AI backend not configured (dev stub)")


# === Hint service with graceful fallback ===
class HintService:
    def __init__(self, prefer_ai: bool = USE_AI_HINTS) -> None:
        self.prefer_ai = prefer_ai
        self.local = LocalHintStrategy()
        self.ai = AIHintStrategy()

    def get_hint(self, q: Question) -> str:
        if self.prefer_ai:
            try:
                hint = self.ai.get_hint(q)
                if hint:
                    return hint
            except Exception:
                # Fallback silently to local hints
                pass
        # Local fallback (or preferred when prefer_ai=False)
        hint = self.local.get_hint(q)
        return hint or "(No hint available)"


# === Minimal integration surface ===
class HintSystem:
    """Small façade the UI layer can call from anywhere.

    Usage in your UI code:
        hs = HintSystem()  # create once
        hint_text = hs.hint_for(question_obj)
        hint_label.config(text=hint_text)
    """

    def __init__(self, prefer_ai: bool = USE_AI_HINTS) -> None:
        self.service = HintService(prefer_ai=prefer_ai)

    def hint_for(self, q: Question) -> str:
        return self.service.get_hint(q)


# === Quick manual test ===
if __name__ == "__main__":
    # Create a tiny demo list if file missing, so `python hint_system.py` works out of the box.
    if not QUESTIONS_PATH.exists():
        demo = [
            {"id": 1, "question": "Who is the current OU football head coach?", "answer": "Brent Venables", "hint_local": "Defensive-minded coach who returned in 2021."},
            {"id": 2, "question": "What is the nickname of the University of Oklahoma?", "answer": "Sooners", "hint_local": "It comes from settlers who moved in a bit too early."},
            {"id": 3, "question": "What city is the OU main campus located in?", "answer": "Norman", "hint_local": "South of OKC along I-35."},
            {"id": 4, "question": "Which student newspaper covers OU campus news?", "answer": "The OU Daily", "hint_local": "It's the independent student-run outlet."},
            {"id": 5, "question": "What are OU's school colors?", "answer": "Crimson and Cream", "hint_local": "Two colors—one deep red, one off-white."},
        ]
        with QUESTIONS_PATH.open("w", encoding="utf-8") as f:
            for row in demo:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Wrote demo {QUESTIONS_PATH} with 5 questions.")

    questions = load_questions_jsonl(QUESTIONS_PATH)
    hs = HintSystem(prefer_ai=USE_AI_HINTS)

    for q in questions:
        hint = hs.hint_for(q)
        print(f"Q{q.id}: {q.question}\n  Hint: {hint}\n")
