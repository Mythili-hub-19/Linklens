# =========================================================
# MEMBER 2 - BACKEND  |  LANGUAGE: Python + FastAPI
# Job: receive the text from the webpage, give it to
#      Member 3's detection, send the answer back as JSON.
# Also links the frontend (static folder) to the backend.
# =========================================================

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from detection import analyze_input         # Member 3's code is used here

app = FastAPI()


# ---------- MEMBER 2: THE API ENDPOINT ----------
# The webpage asks for  /analyze?text=something
# FastAPI puts "something" into the variable  text
@app.get("/analyze")
def analyze(text: str = ""):
    result = analyze_input(text)            # detection runs here
    # LATER (database): save `result` here, before returning it
    return result                           # FastAPI turns this into JSON


# ---------- MEMBER 2: BACKEND <-> FRONTEND LINK ----------
# Shows the static folder at http://127.0.0.1:8000
# Keep these lines AFTER the /analyze part above.
STATIC_FOLDER = Path(__file__).resolve().parent / "static"
app.mount("/", StaticFiles(directory=STATIC_FOLDER, html=True))

