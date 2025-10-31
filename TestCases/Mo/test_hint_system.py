"""
Pytest unit tests for HintSystem

How to run:
    pip install pytest
    pytest -q

These tests exercise:
- Loading 5 questions from a temp JSONL
- AI-success path (mocked)
- AI-failure fallback to local hint (mocked exception)
- Local-only mode (prefer_ai=False)
- Missing-file error behavior
"""
from __future__ import annotations

import json
import os
import types
import pytest

# Import the production module
import hint_system as hs


# -----------------
# Helpers / Fixtures
# -----------------

@pytest.fixture
def five_questions(tmp_path):
    """Create a temp JSONL with 5 questions and return (path, questions_list)."""
    p = tmp_path / "questions.jsonl"
    data = [
        {"id": 1, "question": "Who is the current OU football head coach?", "answer": "Brent Venables", "hint_local": "Defensive-minded coach who returned in 2021."},
        {"id": 2, "question": "What is the nickname of the University of Oklahoma?", "answer": "Sooners", "hint_local": "It comes from settlers who moved in a bit too early."},
        {"id": 3, "question": "What city is the OU main campus located in?", "answer": "Norman", "hint_local": "South of OKC along I-35."},
        {"id": 4, "question": "Which student newspaper covers OU campus news?", "answer": "The OU Daily", "hint_local": "It's the independent student-run outlet."},
        {"id": 5, "question": "What are OU's school colors?", "answer": "Crimson and Cream", "hint_local": "Two colors—one deep red, one off-white."},
    ]
    with p.open("w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    # Also return parsed Question objects for convenience
    qs = hs.load_questions_jsonl(p)
    return p, qs


# ---------
# Test cases
# ---------

def test_loads_five_questions(five_questions):
    path, qs = five_questions
    assert len(qs) == 5
    assert all(isinstance(q.id, int) for q in qs)
    assert all(q.hint_local for q in qs)


def test_ai_success_path(monkeypatch, five_questions):
    """When AI returns a hint, it should be used (not the local one)."""
    _, qs = five_questions

    # Monkeypatch AIHintStrategy.get_hint to simulate success
    def fake_ai_success(self, q):
        return "(AI) short non-spoiler hint"

    monkeypatch.setattr(hs.AIHintStrategy, "get_hint", fake_ai_success, raising=True)

    service = hs.HintService(prefer_ai=True)
    got = service.get_hint(qs[0])
    assert got == "(AI) short non-spoiler hint"


def test_ai_failure_fallback_to_local(monkeypatch, five_questions):
    """On AI error, fallback to local hint silently."""
    _, qs = five_questions

    def fake_ai_fail(self, q):
        raise RuntimeError("simulated AI failure")

    monkeypatch.setattr(hs.AIHintStrategy, "get_hint", fake_ai_fail, raising=True)

    service = hs.HintService(prefer_ai=True)
    got = service.get_hint(qs[1])
    assert got == qs[1].hint_local


def test_local_only_mode_ignores_ai(monkeypatch, five_questions):
    """With prefer_ai=False, system should return local hints and never call AI."""
    _, qs = five_questions

    calls = {"ai": 0}

    def spy_ai(self, q):  # would be called if prefer_ai=True
        calls["ai"] += 1
        return "(AI) should not be used"

    monkeypatch.setattr(hs.AIHintStrategy, "get_hint", spy_ai, raising=True)

    service = hs.HintService(prefer_ai=False)
    got = service.get_hint(qs[2])

    assert got == qs[2].hint_local
    assert calls["ai"] == 0  # AI wasn't touched


def test_missing_file_raises(tmp_path):
    missing = tmp_path / "nope.jsonl"
    with pytest.raises(FileNotFoundError):
        hs.load_questions_jsonl(missing)


def test_hint_system_facade(monkeypatch, five_questions):
    """Smoke-test the small façade used by the UI layer."""
    _, qs = five_questions

    def fake_ai_fail(self, q):
        raise RuntimeError("simulated AI failure")

    monkeypatch.setattr(hs.AIHintStrategy, "get_hint", fake_ai_fail, raising=True)

    system = hs.HintSystem(prefer_ai=True)
    hint = system.hint_for(qs[3])

    assert isinstance(hint, str) and len(hint) > 0
    assert hint == qs[3].hint_local

