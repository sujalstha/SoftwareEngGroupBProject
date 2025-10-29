# DiffSelect.py

class DiffSelect:
    def __init__(self):
        self.current_diff = None

    def difficulty_level_sel(self, diff_selected):
        valid_difficulties = ["Easy", "Medium", "Hard"]

        if diff_selected not in valid_difficulties:
            raise ValueError(f"Invalid difficulty selected: {diff_selected}")

        self.current_diff = diff_selected
        return f"Difficulty set to {diff_selected}"
