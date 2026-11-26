# 🔗 LinkLens — Smart Link & Message Protection

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg)
![Status](https://img.shields.io/badge/Status-Live-brightgreen.svg)

**Protect yourself from suspicious links and phishing messages with LinkLens!**

LinkLens is a web-based security awareness tool that analyzes URLs and messages to identify potential warning signs of phishing and online scams. It provides a risk score, risk level, and actionable safety recommendations.

## 🚀 Try LinkLens Live

### 👉 [OPEN LINKLENS — LIVE DEMO](https://linklens-36fb.onrender.com)

**No installation required!** Open the live website, enter a suspicious URL or message, and click **Analyze Threat** to see the results.

> Note: The application is hosted on Render's free tier. If the service has been inactive, its first request may take some time to load.

---

## ✨ Features

- 🔗 **URL Analysis:** Checks URLs for common suspicious characteristics.
- 💬 **Message Analysis:** Identifies potentially risky wording in messages.
- 📊 **Risk Score:** Assigns a score from 0 to 100.
- 🚦 **Risk Classification:** Categorizes results as Safe, Suspicious, or Dangerous.
- ⚠️ **Warning Details:** Explains the warning signs detected and their score contributions.
- 🛡️ **Prevention Tips:** Provides recommendations based on the analysis.
- 🔍 **Link Extraction:** Analyzes links included in submitted messages.
- 🖥️ **Interactive Interface:** Uses a dark-themed interface with a color-coded risk meter.
- ⚡ **REST API:** Provides an API endpoint for submitting text for analysis.

## 🎯 How to Use

1. Open the [LinkLens Live Website](https://linklens-36fb.onrender.com).
2. Enter a URL, a suspicious message, or a message containing a link.
3. Click **Analyze Threat**.
4. Review the risk score, risk level, and detected warning signs.
5. Follow the prevention tips to help protect yourself online.

**That's it!** You don't need to install Python or run terminal commands to try the live demo.

## 🧪 Example

Try analyzing this simulated suspicious URL:

`http://paypal.secure-login.xyz/verify`

LinkLens may flag warning signs such as:
- Use of HTTP instead of HTTPS.
- A potentially risky domain ending.
- Suspicious words such as `secure`, `login`, or `verify`.
- A brand name appearing in a domain that does not belong to that brand.

*This URL is an illustrative example, not a recommendation to visit the website.*

The actual risk score and warnings depend on the detection rules implemented in the application.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Backend | Python |
| Web Framework | FastAPI |
| Server | Uvicorn |
| Detection Engine | Python, Regular Expressions, URL Parsing |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

## ⚙️ How It Works

LinkLens uses a rule-based detection engine to examine URLs and messages for common warning signs.

### URL Checks
- IP addresses used instead of domain names.
- Suspicious URL structures, including the `@` symbol.
- HTTP links without HTTPS.
- Unusually long URLs.
- Multiple hyphens in domain names.
- Potentially risky domain endings.
- URL shortening services.
- Suspicious keywords in links.
- Brand names appearing in unrelated domains.

### Message Checks
- Urgent or threatening language.
- Requests for sensitive information.
- Suspicious account verification requests.
- Messages that pressure users to act quickly.

The application combines detected warning signs into a risk score capped at 100.

| Risk Score | Risk Level |
|---|---|
| 0–19 | Safe |
| 20–49 | Suspicious |
| 50–100 | Dangerous |

**Important:** These classifications are heuristic estimates, not guarantees of safety or maliciousness.

## 🌐 Live Application & API

**Live Website:**  
https://linklens-36fb.onrender.com

**API Documentation:**  
https://linklens-36fb.onrender.com/docs

The API documentation provides an interactive interface for exploring the available API endpoints.

### Analyze Endpoint

`GET /analyze`

| Parameter | Description |
|---|---|
| `text` | The URL, message, or text to analyze |

Example endpoint:

`https://linklens-36fb.onrender.com/analyze?text=example`

The endpoint returns a JSON response containing the risk score, risk level, warning messages, and prevention tips.

## 💻 Run Locally (Optional)

Judges can use the live demo without running any commands. Developers who want to explore the source code can run the project locally.

### Prerequisites
- Python 3.8 or newer
- pip

### Installation

```bash
git clone https://github.com/Yukta-devlane-18/Linklens.git
cd Linklens
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```text
Linklens/
├── LICENSE
├── README.md
├── requirements.txt
├── .gitignore
└── backend/
    ├── main.py
    ├── detection.py
    └── static/
        ├── index.html
        ├── style.css
        └── script.js
```

## 🔮 Future Improvements

- Integration with real-time threat intelligence databases.
- Persistent storage for previous analyses.
- Automated tests for detection rules.
- Improved detection accuracy and reduced false positives.
- Additional URL and message analysis capabilities.

## 👩‍💻 Contributors

- **Yukta** — [@Yukta-devlane-18](https://github.com/Yukta-devlane-18)

## ⚠️ Disclaimer

LinkLens is an educational hackathon prototype that uses rule-based detection.

It does not currently verify URLs against live threat intelligence databases. False positives and false negatives are possible, and a low risk score does not guarantee that a URL or message is safe.

Always verify suspicious links through official websites or trusted communication channels. Never share passwords, banking details, or OTPs with unverified sources.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Built for safer browsing and phishing awareness. 🔐**

### 🔗 [Try LinkLens Live](https://linklens-36fb.onrender.com)
