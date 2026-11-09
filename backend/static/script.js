
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

// Analyze button - REAL BACKEND CONNECTION
analyzeBtn.addEventListener("click", async function() {

    const text = userInput.value.trim();

    if (text === "") {
        alert("Please paste a URL or message first!");
        return;
    }

    analyzeBtn.textContent = "Analyzing...";
    analyzeBtn.disabled = true;

    result.classList.add("hidden");

    try {

        const response = await fetch(
            `/analyze?text=${encodeURIComponent(text)}`
        );

        const analysis = await response.json();

        if (!response.ok) {
            throw new Error(analysis.detail || "Analysis failed");
        }

        showResult(analysis);

    } catch (error) {

        alert("Unable to analyze: " + error.message);
        console.error("Analysis error:", error);

    } finally {

        analyzeBtn.textContent = "Analyze Threat →";
        analyzeBtn.disabled = false;

    }
});


// Display result
function showResult(analysis) {

    // Accept backend field names

//we replaced analysis.score with score and vice versa warnings , tips & 
//level to make js compatible with response format of python detection engine
//thus frontend matches backend response format
    const score = analysis.risk_score ?? analysis.score ?? analysis.threat_score;

    const level = analysis.risk_level ?? analysis.level;

    const warnings = analysis.warnings ?? analysis.reasons ?? [];

    const tips = analysis.prevention_tips ?? analysis.tips ?? [];

    riskLevel.textContent = "Risk Level: " + level;
    riskScore.textContent = "Risk Score: " + score + "/100";

    meterFill.style.width = score + "%";

    if (level === "Dangerous") {

        riskLevel.style.color = "#ff6464";
        meterFill.style.background = "#ff6464";
        statusBadge.style.background = "#542b35";
        statusBadge.style.color = "#ff9999";

    } else if (level === "Suspicious") {

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

    statusBadge.textContent = level;

    // Display warnings
    warningsList.replaceChildren();

    warnings.forEach(function(warning) {

        const li = document.createElement("li");
        li.textContent = warning;
        warningsList.appendChild(li);

    });

    // Display prevention suggestions
    preventionList.replaceChildren();

    tips.forEach(function(tip) {

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
