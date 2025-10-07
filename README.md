# Instagram → WellnessLiving Automation (Streamlit)

This project demonstrates an end-to-end automation that ingests Instagram leads, creates clients in WellnessLiving, books classes, logs activity to Google Sheets and sends SMS follow-ups. The app is built as a Streamlit app (`app.py`) so it can be deployed on Streamlit Cloud.

> **Important:** This repository contains *example* code and placeholders. Do not commit production credentials. Use environment variables or the secrets manager of your hosting platform.

## Folder structure
(See root of repo — same as provided in the project structure in this README.)

## Quickstart (local)
1. Create a virtual environment with Python 3.11.0 and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Place your Google service account JSON at service_account.json or set the GOOGLE_SERVICE_ACCOUNT_FILE env var.

4. Set required environment variables or create a config.py with placeholders filled:

META_ACCESS_TOKEN, WELLNESS_CLIENT_ID, WELLNESS_CLIENT_SECRET

TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER

OPENAI_API_KEY

GOOGLE_SERVICE_ACCOUNT_FILE

5. Ensure the Kaggle dataset path is available (local copy or update KAGGLE_INSTAGRAM_JSON).

