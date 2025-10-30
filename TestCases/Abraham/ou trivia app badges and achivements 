#Abraham Gutu 
# ou trivia app badges and achivements 
# Badges & Achievements engine for the University of Oklahoma Trivia app
# Pure Python, no external deps. Plug into your app’s event flow.

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from datetime import datetime, date, timedelta
import json
import os

# ----------------------------
# Events (app emits these)
# ----------------------------

class Event: ...
@dataclass
class QuizFinished(Event):
    user_id: str
    category: str              # e.g., "OU History", "Athletics", "Campus Life"
    correct: int
    total: int
    score: float               # 0..100
    finished_at: datetime

@dataclass
class UserLogin(Event):
    user_id: str
    when: datetime

@dataclass
class AnswerResult(Event):
    user_id: str
    is_correct: bool
    when: datetime
    category: Optional[str] = None


# ----------------------------
# Player State
# ----------------------------

@dataclass
class PlayerStats:
    user_id: str
    total_quizzes: int = 0
    total_correct: int = 0
    total_questions: int = 0
    best_streak: int = 0
    current_streak: int = 0
    last_answer_day: Optional[date] = None
    daily_login_streak: int = 0
    last_login_day: Optional[date] = None
    categories_mastered: Set[str] = field(default_factory=set)
    category_quizzes: Dict[str, int] = field(default_factory=dict)
    # progress trackers for multi-step achievements
    counters: Dict[str, int] = field(default_factory=dict)

    def on_answer(self, correct: bool, when: datetime):
        # Maintain per-day streak of *consecutive correct answers*
        self.total_questions += 1
        if correct:
            self.total_correct += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
        self.last_answer_day = when.date()

    def on_quiz_finished(self, q: QuizFinished):
        self.total_quizzes += 1
        self.category_quizzes[q.category] = self.category_quizzes.get(q.category, 0) + 1
        # Example “mastery”: ≥90 score marks category as mastered
        if q.score >= 90.0:
            self.categories_mastered.add(q.category)

    def on_login(self, when: datetime):
        today = when.date()
        if self.last_login_day is None:
            self.daily_login_streak = 1
        else:
            delta = (today - self.last_login_day).days
            if delta == 1:
                self.daily_login_streak += 1
            elif delta == 0:
                # same day—do nothing
                pass
            else:
                self.daily_login_streak = 1
        self.last_login_day = today


# ----------------------------
# Storage (swap in JSON or your DB)
# ----------------------------

class StorageBackend:
    def load_user(self, user_id: str) -> Tuple[PlayerStats, Set[str]]:
        raise NotImplementedError
    def save_user(self, stats: PlayerStats, earned_badge_ids: Set[str]) -> None:
        raise NotImplementedError

class InMemoryStorage(StorageBackend):
    def __init__(self):
        self._stats: Dict[str, PlayerStats] = {}
        self._earned: Dict[str, Set[str]] = {}

    def load_user(self, user_id: str) -> Tuple[PlayerStats, Set[str]]:
        return (self._stats.setdefault(user_id, PlayerStats(user_id=user_id)),
                self._earned.setdefault(user_id, set()))

    def save_user(self, stats: PlayerStats, earned_badge_ids: Set[str]) -> None:
        self._stats[stats.user_id] = stats
        self._earned[stats.user_id] = earned_badge_ids

