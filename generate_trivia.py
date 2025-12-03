import re
import random
from openai import OpenAI
from parseOUDaily import ArticleScraper, URLS

# Text me if you need the key - Ryan
# Make sure OPENAI_API_KEY is set in your environment
client = OpenAI()


def ask_openai(prompt: str) -> str:
    """
    Call OpenAI and return the text output.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",  # or another model you have access to
        input=prompt,
    )
    return response.output_text


def make_trivia_from_article(title: str, content: str) -> str:
    """
    Turn an article into ONE trivia question.

    Output format (exactly 4 lines, in this order):
    Question
    Answer
    Hint
    Correct_Answer
    """
    prompt = f"""
You are helping build an OU-themed trivia app.

Based on the following news article, write ONE multiple-choice trivia question.

Requirements:
- Topic must be about the University of Oklahoma or OU sports/student life as reflected in the article.
- Use 4 answer choices (A, B, C, D).
- Provide a short hint that helps the player think about the answer.
- The correct answer must be exactly one letter: A, B, C, or D.

VERY IMPORTANT OUTPUT FORMAT:
Return your response as EXACTLY FOUR LINES in this order, with NO extra labels or extra text:

Line 1: Question
Line 2: Answer (all 4 choices formatted like 'A) ...; B) ...; C) ...; D) ...')
Line 3: Hint
Line 4: Correct_Answer (just the letter A, B, C, or D)

Do NOT add any other lines, labels, markdown, or explanations.

Article title: {title}

Article text:
\"\"\" 
{content[:6000]}
\"\"\"
"""
    return ask_openai(prompt)


if __name__ == "__main__":
    scraper = ArticleScraper()
    trivia_list = []  # each item: {question, options, hint, correct_index}
    last_correct_index = None

    for url in URLS:
        title_text, content_text = scraper.scrape(url)

        if content_text == "No content found":
            print("\n(No content found, skipping OpenAI call.)")
            continue

        try:
            trivia_block = make_trivia_from_article(title_text, content_text)
            # trivia_block should be:
            # Question\nAnswer\nHint\nCorrect_Answer

            # Split into lines and clean
            lines = [line.strip() for line in trivia_block.split("\n") if line.strip()]

            if len(lines) < 4:
                print("\nUnexpected format from OpenAI, skipping this article.")
                print(trivia_block)
                continue

            question, answer_line, hint, correct_answer_raw = lines[:4]

            # Turn the answer line into a list of options
            # Expected format: "A) ...; B) ...; C) ...; D) ..."
            raw_options = answer_line.split(";")

            options = []
            for opt in raw_options:
                opt = opt.strip()
                if not opt:
                    continue
                # Remove leading "A) ", "B) ", etc., if present
                opt = re.sub(r"^[A-D]\)\s*", "", opt)
                options.append(opt)

            if len(options) != 4:
                print("\nUnexpected number of options, skipping this question.")
                print("Answer line:", answer_line)
                print("Parsed options:", options)
                continue

            # Map correct answer letter -> original index (0–3)
            letter = correct_answer_raw.strip().upper()[0]  # take first character
            letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
            original_correct_index = letter_to_index.get(letter, -1)

            if original_correct_index == -1 or original_correct_index >= len(options):
                print("\nWarning: could not map correct answer properly, skipping this question.")
                print("Raw correct_answer:", correct_answer_raw)
                print("Options:", options)
                continue

            # --- Shuffle options so correct answer index varies ---
            indices = list(range(len(options)))
            random.shuffle(indices)

            # If we can, avoid same correct_index as previous question
            # by reshuffling once if it matches last_correct_index
            def get_correct_after_shuffle():
                shuffled_correct_idx = indices.index(original_correct_index)
                return shuffled_correct_idx

            shuffled_correct_index = get_correct_after_shuffle()

            if last_correct_index is not None and shuffled_correct_index == last_correct_index:
                # Try one more shuffle to change it
                random.shuffle(indices)
                shuffled_correct_index = get_correct_after_shuffle()

            # Build shuffled options
            shuffled_options = [options[i] for i in indices]

            # Now this is our final correct_index
            correct_index = shuffled_correct_index
            last_correct_index = correct_index

            trivia_item = {
                "question": question,
                "options": shuffled_options,   # list of 4 one-line strings
                "hint": hint,
                "correct_index": correct_index,  # 0-based index in options
            }

            trivia_list.append(trivia_item)

            # Optional: print what was added
            print("\nAdded trivia:")
            print("Q:", question)
            print("Options:", shuffled_options)
            print("Hint:", hint)
            print("Correct index:", correct_index)

        except Exception as e:
            print("Error calling OpenAI:", e)

    print(f"\nTotal trivia questions generated: {len(trivia_list)}")
