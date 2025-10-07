import streamlit as st
from datetime import datetime
from helpers.instagram_ingest import simulate_new_leads, load_instagram_dataset
from helpers.wellness_client import WellnessClient
from helpers.sheets_client import SheetsClient
from helpers.sms_client import SMSClient
from helpers.ai_bot import generate_message
from helpers.scheduler_jobs import start_scheduler, update_weekly_schedule
import pandas as pd
import traceback

st.set_page_config(page_title="Instagram → WellnessLiving Automation", layout="wide")

# start background scheduler
try:
    scheduler = start_scheduler()
except Exception:
    # in some hosting envs background schedulers may behave differently
    st.sidebar.warning("Scheduler failed to start in this environment; weekly updates might not run automatically.")
    st.sidebar.text(traceback.format_exc())

st.title("Instagram → WellnessLiving Automation Dashboard")

# Top row: Actions
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Simulate ingest leads from Kaggle dataset"):
        try:
            leads = simulate_new_leads(limit=10)
            st.success(f"Loaded {len(leads)} simulated leads")
            st.session_state["leads"] = leads
        except Exception as e:
            st.error(str(e))

with col2:
    if st.button("Run weekly schedule update now"):
        try:
            update_weekly_schedule()
            st.success("Weekly schedule update executed")
        except Exception as e:
            st.error(f"Failed to update schedule: {e}")

with col3:
    if st.button("List Google Sheet rows"):
        try:
            sc = SheetsClient()
            df = sc.get_all()
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to list sheet data: {e}")

# Leads panel
st.header("Leads (simulated / incoming)")
leads = st.session_state.get("leads")
if not leads:
    st.info("No simulated leads loaded yet. Click the left button to load from Kaggle dataset.")
else:
    df = pd.DataFrame(leads)
    st.dataframe(df)

    # process first lead example
    st.subheader("Process a lead")
    idx = st.number_input("Lead index", min_value=0, max_value=max(0, len(leads)-1), value=0)
    if st.button("Create client in WellnessLiving from selected lead"):
        lead = leads[int(idx)]
        try:
            wc = WellnessClient()
            created = wc.create_client(lead)
            st.success(f"Created client in WellnessLiving: {created}")
            # log to google sheets
            sc = SheetsClient()
            lead_log = lead.copy()
            lead_log["status"] = "Created in WellnessLiving"
            lead_log["timestamp"] = datetime.utcnow().isoformat()
            sc.append_lead(lead_log)
            st.info("Logged lead to Google Sheets.")
        except Exception as e:
            st.error(f"Error creating client: {e}")

    st.subheader("Start interactive chat with AI bot (example)")
    selected_text = st.text_area("User message (simulate)", value="Hi! I want to sign up for a free yoga class on Wednesday evening.")
    if st.button("Send AI message / Suggest times"):
        try:
            # call AI to craft a reply
            prompt = f"User: {selected_text}\nAssistant: Suggest available class times and ask preference in friendly tone."
            reply = generate_message(prompt)
            st.markdown("**AI reply:**")
            st.write(reply)
        except Exception as e:
            st.error(f"AI generation failed: {e}")

st.markdown("---")
st.markdown("**System logs / tips**")
st.write("Replace placeholders in `config.py` with your real API keys. Ensure `service_account.json` is present for Google Sheets or set `GOOGLE_SERVICE_ACCOUNT_FILE` env var.")

st.caption("This demo uses a Kaggle JSON file to simulate Instagram Leads. In production, replace simulation with webhook endpoints that receive Meta Ads Leadgen events and call the create flow.")