class JSONFileStorage(StorageBackend):
    def __init__(self, path="ou_trivia_badges.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({"stats": {}, "earned": {}}, f)

    def _load_all(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _save_all(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load_user(self, user_id: str) -> Tuple[PlayerStats, Set[str]]:
        data = self._load_all()
        s = data["stats"].get(user_id)
        if s is None:
            stats = PlayerStats(user_id=user_id)
        else:
            # reconstruct sets
            stats = PlayerStats(
                user_id=s["user_id"],
                total_quizzes=s["total_quizzes"],
                total_correct=s["total_correct"],
                total_questions=s["total_questions"],
                best_streak=s["best_streak"],
                current_streak=s["current_streak"],
                last_answer_day=date.fromisoformat(s["last_answer_day"]) if s["last_answer_day"] else None,
                daily_login_streak=s["daily_login_streak"],
                last_login_day=date.fromisoformat(s["last_login_day"]) if s["last_login_day"] else None,
                categories_mastered=set(s["categories_mastered"]),
                category_quizzes=dict(s["category_quizzes"]),
                counters=dict(s["counters"]),
            )
        earned = set(data["earned"].get(user_id, []))
        return stats, earned

    def save_user(self, stats: PlayerStats, earned_badge_ids: Set[str]) -> None:
        data = self._load_all()
        s = asdict(stats)
        # convert dates to iso strings; sets to lists
        s["last_answer_day"] = s["last_answer_day"].isoformat() if s["last_answer_day"] else None
        s["last_login_day"] = s["last_login_day"].isoformat() if s["last_login_day"] else None
        s["categories_mastered"] = list(stats.categories_mastered)
        data["stats"][stats.user_id] = s
        data["earned"][stats.user_id] = list(earned_badge_ids)
        self._save_all(data)


# ----------------------------
# Requirements (rules)
# ----------------------------

class Requirement:
    def is_met(self, stats: PlayerStats) -> bool:
        raise NotImplementedError
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        """Return (current, goal) for progress bars when possible."""
        return (0, 1)

@dataclass
class MinQuizzesRequirement(Requirement):
    n: int
    def is_met(self, stats: PlayerStats) -> bool:
        return stats.total_quizzes >= self.n
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        return (min(stats.total_quizzes, self.n), self.n)

@dataclass
class MinCorrectAnswersRequirement(Requirement):
    n: int
    def is_met(self, stats: PlayerStats) -> bool:
        return stats.total_correct >= self.n
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        return (min(stats.total_correct, self.n), self.n)

@dataclass
class StreakRequirement(Requirement):
    n: int
    def is_met(self, stats: PlayerStats) -> bool:
        return stats.best_streak >= self.n
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        return (min(stats.best_streak, self.n), self.n)

@dataclass
class ScoreRequirement(Requirement):
    min_score: float
    count: int = 1
    category: Optional[str] = None
    # Count how many quizzes at/above min_score (optionally within a category)
    def is_met(self, stats: PlayerStats) -> bool:
        key = self._counter_key()
        return stats.counters.get(key, 0) >= self.count
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        key = self._counter_key()
        return (min(stats.counters.get(key, 0), self.count), self.count)
    def _counter_key(self) -> str:
        return f"score_{self.min_score}_{self.category or 'any'}"

@dataclass
class CategoryMasterRequirement(Requirement):
    category: str
    def is_met(self, stats: PlayerStats) -> bool:
        return self.category in stats.categories_mastered

@dataclass
class DailyLoginStreakRequirement(Requirement):
    n: int
    def is_met(self, stats: PlayerStats) -> bool:
        return stats.daily_login_streak >= self.n
    def progress(self, stats: PlayerStats) -> Tuple[int, int]:
        return (min(stats.daily_login_streak, self.n), self.n)


# ----------------------------
# Badge & Achievement Models
# ----------------------------

@dataclass(frozen=True)
class Badge:
    id: str
    name: str
    description: str
    points: int
    requirement: Requirement
    icon: Optional[str] = None       # e.g., "🏛️" or asset key

@dataclass
class AwardResult:
    newly_awarded: List[Badge]
    already_had: List[Badge]
    progress: Dict[str, Tuple[int, int]]  # badge_id -> (current, goal)


# ----------------------------
# Catalog (define OU-themed badges)
# ----------------------------

def ou_badge_catalog() -> List[Badge]:
    return [
        Badge(
            id="first_boomer",
            name="First Boomer",
            description="Complete your first OU trivia quiz.",
            points=25,
            requirement=MinQuizzesRequirement(1),
            icon="🎓",
        ),
        Badge(
            id="tenacious_sooner",
            name="Tenacious Sooner",
            description="Answer 10 questions correctly overall.",
            points=50,
            requirement=MinCorrectAnswersRequirement(10),
            icon="💪",
        ),
        Badge(
            id="boomer_streak_5",
            name="On a Roll (x5)",
            description="Reach a 5-answer correct streak.",
            points=75,
            requirement=StreakRequirement(5),
            icon="🔥",
        ),
        Badge(
            id="campus_expert_90",
            name="Campus Expert",
            description="Score 90+ on any quiz.",
            points=100,
            requirement=ScoreRequirement(min_score=90, count=1),
            icon="🏆",
        ),
        Badge(
            id="history_master",
            name="History Master",
            description="Master the OU History category (score ≥90 on a quiz).",
            points=120,
            requirement=CategoryMasterRequirement("OU History"),
            icon="📜",
        ),
        Badge(
            id="athletics_ace",
            name="Athletics Ace",
            description="Master the Athletics category (score ≥90 on a quiz).",
            points=120,
            requirement=CategoryMasterRequirement("Athletics"),
            icon="🏈",
        ),
        Badge(
            id="loyal_sooner_7",
            name="Loyal Sooner (7-day)",
            description="Log in 7 days in a row.",
            points=150,
            requirement=DailyLoginStreakRequirement(7),
            icon="📆",
        ),
        Badge(
            id="academic_all_star",
            name="Academic All-Star",
            description="Score 90+ on 3 quizzes (any categories).",
            points=200,
            requirement=ScoreRequirement(min_score=90, count=3),
            icon="⭐",
        ),
    ]


# ----------------------------
# Engine
# ----------------------------

class BadgeEngine:
    def __init__(self, storage: StorageBackend, catalog: Optional[List[Badge]] = None):
        self.storage = storage
        self.catalog = catalog or ou_badge_catalog()
        # For quick lookups
        self._by_id: Dict[str, Badge] = {b.id: b for b in self.catalog}

    # Public API you’ll call from your app:
    def process(self, event: Event) -> AwardResult:
        if isinstance(event, QuizFinished):
            return self._on_quiz_finished(event)
        elif isinstance(event, AnswerResult):
            return self._on_answer(event)
        elif isinstance(event, UserLogin):
            return self._on_login(event)
        else:
            return AwardResult([], [], {})

    def get_user_badges(self, user_id: str) -> List[Badge]:
        _, earned = self.storage.load_user(user_id)
        return [self._by_id[b_id] for b_id in earned if b_id in self._by_id]

    def get_progress(self, user_id: str) -> Dict[str, Tuple[int, int]]:
        stats, earned = self.storage.load_user(user_id)
        prog = {}
        for b in self.catalog:
            if b.id in earned:
                continue
            try:
                prog[b.id] = b.requirement.progress(stats)
            except Exception:
                pass
        return prog

    # ---- internal handlers ----

    def _on_answer(self, e: AnswerResult) -> AwardResult:
        stats, earned = self.storage.load_user(e.user_id)
        stats.on_answer(e.is_correct, e.when)
        self.storage.save_user(stats, earned)  # save interim (streaks, etc.)
        return self._evaluate_and_award(stats, earned)

    def _on_login(self, e: UserLogin) -> AwardResult:
        stats, earned = self.storage.load_user(e.user_id)
        stats.on_login(e.when)
        self.storage.save_user(stats, earned)
        return self._evaluate_and_award(stats, earned)

    def _on_quiz_finished(self, q: QuizFinished) -> AwardResult:
        stats, earned = self.storage.load_user(q.user_id)
        # Track score counters for achievements like “90+ score N times”
        self._bump_score_counters(stats, q)
        stats.on_quiz_finished(q)
        self.storage.save_user(stats, earned)
        return self._evaluate_and_award(stats, earned)

    def _bump_score_counters(self, stats: PlayerStats, q: QuizFinished):
        # for ScoreRequirement
        if q.score >= 0:
            any_key = f"score_{90.0}_{'any'}"
            # Only increment “≥90” counter when it qualifies
            if q.score >= 90.0:
                stats.counters[any_key] = stats.counters.get(any_key, 0) + 1
                cat_key = f"score_{90.0}_{q.category}"
                stats.counters[cat_key] = stats.counters.get(cat_key, 0) + 1

    def _evaluate_and_award(self, stats: PlayerStats, earned: Set[str]) -> AwardResult:
        newly: List[Badge] = []
        already: List[Badge] = []
        progress: Dict[str, Tuple[int, int]] = {}

        for badge in self.catalog:
            if badge.id in earned:
                already.append(badge)
                continue
            met = False
            try:
                met = badge.requirement.is_met(stats)
                progress[badge.id] = badge.requirement.progress(stats)
            except Exception:
                pass
            if met:
                earned.add(badge.id)
                newly.append(badge)

        self.storage.save_user(stats, earned)
        return AwardResult(newly_awarded=newly, already_had=already, progress=progress)


# ----------------------------
# Simple demo / reference usage
# ----------------------------

if __name__ == "__main__":
    engine = BadgeEngine(storage=InMemoryStorage())

    uid = "student:ou:abraham"

    # Day 1 login
    r1 = engine.process(UserLogin(user_id=uid, when=datetime.now()))
    # Correct answers
    for _ in range(5):
        engine.process(AnswerResult(user_id=uid, is_correct=True, when=datetime.now()))
    # Finish a quiz with a 92 in OU History
    r2 = engine.process(QuizFinished(
        user_id=uid, category="OU History", correct=23, total=25, score=92.0, finished_at=datetime.now()
    ))

    # Print newly earned badges
    print("Newly awarded:")
    for b in r2.newly_awarded:
        print(f"- {b.name} (+{b.points})")

    # Show progress bars for not-yet-earned badges
    print("\nProgress:")
    prog = engine.get_progress(uid)
    for bid, (cur, goal) in prog.items():
        badge = engine._by_id[bid]
        print(f"- {badge.name}: {cur}/{goal}")
