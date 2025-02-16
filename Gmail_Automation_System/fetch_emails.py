import os
import pickle
import sqlite3
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Authenticate with Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

# Store emails in database
def store_email(email_info):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO emails (id, sender, recipient, subject, received_at, snippet, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email_info["id"], email_info["from"], email_info["to"], email_info["subject"], email_info["date"], email_info["snippet"], email_info['is_read']))

    conn.commit()
    conn.close()

# Fetch and store emails
def fetch_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(userId="me", maxResults=15).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return

    for msg in messages:
        msg_id = msg["id"]
        email_data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
        headers = email_data["payload"]["headers"]

        email_info = {
            "id": msg_id,
            "from": None,
            "to": None,
            "subject": None,
            "date": None,
            "snippet": email_data.get("snippet", ""),
            "is_read": False,
        }

        label_ids = email_data.get("labelIds", [])
        if 'UNREAD' not in label_ids:
            email_info["is_read"] = True

        for header in headers:
            if header["name"] == "From":
                email_info["from"] = header["value"]
            elif header["name"] == "To":
                email_info["to"] = header["value"]
            elif header["name"] == "Subject":
                email_info["subject"] = header["value"]
            elif header["name"] == "Date":
                email_info["date"] = header["value"]

        store_email(email_info)  # Store email in database

        print(f"✅ Stored Email: {email_info['subject']} from {email_info['from']}")

if __name__ == "__main__":
    fetch_emails()
