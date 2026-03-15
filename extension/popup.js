const api = typeof browser !== "undefined" ? browser : chrome;

const analyzeCurrentButton = document.getElementById("analyzeCurrent");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

function formatResult(data) {
  const prediction = data.prediction === 1 ? "Phishing" : "Legit";
  const prob = typeof data.probability === "number"
    ? ` (p=${data.probability.toFixed(4)})`
    : "";
  return `${prediction}${prob}`;
}

analyzeCurrentButton.addEventListener("click", async () => {
  statusEl.textContent = "Reading Gmail and analyzing...";
  resultEl.textContent = "";

  try {
    const response = await api.runtime.sendMessage({ type: "ANALYZE_EMAIL" });
    if (response && response.error) {
      statusEl.textContent = "";
      resultEl.textContent = response.error;
      return;
    }

    if (!response || !response.result) {
      statusEl.textContent = "";
      resultEl.textContent = "No result.";
      return;
    }

    statusEl.textContent = "";
    resultEl.textContent = formatResult(response.result);
  } catch (error) {
    statusEl.textContent = "";
    resultEl.textContent = "Failed to analyze current email. Open a Gmail email and try again.";
  }
});
