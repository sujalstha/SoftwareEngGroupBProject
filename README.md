# OU Trivia App # 
_By Group B: Sujal, Jole, Devin, Jayce, Mo, Ryan, Abraham_

---

## 📖 Overview

**OU Trivia** is a desktop game that tests knowledge of the University of Oklahoma’s history, sports, and campus culture.  
The app is built with **Python (Tkinter)** and uses:

- **Web scraping** of OU Daily articles  
- **OpenAI’s API** to generate fresh trivia questions, answers, and hints  
- A **JSON pipeline** to move questions from the backend into the UI

Every time you play, the game can generate a new set of OU-themed questions based on real news articles, so the content stays current and interesting.

---

## ✨ Current Features

### 🎨 OU-Themed UI
- Tkinter front end styled with **OU crimson & cream**.
- Clean layout with:
  - Top bar: Difficulty, timer, current streak  
  - Center: Question & hint  
  - Bottom: Four large answer buttons

### 🤖 AI-Generated Trivia
- Scrapes current OU Daily articles via `parseOUDaily.py`.
- Sends article titles and content to the **OpenAI API**.
- OpenAI responds in a strict format that includes:
  - Question text  
  - Four answer options  
  - Hint  
  - Correct answer index  
- `jsonBuilder.py` parses the AI output and builds a `trivia_questions.json` file for the front end.

### 🎯 Difficulty-Based Gameplay
- Difficulty selection: **Easy / Medium / Hard** (via `DiffSelect.py` + main UI).
- Difficulty controls **how we prompt the AI** and **how much time** the player gets:
  - Easy → 30 seconds per question  
  - Medium → 20 seconds  
  - Hard → 10 seconds  

### ⏱ Timed Questions & Streaks
- If the timer hits 0 → **Game over** (“Time’s up! Game end. Goodbye!”).
- Answer correctly → next question.
- Answer incorrectly → “Incorrect choice! Game over. Goodbye!” and the game exits gracefully.
- **Streak counter**:
  - Tracks consecutive correct answers
  - Popup celebration at 5, 10, and 15 in a row

### 🔁 Fresh Questions Each Run
- Every time you select a difficulty, the app:
  1. Scrapes articles
  2. Calls the OpenAI API to generate new questions
  3. Overwrites `trivia_questions.json` with a fresh set
- No old state is reused — each run can feel like a “new edition” of OU Trivia.

### ⚙️ Responsive Loading (Threading)
- Generating questions can take a bit (web + API), so the UI uses **background threads**:
  - The Tkinter window **stays responsive** while questions are being generated.
  - Status label shows `Generating <difficulty> questions... please wait.`
  - Once background work is done, the quiz screen appears automatically.

---

## 🛠 Tech Stack

- **Language:** Python 3.9+
- **UI Framework:** Tkinter
- **Backend Logic:**  
  - `parseOUDaily.py` – Scrapes OU Daily article titles & content  
  - `generate_trivia.py` – Calls OpenAI API and coordinates question generation  
  - `jsonBuilder.py` – Parses AI responses into a clean JSON structure for the GUI
- **Data Format:** `trivia_questions.json`  
- **Planned / optional:** SQLite for leaderboards and user persistence

> The original design mentioned SQLite and player accounts.  
> The current version of the game’s main entry **does not use SQLite or usernames**;  
> database integration is now a planned future enhancement (see Roadmap).

---

## 📂 Project Structure

```plaintext
OU_Trivia_App/
│── main.py              # Tkinter app entry point (difficulty UI + quiz loop)
│── generate_trivia.py   # AI-powered question generation pipeline
│── jsonBuilder.py       # Parses AI output into question dicts & JSON
│── parseOUDaily.py      # Scrapes OU Daily articles (ArticleScraper + URLS)
│── DiffSelect.py        # Simple difficulty selection helper
│── urls.py              # (Optional) Separate URL list module
│── trivia_questions.json# Last generated question set (overwritten each run)
│── README.md            # Project documentation
```
---

## 🚀 Getting Started

1. Prerequisites

- `Python 3.9+`

Packages:

- `openai`

- `requests`

- `beautifulsoup4`

## A Valid OpenAI API key !!!

Install dependencies (after cloning the repo):
```pip install openai requests beautifulsoup4```

Set your API key (example for macOS/Linux):
```OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"```

Or for Windows PowerShell:
```$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"```

### Running from the Command Line - Probably the Quickest:
```plaintext
git clone <repo-link>
cd OU_Trivia_App

# (Optional) create and activate a venv
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install openai requests beautifulsoup4

# Set your API key (see above), then run:
python main.py

```
🗂 Backlog & Roadmap (Updated)
Task	Status
Basic Tkinter trivia UI	✅ Done
Difficulty selection (Easy/Med/Hard)	✅ Done
AI-powered question generation	✅ Done
Timer per question	✅ Done
Streak tracking + popups	✅ Done
Background threading for loading	✅ Done
OU Daily article scraping	✅ Done
Clean JSON question pipeline	✅ Done
Auto-parse latest OU Daily links	🔁 Planned
Reduce load times (URL limiting, caching, pre-generation)	🔁 Planned
Customizable game settings (timer, # questions, categories)	🔁 Planned
Reintroduce SQLite for scores/users	🔁 Planned
High score board/leaderboard	🔁 Planned
Mascot animations (Boomer/Sooner)	🔁 Planned
Sound effects for correct/incorrect	🔁 Planned
Multiple game modes (Endless, Sudden Death, Practice)	🔁 Planned
Theming/dark mode	🔁 Planned
