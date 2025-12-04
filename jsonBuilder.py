import json
import ast

class JSONBuilder:
    def __init__(self):
        # Stores all questions for batch mode
        self.questions = []

    # PARSER: Convert OpenAI raw text → fields
    def parse_openai_output(self, text):
        """
        Expected OpenAI output format:

            <question>
            ['Ans1', 'Ans2', 'Ans3', 'Ans4']
            Hint: <hint text>
            <correct_index>
        """

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if len(lines) < 4:
            raise ValueError("OpenAI output malformed: not enough lines.")

        # 1. Question
        question = lines[0]

        # 2. Answers
        try:
            answers = ast.literal_eval(lines[1])
        except Exception:
            raise ValueError("Could not parse answer list from line 2.")

        # 3. Hint
        hint_line = lines[2]
        if hint_line.lower().startswith("hint:"):
            hint = hint_line[5:].strip()
        else:
            raise ValueError("Hint line missing or malformed.")

        # 4. Correct index
        try:
            correct_index = int(lines[-1])
        except:
            raise ValueError("Correct index must be an integer.")

        return question, answers, correct_index, hint

    # BUILDER: Construct JSON object for ONE question
    def build(self, question, answers, correct_index, hint):
        question = question.strip()
        answers = [a.strip() for a in answers]
        hint = hint.strip()

        if correct_index < 0 or correct_index >= len(answers):
            raise ValueError("correct_index out of range.")

        return {
            "question": question,
            "answers": answers,
            "correct_index": correct_index,
            "hint": hint
        }

    # ADD: Add question to batch list
    def add_question(self, question_dict):
        self.questions.append(question_dict)

    # SAVE ALL: Write *all questions* to one JSON file
    def save_all(self, filename="trivia_questions.json"):
        bundle = {"questions": self.questions}

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bundle, f, indent=4, ensure_ascii=False)

        print(f"[JSONBuilder] Saved {len(self.questions)} questions → {filename}")
