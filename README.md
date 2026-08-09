# AI Assistant

A simple conversational AI web app built with Streamlit and the OpenAI Python SDK. It retains a short conversation history, shows actionable setup errors, and lets you clear the chat at any time.

## Requirements

- Python 3.10 or newer
- An OpenAI API key

## Run locally

From the `cnn` folder, run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `OPENAI_API_KEY` to your key. Optionally set `OPENAI_MODEL` to a model your account can access.

Then start the app:

```powershell
streamlit run app.py
```

Streamlit prints a local URL (normally `http://localhost:8501`) to open in your browser.

## Project structure

```text
app.py                  Streamlit user interface
services/ai_service.py  OpenAI request and error handling
.env.example            Environment variable template
```

Never commit your real `.env` file or API key.
