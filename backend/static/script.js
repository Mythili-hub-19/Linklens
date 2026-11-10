const userInput = document.getElementById("userInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const resetBtn = document.getElementById("resetBtn");

const result = document.getElementById("result");
const riskLevel = document.getElementById("riskLevel");
const riskScore = document.getElementById("riskScore");

const warningsList = document.getElementById("warnings");
const preventionList = document.getElementById("preventionTips");

const meterFill = document.getElementById("meterFill");
const statusBadge = document.getElementById("statusBadge");


// Sample input buttons

document.querySelectorAll(".sample-btn").forEach(function(button) {
    button.addEventListener("click", function() {
        userInput.value = button.dataset.sample;
        userInput.focus();
    });
});


// Analyze button

analyzeBtn.addEventListener("click", function() {

    const text = userInput.value.trim();

    if (text === "") {
        alert("Please paste a URL or message first!");
        return;
    }

    analyzeBtn.textContent = "Analyzing...";
    analyzeBtn.disabled = true;

    result.classList.add("hidden");

    // ---------- JAVASCRIPT <-> BACKEND: THE fetch() CALL ----------
    fetch("/analyze?text=" + encodeURIComponent(text))
        .then(function(response) {
            return response.json().then(function(data) {
                if (!response.ok) {
                    // main.py sends errors as {"detail": "..."}
                    throw new Error(data.detail || "Analysis failed.");
                }
                return data;
            });
        })
        .then(function(data) {
            showResult(data);                      // data comes from detection.py
        })
        .catch(function(error) {
            if (error instanceof TypeError) {
                alert("Cannot reach the server. Is FastAPI running?");
            } else {
                alert(error.message);
            }
        })
        .finally(function() {
            analyzeBtn.textContent = "Analyze Threat →";
            analyzeBtn.disabled = false;
        });
});


// Display result

function showResult(analysis) {

    riskLevel.textContent = "Risk Level: " + analysis.risk_level;
    riskScore.textContent = "Risk Score: " + analysis.risk_score + "/100";

    meterFill.style.width = analysis.risk_score + "%";

    if (analysis.risk_level === "Dangerous") {

        riskLevel.style.color = "#ff6464";
        meterFill.style.background = "#ff6464";
        statusBadge.style.background = "#542b35";
        statusBadge.style.color = "#ff9999";

    } else if (analysis.risk_level === "Suspicious") {

        riskLevel.style.color = "#ffc45c";
        meterFill.style.background = "#ffc45c";
        statusBadge.style.background = "#55452a";
        statusBadge.style.color = "#ffda8a";

    } else {

        riskLevel.style.color = "#50d69a";
        meterFill.style.background = "#50d69a";
        statusBadge.style.background = "#1d5947";
        statusBadge.style.color = "#70edb8";
    }

    statusBadge.textContent = analysis.risk_level;


    // Display warnings

    warningsList.replaceChildren();

    analysis.warnings.forEach(function(warning) {
        const li = document.createElement("li");
        li.textContent = warning;
        warningsList.appendChild(li);
    });


    // Display prevention suggestions

    preventionList.replaceChildren();

    analysis.prevention_tips.forEach(function(tip) {
        const li = document.createElement("li");
        li.textContent = tip;
        preventionList.appendChild(li);
    });

    result.classList.remove("hidden");
}


// Reset button

resetBtn.addEventListener("click", function() {

    userInput.value = "";

    result.classList.add("hidden");

    meterFill.style.width = "0%";

    warningsList.replaceChildren();
    preventionList.replaceChildren();

    analyzeBtn.textContent = "Analyze Threat →";
    analyzeBtn.disabled = false;

    userInput.focus();
});