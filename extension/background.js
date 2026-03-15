const api = typeof browser !== "undefined" ? browser : chrome;
const API_URL = "http://localhost:8000/predict";

async function analyzeActiveTab() {
  const tabs = await api.tabs.query({ active: true, currentWindow: true });
  const tab = tabs[0];
  if (!tab || !tab.id) {
    return { error: "No active tab." };
  }
  const response = await api.tabs.sendMessage(tab.id, { type: "GET_EMAIL_TEXT" });
  if (!response || !response.text) {
    return { error: "No email text found." };
  }
  const apiResponse = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: response.text })
  });
  const data = await apiResponse.json();
  if (!apiResponse.ok) {
    return { error: data.detail || "API error." };
  }
  return { result: data };
}

api.runtime.onMessage.addListener((message) => {
  if (message && message.type === "ANALYZE_EMAIL") {
    return analyzeActiveTab();
  }
  return false;
});
