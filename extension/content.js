const api = typeof browser !== "undefined" ? browser : chrome;
const BUTTON_ID = "phishing-analyze-floating-button";
const RESULT_ID = "phishing-analyze-floating-result";

function extractEmailText() {
  const candidates = document.querySelectorAll("div.a3s.aiL, div.a3s");
  for (const node of candidates) {
    const text = node.innerText ? node.innerText.trim() : "";
    if (text) {
      return text;
    }
  }
  return "";
}

function formatResult(data) {
  const prediction = data.prediction === 1 ? "Phishing" : "Legit";
  const prob = typeof data.probability === "number"
    ? ` (p=${data.probability.toFixed(4)})`
    : "";
  return `${prediction}${prob}`;
}

function showFloatingResult(message, isError = false) {
  const resultEl = document.getElementById(RESULT_ID);
  if (!resultEl) {
    return;
  }
  resultEl.textContent = message;
  resultEl.style.display = "block";
  resultEl.style.background = isError ? "#fff1f1" : "#ffffff";
  resultEl.style.borderColor = isError ? "#f3b0b0" : "#d9e2ec";
}

async function analyzeCurrentEmailFromPage() {
  const buttonEl = document.getElementById(BUTTON_ID);
  if (!buttonEl) {
    return;
  }

  buttonEl.disabled = true;
  buttonEl.textContent = "Analiziram...";
  showFloatingResult("Čitam mejl...");

  try {
    const response = await api.runtime.sendMessage({ type: "ANALYZE_EMAIL" });
    if (response && response.error) {
      showFloatingResult(response.error, true);
      return;
    }

    if (!response || !response.result) {
      showFloatingResult("Nema rezultata.", true);
      return;
    }

    showFloatingResult(formatResult(response.result));
  } catch (error) {
    showFloatingResult("Greška pri analizi.", true);
  } finally {
    buttonEl.disabled = false;
    buttonEl.textContent = "Analiziraj";
  }
}

function injectFloatingAnalyzeButton() {
  if (document.getElementById(BUTTON_ID)) {
    return;
  }

  const wrapper = document.createElement("div");
  wrapper.style.position = "fixed";
  wrapper.style.right = "16px";
  wrapper.style.bottom = "16px";
  wrapper.style.zIndex = "999999";
  wrapper.style.display = "flex";
  wrapper.style.flexDirection = "column";
  wrapper.style.gap = "8px";
  wrapper.style.alignItems = "flex-end";

  const resultEl = document.createElement("div");
  resultEl.id = RESULT_ID;
  resultEl.style.display = "none";
  resultEl.style.maxWidth = "280px";
  resultEl.style.padding = "8px 10px";
  resultEl.style.background = "#ffffff";
  resultEl.style.border = "1px solid #d9e2ec";
  resultEl.style.borderRadius = "10px";
  resultEl.style.fontFamily = "Arial, sans-serif";
  resultEl.style.fontSize = "13px";
  resultEl.style.color = "#1f2933";
  resultEl.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.12)";

  const buttonEl = document.createElement("button");
  buttonEl.id = BUTTON_ID;
  buttonEl.textContent = "Analiziraj";
  buttonEl.style.border = "none";
  buttonEl.style.background = "#0f62fe";
  buttonEl.style.color = "#ffffff";
  buttonEl.style.padding = "10px 14px";
  buttonEl.style.borderRadius = "999px";
  buttonEl.style.cursor = "pointer";
  buttonEl.style.fontFamily = "Arial, sans-serif";
  buttonEl.style.fontSize = "14px";
  buttonEl.style.fontWeight = "600";
  buttonEl.style.boxShadow = "0 6px 16px rgba(0, 0, 0, 0.2)";

  buttonEl.addEventListener("click", analyzeCurrentEmailFromPage);

  wrapper.appendChild(resultEl);
  wrapper.appendChild(buttonEl);
  document.body.appendChild(wrapper);
}

injectFloatingAnalyzeButton();

api.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message && message.type === "GET_EMAIL_TEXT") {
    sendResponse({ text: extractEmailText() });
  }
  return true;
});
