# OU Trivia App 🎓
_By Group B: Sujal, Jole, Devin, Jayce, Mo, Ryan, Abraham_

---

## 📖 Overview

**OU Trivia** is a desktop application that tests knowledge of the University of Oklahoma’s history, sports, culture, and current events.  
The game uses:

- **Web scraping** of OU Daily articles  
- **OpenAI API** to generate fresh trivia questions  
- **JSON pipelines** for question formatting  
- **Tkinter** for the graphical user interface  

Each playthrough generates a brand‑new set of questions based on real OU news articles.

---

## ✨ Features

- 🎨 OU-themed crimson & cream UI  
- 🤖 AI-generated questions, hints, and answer options  
- 🎯 Difficulty levels (Easy / Medium / Hard)  
- ⏱ Timed questions (30s / 20s / 10s based on difficulty)  
- 🔁 New question set every time you run the app  
- ⚡ Background threading so the UI never freezes  
- 🔥 Streak tracking with reward popups (5, 10, 15 in a row)  
- ❌ Game over on wrong answer or timeout  
- 🏆 “You Win!” screen when questions run out  

---

## 🛠 Tech Stack

- Python 3.9+  
- Tkinter  
- Requests + BeautifulSoup4  
- OpenAI API  
- JSON data storage (no SQLite in current version)  

---

## 📂 Project Structure

```
OU_Trivia_App/
│── main.py             
│── generate_trivia.py   
│── jsonBuilder.py       
│── parseOUDaily.py      
│── DiffSelect.py        
│── urls.py              
│── trivia_questions.json
│── README.md            
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- Install required packages:

```
pip install openai requests beautifulsoup4
```

- Set your OpenAI API key:

**macOS/Linux:**
```
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

**Windows PowerShell:**
```
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

---

### 2. Run From Command Line

```
git clone <repo-link>
cd OU_Trivia_App

python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install openai requests beautifulsoup4

python main.py
```

You will see a window:

1. Pick a difficulty (Easy / Medium / Hard)  
2. Wait while questions are generated  
3. Play the quiz with timers & streak tracking  

---

## 🧑‍💻 Running in PyCharm

1. Open the `OU_Trivia_App` folder in PyCharm  
2. Set **Project → Python Interpreter** to Python 3.9+  
3. Install packages:  
   - `openai`  
   - `requests`  
   - `beautifulsoup4`  
4. Add environment variable:  

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

5. Run `main.py`

---

## 🧑‍💻 Running in VS Code

1. Open the folder in VS Code  
2. Select interpreter (Python 3.9+)  
3. Install dependencies:

```
pip install openai requests beautifulsoup4
```

4. Set the API key:

**macOS/Linux**
```
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

**Windows PowerShell**
```
$env:OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

5. Run using the **Run ▶️** button or **F5**

---

## 🗂 Roadmap

- Auto-parse newest OU Daily article links  
- Faster load times (parallel scraping, caching, pre-generation)  
- More customizable game settings  
- Dark mode & accessibility features  
- Sound effects & simple animations  
- Multiple game modes (Endless, Sudden Death, Practice)  
- SQLite leaderboard & player profiles  

---

**Boomer Sooner!** 🐴🔴⚪️
