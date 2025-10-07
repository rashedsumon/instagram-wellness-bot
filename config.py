import os

# Prefer environment variables (set these in Streamlit Cloud secrets or your host env)
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "YOUR_META_ACCESS_TOKEN")
WELLNESS_CLIENT_ID = os.getenv("WELLNESS_CLIENT_ID", "YOUR_WELLNESS_CLIENT_ID")
WELLNESS_CLIENT_SECRET = os.getenv("WELLNESS_CLIENT_SECRET", "YOUR_WELLNESS_CLIENT_SECRET")
WELLNESS_API_BASE = os.getenv("WELLNESS_API_BASE", "https://api.wellnessliving.com")  # example

GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Instagram Leads")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "+1234567890")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# Kaggle dataset path (provided)
KAGGLE_INSTAGRAM_JSON = os.getenv("KAGGLE_INSTAGRAM_JSON", "/kaggle/input/instagram-ads/instagram_posts.json")

# Scheduler
SCHEDULED_WEEKLY_JOB_HOUR = int(os.getenv("SCHEDULED_WEEKLY_JOB_HOUR", "2"))  # 2 AM UTC on Sunday
