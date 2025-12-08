from fastapi import FastAPI, Request, HTTPException
from generate_trivia import generate_questions_for_difficulty

app = FastAPI()

# I chose CWE-287, Improper Authentication.
# Right now my features – generate_trivia and the timer – don’t involve login
# or user identity, so this weakness doesn’t really show up yet.
#
# However, in the future we plan to add a login system so only authorized users
# can generate new trivia or access certain modes, and we’ll need to avoid
# CWE-287 by doing proper server-side authentication and not letting users
# bypass those checks.

# Fake in-memory session store (for demo purposes)
logged_in_sessions = set()

@app.post("/login")
def login(username: str, password: str):
    # Very simplified: normally you'd verify a hashed password in a database
    if username == "testuser" and password == "secret123":
        session_id = "some-random-secure-token"
        logged_in_sessions.add(session_id)
        return {"session_id": session_id}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# ❌ Vulnerable version (what CWE-287 warns about) would be:
# @app.post("/generate_trivia")
# def generate_trivia_open():
#     # Anyone can call this without being logged in
#     return generate_questions_for_difficulty("Easy")


# ✅ Fixed version: require authentication before generating trivia
@app.post("/generate_trivia")
def generate_trivia_protected(request: Request):
    # Client must send a valid session ID in the header
    session_id = request.headers.get("X-Session-Id")

    # Proper authentication: check session on the server side
    if session_id not in logged_in_sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Only authenticated users reach this point
    questions = generate_questions_for_difficulty("Easy")
    return {"count": len(questions), "questions": questions}
