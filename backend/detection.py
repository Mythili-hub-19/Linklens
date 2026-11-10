
# =========================================================
# MEMBER 3 - DETECTION | Python
# Job: Analyze messages and URLs for suspicious indicators.
# =========================================================

import re
from urllib.parse import urlparse

# ---------- Detection lists ----------

URGENT_WORDS = [
    "urgent", "immediately", "account blocked",
    "suspended", "within 24 hours", "act now"
]

SECRET_WORDS = [
    "password", "login", "verify your account",
    "otp", "bank details", "account details"
]

BAD_ENDINGS = [
    ".xyz", ".top", ".click", ".tk",
    ".ml", ".gq", ".zip"
]

SHORTENERS = [
    "bit.ly", "tinyurl.com", "t.co",
    "goo.gl", "is.gd", "cutt.ly"
]

BRANDS = [
    "paypal", "google", "amazon", "apple",
    "microsoft", "facebook", "netflix",
    "paytm", "hdfc", "icici"
]

LINK_WORDS = [
    "login", "verify", "secure", "update",
    "account", "password", "bank",
    "free", "gift", "prize", "bonus"
]


# ---------- Main detection function ----------

def analyze_input(user_input):

    text = user_input.strip().lower()

    if not text:
        return {
            "error": "Please enter a message or URL."
        }

    score = 0
    warnings = []

    def add_warning(points, message):
        nonlocal score

        score += points

        if message not in warnings:
            warnings.append(message)

    # ---------- PART A: MESSAGE ANALYSIS ----------

    message = re.sub(
        r"(?:https?://|www\.)\S+",
        "",
        text
    )

    for word in URGENT_WORDS:
        if word in message:
            add_warning(
                15,
                "Urgent or threatening language detected (+15)"
            )
            break

    for word in SECRET_WORDS:
        if word in message:
            add_warning(
                25,
                "Possible request for sensitive information (+25)"
            )
            break

    # ---------- PART B: URL EXTRACTION ----------

    links = re.findall(
        r"(?:https?://|www\.)[^\s<>\"']+|"
        r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}(?:/[^\s<>\"']*)?",
        text
    )

    # Remove common punctuation from extracted links
    links = [
        link.rstrip(".,!?;:)]}")
        for link in links
    ]

    # Remove duplicate links
    links = list(dict.fromkeys(links))

    for original_link in links:

        typed_http = original_link.startswith("http://")

        link = original_link

        if link.startswith("www."):
            link = "http://" + link

        elif not link.startswith(("http://", "https://")):
            link = "http://" + link

        try:
            parsed = urlparse(link)
            host = parsed.hostname or ""

        except ValueError:
            continue

        if "." not in host:
            continue

        host = host.lower()

        # Rule 1: IP address instead of domain
        if re.fullmatch(
            r"\d{1,3}(?:\.\d{1,3}){3}",
            host
        ):
            add_warning(
                30,
                "Uses an IP address instead of a website name (+30)"
            )

        # Rule 2: @ symbol
        if "@" in link:
            add_warning(
                25,
                "Contains an '@' symbol which may hide the destination (+25)"
            )

        # Rule 3: HTTP instead of HTTPS
        if typed_http:
            add_warning(
                15,
                "Uses HTTP instead of HTTPS (+15)"
            )

        # Rule 4: Long URL
        if len(original_link) > 75:
            add_warning(
                10,
                "Very long URL (+10)"
            )

        # Rule 5: Multiple hyphens
        if host.count("-") >= 2:
            add_warning(
                10,
                "Multiple hyphens in website name (+10)"
            )

        # Rule 6: Risky domain endings
        for ending in BAD_ENDINGS:

            if host.endswith(ending):
                add_warning(
                    15,
                    "Risky website ending " + ending + " (+15)"
                )
                break

        # Rule 7: URL shorteners
        if host in SHORTENERS:
            add_warning(
                15,
                "Short link hides its final destination (+15)"
            )

        # Rule 8: Suspicious URL words
        found = [
            word for word in LINK_WORDS
            if word in original_link
        ]

        if found:
            points = min(len(found) * 8, 24)

            add_warning(
                points,
                "Suspicious URL words: "
                + ", ".join(found)
                + " (+" + str(points) + ")"
            )

        # Rule 9: Brand impersonation indicators
        parts = host.split(".")

        main_name = parts[-2] if len(parts) >= 2 else ""

        if (
            main_name in ["co", "com", "org", "net", "gov", "ac"]
            and len(parts) >= 3
        ):
            main_name = parts[-3]

        for brand in BRANDS:

            if (
                brand in re.split(r"[.-]", host)
                and main_name != brand
            ):
                add_warning(
                    25,
                    "Possible impersonation of " + brand + " (+25)"
                )
                break

    # ---------- PART C: RISK SCORE ----------

    score = min(score, 100)

    if score >= 50:
        level = "Dangerous"

    elif score >= 20:
        level = "Suspicious"

    else:
        level = "Safe"

    if not warnings:
        warnings.append(
            "No suspicious patterns detected by the current rules."
        )

    # ---------- PART D: PREVENTION TIPS ----------

    if level == "Dangerous":

        tips = [
            "Avoid opening this suspicious link.",
            "Never enter passwords or OTPs on unverified pages.",
            "Verify the sender through an official channel."
        ]

    elif level == "Suspicious":

        tips = [
            "Check the website domain carefully.",
            "Avoid sharing personal or banking information.",
            "Verify the message before taking action."
        ]

    else:

        tips = [
            "No suspicious indicators were detected by current rules.",
            "Check the website address before entering information.",
            "Never share passwords or OTPs through messages."
        ]

    # ---------- PART E: JSON RESPONSE ----------

    return {
        "risk_score": score,
        "risk_level": level,
        "warnings": warnings,
        "prevention_tips": tips
    }
