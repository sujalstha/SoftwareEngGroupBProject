class DiffSelect:
    def __init__(self):
        self.current_diff = None

    def difficulty_level_sel(self, level):
        valid_levels = ["Easy", "Medium", "Hard"]

        if level not in valid_levels:
            raise ValueError("Invalid difficulty selection")

        self.current_diff = level
        return f"Difficulty set to {level}"
