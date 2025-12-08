import re  # (Currently unused; you can remove this if not needed)
from openai import OpenAI

from parseOUDaily import ArticleScraper, URLS  # Your scraper + list of OU Daily URLs
from jsonBuilder import JSONBuilder            # Helper to parse/save trivia into JSON

# Uses OPENAI_API_KEY from your environment
client = OpenAI()


def ask_openai(prompt: str) -> str:
    """
    Send a prompt to OpenAI and return the text output.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",  # Model to use
        input=prompt,          # Prompt text
    )
    # response.output_text is a convenience for "just give me the text"
    return response.output_text


def make_trivia_from_article(title: str, content: str, difficulty: str) -> str:
    """
    Turn a single OU Daily article into ONE trivia question string
    using the given difficulty setting.

    The model is instructed to output exactly 4 lines:
        1) Question text
        2) Python list of 4 choices: ["A", "B", "C", "D"]
        3) Hint: <text>
        4) Correct answer index (0–3)
    """
    # Build a detailed prompt that explains format + difficulty rules
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
    # Send the prompt to OpenAI and return the raw 4-line string
    return ask_openai(prompt)


def generate_questions_for_difficulty(difficulty: str, json_path: str = "trivia_questions.json"):
    """
    Generate trivia questions for a given difficulty level.

    Steps:
    - Loop over each URL in URLS.
    - Scrape article title + content.
    - Ask OpenAI for ONE question per article.
    - Parse the model output into a question dict.
    - Save all questions into a JSON file (overwrite each time).
    - Return the list of question dicts.

    Each dict looks like:
        {
            "question": str,
            "answers": [str, str, str, str],
            "correct_index": int,
            "hint": str,
            "source_title": str
        }
    """
    scraper = ArticleScraper()  # Handles downloading/parsing OU Daily articles
    builder = JSONBuilder()     # Collects questions and writes JSON

    for url in URLS:
        print(f"\n--- Scraping ---\n{url}")
        try:
            # Get article title and body text from the URL
            title_text, content_text = scraper.scrape(url)
        except Exception as e:
            # If scraping fails, log and move on to the next URL
            print(f"[ERROR] Failed to scrape URL: {url}\n{e}")
            continue

        # Skip articles with no usable content
        if not content_text or content_text == "No content found":
            print("(No content found, skipping this article.)")
            continue

        try:
            # Ask OpenAI to turn this article into a trivia question
            raw = make_trivia_from_article(title_text, content_text, difficulty)

            # Parse the 4-line output string into structured pieces
            question, answers, correct_index, hint = builder.parse_openai_output(raw)

            # Add the question to our in-memory list
            builder.add_question(
                question=question,
                answers=answers,
                correct_index=correct_index,
                hint=hint,
                source_title=title_text,
            )

            # Optional debug print to see what was generated
            print("Q:", question)
            print("Answers:", answers)
            print("Correct index:", correct_index)
            print("Hint:", hint)

        except Exception as e:
            # If something goes wrong parsing or building, log it and continue
            print("[ERROR] Could not build question for this article:", e)
            continue

    # Write all collected questions into the JSON file (overwrites existing file)
    builder.save_all(json_path)

    # Also return the list of questions for whoever called this function (e.g., GUI)
    return builder.questions


if __name__ == "__main__":
    # If you run this file directly:
    #   python generate_trivia.py
    # it will generate Easy questions and save them to trivia_questions.json
    generated = generate_questions_for_difficulty("Easy")
    print(f"Generated {len(generated)} questions for Easy mode.")
