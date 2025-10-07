import requests
from typing import Optional, Dict, List
from config import WELLNESS_API_BASE, WELLNESS_CLIENT_ID, WELLNESS_CLIENT_SECRET

# NOTE: WellnessLiving API specifics may differ. Replace endpoint paths & auth flow per their docs.
class WellnessClient:
    def __init__(self):
        self.base = WELLNESS_API_BASE
        self.token = None

    def authenticate(self) -> str:
        """
        Implement WellnessLiving authentication (example uses client credential flow).
        Replace with the actual method from WellnessLiving docs.
        """
        # Example placeholder:
        resp = requests.post(
            f"{self.base}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": WELLNESS_CLIENT_ID,
                "client_secret": WELLNESS_CLIENT_SECRET
            },
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        self.token = data.get("access_token")
        return self.token

    def headers(self):
        if not self.token:
            self.authenticate()
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def create_client(self, lead: Dict) -> Dict:
        """
        Create a client/lead in WellnessLiving. Adapt fields to API contract.
        """
        payload = {
            "firstName": lead.get("name") or "Lead",
            "email": lead.get("email"),
            "phone": lead.get("phone"),
            "notes": f"Imported from Instagram: {lead.get('interest')}"
        }
        resp = requests.post(f"{self.base}/clients", json=payload, headers=self.headers(), timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_schedule(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Fetch classes between start_date and end_date
        """
        params = {"start": start_date, "end": end_date}
        resp = requests.get(f"{self.base}/classes", headers=self.headers(), params=params, timeout=10)
        resp.raise_for_status()
        return resp.json().get("classes", [])

    def book_class(self, client_id: str, class_id: str) -> Dict:
        payload = {"clientId": client_id, "classId": class_id}
        resp = requests.post(f"{self.base}/bookings", headers=self.headers(), json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
