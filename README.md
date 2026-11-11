# LinkLens

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg) ![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)

**Smart link and message protection.** *Built as a hackathon project.* LinkLens is a small web app that checks a suspicious URL or message and tells you how risky it looks *before* you click. Paste something in, and it returns a risk score out of 100, a risk level, and a list of the warning signs it found.

> **Note:** LinkLens is a demo built on simple rule-based checks. It does not look up live threat databases, so a low score does not guarantee that a link or message is safe.

## Features

- Analyzes a **URL**, a **message**, or a message that **contains links**
- Gives a **risk score (0–100)** and a level: **Safe**, **Suspicious**, or **Dangerous**
- Explains the result with a list of **warnings**, each showing the points it added
- **Prevention tips** tailored to the risk level, so users know what to do next
- One-click **sample inputs** (safe URL, suspicious URL, phishing message) to try it out
- Clean, dark-themed single-page interface with a colour-coded risk meter
- FastAPI backend that serves both the API and the frontend, so there is only one server to run

## Tech stack

| Layer     | Technology                                  |
| --------- | ------------------------------------------- |
| Backend   | Python, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn |
| Detection | Python (`re`, `urllib.parse`), no extra dependencies |
| Frontend  | HTML, CSS, vanilla JavaScript               |

## Project structure

```
Linklens/
├── LICENSE
├── README.md
├── requirements.txt
├── .gitignore
└── backend/
    ├── main.py          # FastAPI app: /analyze endpoint + serves the frontend
    ├── detection.py     # Rule-based detection engine (scoring logic)
    └── static/
        ├── index.html   # Page layout
        ├── style.css    # Styling
        └── script.js    # Calls the API and renders the result
```

## Getting started

### Prerequisites

- Python 3.8 or newer
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mythili-hub-19/Linklens.git
cd Linklens

# 2. (Recommended) create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the app

Start the server from inside the `backend` folder (`main.py` imports `detection.py` directly, so it must be run from there):

```bash
cd backend
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

## Usage

1. Paste a suspicious URL or message into the text box, or click one of the sample buttons.
2. Click **Analyze Threat →**.
3. Review the risk level, score, and the warnings that explain it.
4. Click **Reset** to start over.

## API

### `GET /analyze`

| Parameter | Type   | Description                      |
| --------- | ------ | -------------------------------- |
| `text`    | string | The URL or message to analyze    |

**Example request**

```
GET /analyze?text=http://paypal.secure-login.xyz/verify
```

**Example response**

```json
{
  "risk_score": 79,
  "risk_level": "Dangerous",
  "warnings": [
    "Not secure: uses http instead of https (+15)",
    "Risky website ending .xyz (+15)",
    "Risky words in link: login, verify, secure (+24)",
    "Pretends to be 'paypal' but is not (+25)"
  ],
  "prevention_tips": [
    "Avoid opening this suspicious link.",
    "Never enter passwords or OTPs on unverified pages.",
    "Verify the sender through an official channel."
  ]
}
```

If `text` is empty, the API responds with HTTP `400` and `{"detail": "Input cannot be empty."}`.

Because FastAPI is used, interactive API docs are also available at **http://127.0.0.1:8000/docs** while the server is running.

## How detection works

`detection.py` adds points for each warning sign it finds. More points mean more danger. The total is capped at 100.

### Message wording

| Check                                   | Points |
| --------------------------------------- | ------ |
| Urgent or threatening language          | +15    |
| Request for sensitive information       | +25    |

### Link checks (applied to every link found)

| Check                                              | Points   |
| -------------------------------------------------- | -------- |
| IP address instead of a website name               | +30      |
| `@` symbol that can hide the real website          | +25     |
| `http://` instead of `https://`                    | +15      |
| Very long link (over 75 characters)                | +10      |
| Many hyphens in the website name (2 or more)       | +10      |
| Risky ending such as `.xyz`, `.top`, `.tk`         | +15      |
| URL shortener (`bit.ly`, `tinyurl.com`, …)         | +15      |
| Risky words in the link (`login`, `verify`, …)     | +8 each, max +24 |
| Well-known brand name on a site that isn't that brand | +25   |

### Risk levels

| Score    | Level      |
| -------- | ---------- |
| 0–19     | Safe       |
| 20–49    | Suspicious |
| 50–100   | Dangerous  |

All keyword and domain lists (`URGENT_WORDS`, `SECRET_WORDS`, `BAD_ENDINGS`, `SHORTENERS`, `BRANDS`, `LINK_WORDS`) sit at the top of `detection.py`, so you can edit them freely to tune the detection.

## Roadmap

- Database support to store past analyses
- Optional lookups against real threat-intelligence sources
- Tests for the detection rules

## Contributing

Contributions are welcome. Fork the repo, create a branch for your change, and open a pull request with a short description of what you changed and why.

## Disclaimer

LinkLens is a hackathon prototype provided for demonstration and educational purposes. It uses simple heuristics, can produce false positives and false negatives, and must not be relied on as a security product. Always verify suspicious links and messages through official channels.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it, provided the copyright and license notice are kept. The software is provided "as is", without warranty of any kind.
