
import unittest
from DiffSelect import DiffSelect


class TestDiffSelect(unittest.TestCase):

    def setUp(self):
        self.diff_select = DiffSelect()

    def test_easy_selection(self):
        result = self.diff_select.difficulty_level_sel("Easy")
        self.assertEqual(result, "Difficulty set to Easy")
        self.assertEqual(self.diff_select.current_diff, "Easy")

    def test_medium_selection(self):
        result = self.diff_select.difficulty_level_sel("Medium")
        self.assertEqual(result, "Difficulty set to Medium")
        self.assertEqual(self.diff_select.current_diff, "Medium")

    def test_hard_selection(self):
        result = self.diff_select.difficulty_level_sel("Hard")
        self.assertEqual(result, "Difficulty set to Hard")
        self.assertEqual(self.diff_select.current_diff, "Hard")

    def test_invalid_selection(self):
        with self.assertRaises(ValueError) as context:
            self.diff_select.difficulty_level_sel("Insane")
        self.assertEqual(str(context.exception), "Invalid difficulty selection")


if __name__ == "__main__":
    unittest.main()
