class DiffSelect:
    def __init__(self):
        self.current_diff = None

    def difficulty_level_sel(self, level: str):
        valid = ["Easy", "Medium", "Hard"]
        if level not in valid:
            raise ValueError("Invalid difficulty selection")

        self.current_diff = level
        return f"Difficulty set to {level}"

    def get_difficulty(self):
        return self.current_diff
