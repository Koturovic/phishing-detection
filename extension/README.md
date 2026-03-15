Firefox extension for phishing detection.

Prerequisite:
- Start local API first: `python3 -m uvicorn src.api_server:app --reload --port 8000`

Load the extension:
- Open `about:debugging#/runtime/this-firefox`
- Click "Load Temporary Add-on"
- Select `extension/manifest.json`

How to use:
- Click the extension icon.
- Paste email text into the popup text box.
- Click "Analyze Text".
- You get result: `Legit` or `Phishing` (and probability if available).
