# =========================================================
# MEMBER 3 - DETECTION  |  LANGUAGE: Python only
# Job: read the text/link, add points for every warning sign,
#      return score, level and a list of warnings.
# More points = more dangerous.
# =========================================================

import re
from urllib.parse import urlparse

# ---------- lists you can edit freely ----------
URGENT_WORDS = ["urgent", "immediately", "account blocked", "suspended",
                "within 24 hours", "act now"]
SECRET_WORDS = ["password", "login", "verify your account", "otp",
                "bank details", "account details"]
BAD_ENDINGS = [".xyz", ".top", ".click", ".tk", ".ml", ".gq", ".zip"]
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly"]
BRANDS = ["paypal", "google", "amazon", "apple", "microsoft", "facebook",
          "netflix", "paytm", "hdfc", "icici"]
LINK_WORDS = ["login", "verify", "secure", "update", "account", "password",
              "bank", "free", "gift", "prize", "bonus"]


# ---------- the ONE function main.py calls ----------
def analyze_input(user_input):
    text = user_input.strip().lower()
    if text == "":
        return {"error": "Please enter a message or URL."}

    score = 0
    warnings = []

    # ----- Part A: warning signs in the MESSAGE wording -----
    # (links are removed first, because links are checked separately in Part B)
    message = re.sub(r"(?:https?://|www\.)\S+", "", text)
    for word in URGENT_WORDS:
        if word in message:
            score += 15
            warnings.append("Urgent or threatening language detected (+15)")
            break

    for word in SECRET_WORDS:
        if word in message:
            score += 25
            warnings.append("Possible request for sensitive information (+25)")
            break

    # ----- Part B: find the links inside the text -----
    links = re.findall(r"(?:https?://|www\.)\S+", text)
    if not links and " " not in text and "." in text:
        links = [text]                       # the whole input is just a link

    for link in links:
        typed_http = link.startswith("http://")
        if not link.startswith("http"):
            link = "http://" + link          # urlparse needs this at the start

        try:
            host = urlparse(link).hostname or ""
        except ValueError:
            host = ""
        if "." not in host:
            continue

        # Rule 1: a number (192.168.1.5) instead of a website name
        if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", host):
            score += 30
            warnings.append("Uses a number (IP address) instead of a website name (+30)")

        # Rule 2: '@' can hide the real website
        if "@" in link:
            score += 25
            warnings.append("Has an '@' symbol which can hide the real website (+25)")

        # Rule 3: http instead of https
        if typed_http:
            score += 15
            warnings.append("Not secure: uses http instead of https (+15)")

        # Rule 4: very long link
        if len(link) > 75:
            score += 10
            warnings.append("Very long link (+10)")

        # Rule 5: many hyphens in the website name
        if host.count("-") >= 2:
            score += 10
            warnings.append("Many hyphens in the website name (+10)")

        # Rule 6: risky ending like .xyz or .top
        for ending in BAD_ENDINGS:
            if host.endswith(ending):
                score += 15
                warnings.append("Risky website ending " + ending + " (+15)")
                break

        # Rule 7: short link hides the real destination
        if host in SHORTENERS:
            score += 15
            warnings.append("Short link hides the real destination (+15)")

        # Rule 8: risky words inside the link
        found = [w for w in LINK_WORDS if w in link]
        if found:
            points = min(len(found) * 8, 24)
            score += points
            warnings.append("Risky words in link: " + ", ".join(found)
                            + " (+" + str(points) + ")")

        # Rule 9: a famous brand used on a website that is not that brand
        parts = host.split(".")
        main_name = parts[-2]                          # paypal.com -> paypal
        if main_name in ["co", "com", "org", "net", "gov", "ac"] and len(parts) >= 3:
            main_name = parts[-3]                      # bbc.co.uk  -> bbc
        for brand in BRANDS:
            if brand in re.split(r"[.-]", host) and main_name != brand:
                score += 25
                warnings.append("Pretends to be '" + brand + "' but is not (+25)")
                break

    # ----- Part C: decide the level -----
    if score > 100:
        score = 100
    if score >= 50:
        level = "Dangerous"
    elif score >= 20:
        level = "Suspicious"
    else:
        level = "Safe"

    if not warnings:
        warnings.append("No warning signs found.")

    # this dictionary becomes the JSON answer
    return {"risk_score": score, "risk_level": level, "warnings": warnings}