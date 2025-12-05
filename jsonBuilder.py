import json
import ast

class JSONBuilder:
    def __init__(self):
        # Stores all questions for batch mode
        self.questions = []

    # PARSER: Convert OpenAI raw text → fields
    def parse_openai_output(self, text):
        """
        Expected OpenAI output format (exactly 4 lines):

            <question>
            ["Ans1", "Ans2", "Ans3", "Ans4"]
            Hint: <hint text>
            <correct_index>

        Where <correct_index> is 0, 1, 2, or 3.
        """

        # Clean lines, remove empty ones
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if len(lines) < 4:
            raise ValueError("OpenAI output malformed: not enough lines.")

        # 1. Question
        question = lines[0]

        # 2. Answers as a Python list literal
        answers_line = lines[1]
        try:
            answers = ast.literal_eval(answers_line)
        except Exception:
            raise ValueError("Could not parse answer list from line 2.")

        if not isinstance(answers, list) or len(answers) != 4:
            raise ValueError("Answers line must be a list of 4 strings.")

        # 3. Hint
        hint_line = lines[2]
        if hint_line.lower().startswith("hint:"):
            hint = hint_line[5:].strip()
        else:
            raise ValueError("Hint line missing or malformed (must start with 'Hint:').")

        # 4. Correct index
        try:
            correct_index = int(lines[3])
        except Exception:
            raise ValueError("Correct index must be an integer.")

        if correct_index < 0 or correct_index >= len(answers):
            raise ValueError("Correct index out of range 0–3.")

        return question, answers, correct_index, hint

    # ADD: Build dict and add to list
    def add_question(self, question, answers, correct_index, hint, source_title=None):
        question = question.strip()
        answers = [a.strip() for a in answers]
        hint = hint.strip()

        if correct_index < 0 or correct_index >= len(answers):
            raise ValueError("correct_index out of range.")

        q_dict = {
            "question": question,
            "answers": answers,
            "correct_index": correct_index,
            "hint": hint,
        }

        if source_title:
            q_dict["source_title"] = source_title.strip()

        self.questions.append(q_dict)

    # SAVE ALL: Write *all questions* to one JSON file
    def save_all(self, filename="trivia_questions.json"):
        """
        Overwrites trivia_questions.json each time it's called.
        So every time you pick a difficulty and generate, you get a fresh set.
        """
        bundle = {"questions": self.questions}

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=4, ensure_ascii=False)

        print(f"[JSONBuilder] Saved {len(self.questions)} questions → {filename}")
