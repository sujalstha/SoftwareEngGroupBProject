import json
import ast

class JSONBuilder:
    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    # PARSER: Take OpenAI raw output and extract Q, answers, index, hint
    # ----------------------------------------------------------------------
    def parse_openai_output(self, text):
        """
        Expected OpenAI output format:

            <question>
            ['Ans1', 'Ans2', 'Ans3', 'Ans4']
            Hint: <hint text>
            <correct_index>

        Returns:
            question, answers, correct_index, hint
        """

        # Split + remove empty lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if len(lines) < 4:
            raise ValueError("OpenAI output malformed: not enough lines.")

        # 1. Question
        question = lines[0]

        # 2. Answers (Python list string → actual list)
        try:
            answers = ast.literal_eval(lines[1])
        except Exception:
            raise ValueError("Could not parse answer list from line 2.")

        # 3. Hint ("Hint: <text>")
        hint_line = lines[2]
        if hint_line.lower().startswith("hint:"):
            hint = hint_line[5:].strip()
        else:
            raise ValueError("Hint line missing or malformed.")

        # 4. Correct index (last line)
        try:
            correct_index = int(lines[-1])
        except:
            raise ValueError("Correct index must be an integer.")

        return question, answers, correct_index, hint

    # ----------------------------------------------------------------------
    # BUILDER: Takes parsed values → clean JSON dict
    # ----------------------------------------------------------------------
    def build(self, question, answers, correct_index, hint):
        """
        Builds the final JSON object.
        """

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

    # ----------------------------------------------------------------------
    # SAVER: Write dict → .json file
    # ----------------------------------------------------------------------
    def save(self, data, filename="question.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[JSONBuilder] Saved → {filename}")
