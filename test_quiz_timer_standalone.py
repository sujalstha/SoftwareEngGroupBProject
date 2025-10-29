# test_quiz_timer_standalone.py
"""
Pytest tests for the standalone QuizTimer feature.

Run:
    pytest -q

Assumes:
    - quiz_timer_feature.py exports `QuizTimer`
"""
import time
from threading import Event
import pytest

from quiz_timer_feature import QuizTimer


@pytest.fixture
def tracker():
    """
    Shared test fixture providing:
      - updates: list recording each update_callback(remaining)
      - finished: Event set by finish_callback()
      - on_update, on_finish: callbacks for the timer
    """
    updates = []
    finished = Event()

    def on_update(remaining: int):
        updates.append(remaining)

    def on_finish():
        finished.set()

    return updates, finished, on_update, on_finish


def test_counts_down_and_calls_finish(tracker):
    updates, finished, on_update, on_finish = tracker

    timer = QuizTimer(3, on_update, on_finish)
    start = time.time()
    timer.start()

    # Wait slightly longer than the duration for callbacks to fire
    assert finished.wait(timeout=5), "finish_callback should be called when time reaches 0"

    elapsed = time.time() - start
    # Updates should include 0 at the end of the countdown
    assert 0 in updates, "Updates should include 0 at the end of the countdown"
    # Should not have more than 3 ticks for a 3-second timer
    assert len(updates) <= 3, "Should not tick more than once per second for a 3-second timer"
    # Rough timing sanity check (allow small jitter)
    assert elapsed >= 2.8, "Elapsed should roughly match the duration (allowing for small jitter)"


def test_stop_prevents_finish(tracker):
    updates, finished, on_update, _ = tracker

    stop_called = Event()

    def on_finish_never():
        stop_called.set()

    timer = QuizTimer(5, on_update, on_finish_never)
    timer.start()
    time.sleep(1.6)  # allow at least one tick
    timer.stop()
    time.sleep(1.0)  # give time to ensure no finish after stop

    assert not stop_called.is_set(), "finish_callback must not run after stop()"
    assert len(updates) >= 1, "Should have at least one tick before stopping"


def test_reset_restores_remaining_and_stops(tracker):
    _, finished, on_update, on_finish = tracker

    timer = QuizTimer(4, on_update, on_finish)
    timer.start()
    time.sleep(1.2)
    timer.reset()

    assert timer.remaining == 4, "reset() should restore original duration"
    assert not timer.running, "reset() should also stop the timer"
    assert not finished.is_set(), "finish_callback should not be called after reset()"


def test_zero_duration_immediate_finish(tracker):
    updates, finished, on_update, _ = tracker

    immediate = Event()

    def done():
        immediate.set()

    timer = QuizTimer(0, on_update, done)
    timer.start()

    assert immediate.wait(timeout=1.0), "Timer with 0 duration should call finish immediately"
    # update_callback may not be called at all for zero-duration; don't strictly require it.
    # If your implementation does call update(0), this will still pass:
    assert 0 in (updates or [0]), "Update should report 0 when starting at zero duration"


def test_multiple_starts_behave_like_restart(tracker):
    """
    Restart semantics: safest pattern is stop() then start() again.
    This avoids overlapping threads in a simple timer implementation.
    """
    _, finished, on_update, on_finish = tracker

    timer = QuizTimer(3, on_update, on_finish)
    timer.start()
    time.sleep(1.2)
    timer.stop()    # ensure old thread is halted before restarting
    timer.start()   # restart fresh

    assert finished.wait(timeout=4.5), "Timer should eventually finish after restart"
