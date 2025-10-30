import unittest
from datetime import datetime, timedelta


from your_module_name import (   # ← change this to your filename (no .py)
    BadgeEngine,
    InMemoryStorage,
    UserLogin,
    AnswerResult,
    QuizFinished,
)

class TestOUTriviaBadges(unittest.TestCase):

    def setUp(self):
        self.storage = InMemoryStorage()
        self.engine = BadgeEngine(self.storage)
        self.user_id = "student:ou:abraham"

    def test_first_quiz_earns_first_boomer(self):
        """Finishing 1 quiz should give the 'first_boomer' badge."""
        res = self.engine.process(QuizFinished(
            user_id=self.user_id,
            category="OU History",
            correct=5,
            total=5,
            score=100.0,
            finished_at=datetime.now()
        ))
        ids = {b.id for b in res.newly_awarded}
        self.assertIn("first_boomer", ids)

    def test_ten_correct_answers_earns_tenacious_sooner(self):
        """Answering 10 questions correctly overall should award 'tenacious_sooner'."""
        now = datetime.now()
        # 10 correct answers, separate events
        for i in range(10):
            self.engine.process(AnswerResult(
                user_id=self.user_id,
                is_correct=True,
                when=now + timedelta(seconds=i)
            ))

        # final state after 10th answer
        # the last event should include the badge in newly_awarded
        res = self.engine.process(AnswerResult(
            user_id=self.user_id,
            is_correct=True,
            when=now + timedelta(seconds=11)
        ))
        ids = {b.id for b in res.newly_awarded}
        self.assertIn("tenacious_sooner", ids)

    def test_90_plus_quiz_in_history_gives_campus_and_history(self):
        """Scoring 90+ in OU History should give both general 90+ and history master."""
        res = self.engine.process(QuizFinished(
            user_id=self.user_id,
            category="OU History",
            correct=18,
            total=20,
            score=90.0,
            finished_at=datetime.now()
        ))
        ids = {b.id for b in res.newly_awarded}
        # campus_expert_90 comes from ScoreRequirement(min_score=90, count=1)
        self.assertIn("campus_expert_90", ids)
        # history_master comes from CategoryMasterRequirement("OU History")
        self.assertIn("history_master", ids)

    def test_7_day_login_streak_awards_loyal_sooner(self):
        """7 consecutive daily logins → 'loyal_sooner_7'."""
        base = datetime(2025, 1, 1, 9, 0, 0)
        last_res = None
        for i in range(7):
            last_res = self.engine.process(UserLogin(
                user_id=self.user_id,
                when=base + timedelta(days=i)
            ))
        ids = {b.id for b in last_res.newly_awarded}
        self.assertIn("loyal_sooner_7", ids)

    def test_progress_shows_unearned_badges(self):
        """Progress API should return entries for badges not yet earned."""
        # no events yet
        prog = self.engine.get_progress(self.user_id)
        # we have a known badge in catalog
        self.assertIn("first_boomer", prog)
        current, goal = prog["first_boomer"]
        self.assertEqual(current, 0)
        self.assertEqual(goal, 1)


if __name__ == "__main__":
    unittest.main()
