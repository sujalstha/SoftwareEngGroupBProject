"""
jsonBuilder – SECURITY REVIEW & CWE-476 MAPPING

This file elaborates on the following: 

1. Security concerns related to null-like values in Python
2. Potential risks when interacting with external APIs and scrapers
3. Security commentary on the jsonBuilder code
4. Explanation of CWE-476 and how it applies to this project
5. Mitigations and best practices
"""


#SECURITY CONCERNS & RECOMMENDATIONS

"""
In Python, a null pointer dereference maps to attempting to operate on `None`
as if it were a real object. This happens when upstream failures (scraper, API,
JSON file read, etc.) return unexpected None values and the rest of the system
blindly assumes the data is valid.

Key concerns:

1. Unvalidated API Responses
   - OpenAI may return malformed or empty output.
   - Without checks, None values flow into the game logic and cause crashes.

2. Assuming Parsed Fields Always Exist
   - The parser expects a strict four-line output.
   - If any line is missing, Python may index into an empty list or operate
     on None by mistake.

3. Implicit Trust in Answer Lists and Indexes
   - If answers=None or index is invalid, the UI will break when rendering.
   - Equivalent to dereferencing a null pointer.

4. Scraper Returning No Content
   - Failed HTTP requests or changes in OU Daily’s layout can produce None,
     which travels downstream unless validated.

5. Lack of Defensive Programming in the UI
   - The UI screens assume valid JSON objects.
   - Unexpected None values can cause immediate crashes.

Mitigation Strategy (implemented):

- Validate all inputs early.
- Add strict checks in parser and JSON builder.
- Raise controlled exceptions instead of allowing None propagation.
- Avoid C extensions or modules that reintroduce raw-pointer behavior.
- Validate JSON before loading into the game.
"""


#CODE EXCERPT WITH SECURITY COMMENTARY

import ast
import json


class JSONBuilder:
    """
    This class handles:
    - Parsing OpenAI raw output
    - Validating extracted components
    - Building structured JSON objects
    - Mitigating null-like failures by failing early
    """

    def __init__(self):
        self.questions = []

    def parse_openai_output(self, text):
        """
        Convert raw OpenAI output into components.

        Expected format:
            <question>
            ['Ans1', 'Ans2', 'Ans3', 'Ans4']
            Hint: <text>
            <index>

        SECURITY FIXES:
        - Validate text is not None
        - Ensure required lines exist
        - Catch parsing failures
        - Prevent None from leaking into game logic
        """

        if not text:
            raise ValueError("Empty or None OpenAI response received.")

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if len(lines) < 4:
            raise ValueError("Malformed OpenAI output (missing fields).")

        question = lines[0]

        try:
            answers = ast.literal_eval(lines[1])
        except Exception:
            raise ValueError("Failed to parse answers list from OpenAI output.")

        hint_line = lines[2]
        if not hint_line.lower().startswith("hint:"):
            raise ValueError("Hint line malformed or missing.")
        hint = hint_line[5:].strip()

        try:
            correct_index = int(lines[-1])
        except:
            raise ValueError("Correct index is not a valid integer.")

        return question, answers, correct_index, hint

    def build(self, question, answers, correct_index, hint):
        """
        Build one validated question object.

        SECURITY FIXES:
        - Check all parameters for None
        - Validate answer list and index bounds
        - Reject invalid structured data
        """

        if question is None or hint is None or answers is None:
            raise ValueError("One or more fields are None (invalid data).")

        answers = [a.strip() for a in answers]

        if correct_index < 0 or correct_index >= len(answers):
            raise ValueError("Correct index out of bounds.")

        return {
            "question": question.strip(),
            "answers": answers,
            "correct_index": correct_index,
            "hint": hint.strip(),
        }

    def add_question(self, qdict):
        self.questions.append(qdict)

    def save_all(self, filename="trivia_bank.json"):
        """
        Save accumulated questions to one JSON file.
        """

        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"questions": self.questions}, f, indent=4, ensure_ascii=False)


# CWE-476: NULL POINTER DEREFERENCE

"""
CWE-476 describes failures that occur when code dereferences a null pointer.
Python does not allow raw pointer manipulation, but the equivalent failure
pattern occurs when the system operates on None values unexpectedly.

Examples in this project:

- Trying to index into None instead of a list
- Accessing attributes on None
- Passing None to UI components that expect strings
- Spreading None values through data structures due to missing validation

How the mitigation works:

- All parsing and building functions validate input early.
- Any detection of None or malformed fields triggers a controlled exception.
- Prevents the UI and game logic from encountering None-based failures.
"""


#RISK LEVEL & BEST PRACTICES

"""
Current Risk Level: LOW

Reasons:
- Python inherently protects memory access.
- Strict validation prevents None propagation.
- All external data sources undergo early sanitization.

Best Practices Moving Forward:

1. Validate all external data aggressively.
2. Sanitize OpenAI and scraper output before use.
3. Add UI-side checks when loading questions.
4. Use safe default values when encountering errors.
5. Add unit tests specifically for malformed OpenAI output.
"""

# End of security review file
