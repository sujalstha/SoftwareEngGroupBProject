"""
QuizTimer Feature – Standalone Version
For reuse in OU Trivia App or other projects.
Implements a countdown timer with callbacks.
"""
import time
import threading

class QuizTimer:
    def __init__(self, duration, update_callback, finish_callback):
        """Initialize the QuizTimer.
        Args:
            duration (int): Total time in seconds.
            update_callback (function): Called every second with remaining time.
            finish_callback (function): Called once when timer reaches 0.
        """
        self.duration = duration
        self.remaining = duration
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self.running = False
        self.thread = None

    def start(self):
        """Starts the countdown timer in a background thread."""
        self.running = True
        self.remaining = self.duration
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        """Internal function that decreases remaining time every second."""
        while self.running and self.remaining > 0:
            time.sleep(1)
            self.remaining -= 1
            self.update_callback(self.remaining)
        if self.remaining == 0 and self.running:
            self.finish_callback()

    def stop(self):
        """Stops the timer manually (pauses countdown)."""
        self.running = False

    def reset(self):
        """Stops and resets timer to its original duration."""
        self.stop()
        self.remaining = self.duration


# Example usage demonstration
if __name__ == "__main__":
    def show_update(remaining):
        print(f"Time left: {remaining}s")

    def finished():
        print("Time's up!")

    timer = QuizTimer(5, show_update, finished)
    print("Starting 5-second timer...")
    timer.start()
    time.sleep(3)
    print("Stopping early at 3s.")
    timer.stop()
    print("Restarting...")
    timer.start()
    time.sleep(6)
    print("Done.")
