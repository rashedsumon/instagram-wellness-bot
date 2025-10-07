import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from config import GOOGLE_SERVICE_ACCOUNT_FILE, GOOGLE_SHEET_NAME

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

class SheetsClient:
    def __init__(self, service_account_file: str = None, sheet_name: str = None):
        self.service_account_file = service_account_file or GOOGLE_SERVICE_ACCOUNT_FILE
        self.sheet_name = sheet_name or GOOGLE_SHEET_NAME
        creds = Credentials.from_service_account_file(self.service_account_file, scopes=SCOPES)
        self.client = gspread.authorize(creds)
        self.sheet = self._open_or_create_sheet(self.sheet_name)

    def _open_or_create_sheet(self, name):
        try:
            sh = self.client.open(name)
        except gspread.SpreadsheetNotFound:
            sh = self.client.create(name)
            # Optionally share the sheet with the service account or other emails
        worksheet = sh.sheet1
        # Ensure header exists
        header = ["Name", "Email", "Phone", "Interest", "Class", "ClassDate", "FollowUpSent", "Status", "Source", "Timestamp"]
        if worksheet.row_count < 1:
            worksheet.insert_row(header, 1)
        return worksheet

    def append_lead(self, lead: dict):
        row = [
            lead.get("name"),
            lead.get("email"),
            lead.get("phone"),
            lead.get("interest"),
            lead.get("class") or "",
            lead.get("class_date") or "",
            lead.get("followup_sent") or "No",
            lead.get("status") or "New",
            lead.get("source") or "Instagram",
            lead.get("timestamp") or ""
        ]
        self.sheet.append_row(row)

    def get_all(self) -> pd.DataFrame:
        values = self.sheet.get_all_records()
        return pd.DataFrame(values)
