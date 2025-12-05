import re
from openai import OpenAI

from parseOUDaily import ArticleScraper, URLS
from jsonBuilder import JSONBuilder

# Make sure OPENAI_API_KEY is set in your environment
# Text Ryan for OPENAI_API_KEY
client = OpenAI()


def ask_openai(prompt: str) -> str:
    """
    Call OpenAI and return the text output as a plain string.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",  # or whichever model you have access to
        input=prompt,
    )
    # New OpenAI Python SDK gives convenience:
    return response.output_text


def make_trivia_from_article(title: str, content: str, difficulty: str) -> str:
    """
    Turn an article into ONE trivia question based on difficulty.

    OUTPUT FORMAT (EXACTLY 4 LINES):

    Line 1: Question text
    Line 2: A valid Python list of 4 answer choices, like:
            ["choice A text", "choice B text", "choice C text", "choice D text"]
    Line 3: Hint: <short hint text>
    Line 4: Correct answer index as an integer 0, 1, 2, or 3
    """

    prompt = f"""
You are helping build an OU-themed trivia app.

Difficulty mode: {difficulty}

Based on the following OU Daily news article, write ONE multiple-choice trivia question.

The question style should match the difficulty:
- Easy: very straightforward, obvious to most OU students.
- Medium: requires paying attention to key details in the article.
- Hard: more specific or tricky detail that still can be answered from the article.

The question must be about the University of Oklahoma (OU), OU sports, OU student life,
or something clearly tied to OU from this article.

VERY IMPORTANT: FOLLOW THIS EXACT OUTPUT FORMAT (4 LINES ONLY):

Line 1: Question text (no label)
Line 2: A valid Python list of 4 answer choices, like:
        ["choice A text", "choice B text", "choice C text", "choice D text"]
Line 3: Hint: <short hint text>
Line 4: Correct answer index as an integer 0, 1, 2, or 3
        (0 means the first answer in the list is correct, etc.)

Do NOT add any extra text, explanation, markdown, or labels.
Do NOT repeat the article verbatim, just use it to design the question.

Article title: {title}

Article text (you can skim and extract key facts; don't copy this whole thing into the question):
\"\"\" 
{content[:6000]}
\"\"\"
"""
    return ask_openai(prompt)


def generate_questions_for_difficulty(difficulty: str, json_path: str = "trivia_questions.json"):
    """
    Main function the GUI calls.

    - Scrapes each URL from parseOUDaily.URLS.
    - Asks OpenAI for ONE question per article using the chosen difficulty.
    - Parses & stores them into trivia_questions.json (overwritten each time).
    - Returns the list of question dicts.

    Each question dict looks like:
        {
            "question": str,
            "answers": [str, str, str, str],
            "correct_index": int,
            "hint": str,
            "source_title": str (optional)
        }
    """
    scraper = ArticleScraper()
    builder = JSONBuilder()

    for url in URLS:
        print(f"\n--- Scraping ---\n{url}")
        try:
            title_text, content_text = scraper.scrape(url)
        except Exception as e:
            print(f"[ERROR] Failed to scrape URL: {url}\n{e}")
            continue

        if not content_text or content_text == "No content found":
            print("(No content found, skipping this article.)")
            continue

        try:
            raw = make_trivia_from_article(title_text, content_text, difficulty)
            question, answers, correct_index, hint = builder.parse_openai_output(raw)

            builder.add_question(
                question=question,
                answers=answers,
                correct_index=correct_index,
                hint=hint,
                source_title=title_text,
            )

            # Optional debug output
            print("Q:", question)
            print("Answers:", answers)
            print("Correct index:", correct_index)
            print("Hint:", hint)

        except Exception as e:
            print("[ERROR] Could not build question for this article:", e)
            continue

    # Overwrite JSON file each time you generate
    builder.save_all(json_path)

    return builder.questions


if __name__ == "__main__":
    # Manual test: generate Easy questions and write JSON
    generated = generate_questions_for_difficulty("Easy")
    print(f"Generated {len(generated)} questions for Easy mode.")
