import json
import sqlite3  
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

# Load Gmail API credentials
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

CLIENT_SECRET_FILE = "credentials.json"
# Connect to database
DB_FILE = "emails.db"  
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Load Gmail API service
def get_gmail_service():
    creds = None
    
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Return the Gmail API service object
    return build("gmail", "v1", credentials=creds)

# Load rules from JSON file
def load_rules():
    try:
        with open("rules.json", "r") as file:
            data = json.load(file)
        return data.get("rules", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ No rules found or invalid JSON format.")
        return []

# Fetch unread emails from database
def fetch_emails():
    cursor.execute("SELECT id, sender, subject, snippet, received_at FROM emails WHERE is_read = 0")
    return cursor.fetchall()

# Apply rules to emails
def apply_rules(service, emails, rules):
    for email in emails:
        msg_id, sender, subject, snippet, received_at = email

        for rule in rules:
            conditions_met = []
            for condition in rule["conditions"]:
                field, operator, value = condition["field"], condition["operator"], condition["value"]
                
                # Get actual email field value
                email_value = {"from": sender, "subject": subject, "snippet": snippet, "received_at": received_at}.get(field, "")
                
                # Check condition
                if operator == "contains" and value in email_value:
                    conditions_met.append(True)
                elif operator == "does_not_contain" and value not in email_value:
                    conditions_met.append(True)
                elif operator == "equals" and email_value == value:
                    conditions_met.append(True)
                elif operator == "does_not_equal" and email_value != value:
                    conditions_met.append(True)
                else:
                    conditions_met.append(False)

            # Check rule predicate
            rule_match = all(conditions_met) if rule["predicate"] == "All" else any(conditions_met)

            # Apply actions if rule matches
            if rule_match:
                print(f"✅ Rule matched for email '{subject}' from {sender}")
                apply_actions(service, msg_id, rule["actions"])

# Apply actions (mark read/unread, move email)
def apply_actions(service, msg_id, actions):
    labels_to_add = []
    labels_to_remove = []
    msg = service.users().messages().get(userId="me", id=msg_id).execute()
    current_labels = msg['labelIds']

    for action in actions:
        if action == "mark_as_read" and "UNREAD" in current_labels:
            labels_to_remove.append("UNREAD")
        elif action == "mark_as_unread" and "UNREAD" not in current_labels:
            labels_to_add.append("UNREAD")
        elif action.startswith("move_to_folder"):
            folder_name = action.split(":")[1]
            label_id = get_label_id(service, folder_name)
            if label_id:
                labels_to_add.append(label_id)

    modify_email_labels(service, msg_id, labels_to_add, labels_to_remove)

# Get Gmail label ID
def get_label_id(service, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label["name"].lower() == label_name.lower():
            return label["id"]
    
    # Create label if not found
    new_label = service.users().labels().create(userId="me", body={"name": label_name}).execute()
    return new_label["id"]

# Modify Gmail labels
def modify_email_labels(service, msg_id, add_labels, remove_labels):
    # Skip modification if no labels are to be added or removed
    if not add_labels and not remove_labels:
        print(f"Skipping modification for email {msg_id}: No labels to add or remove")
        return

    modifications = {"addLabelIds": add_labels, "removeLabelIds": remove_labels}
    service.users().messages().modify(userId="me", id=msg_id, body=modifications).execute()
    print(f"📩 Email {msg_id} updated with labels: {add_labels}, removed: {remove_labels}")

# Main function to process emails
def process_emails():
    service = get_gmail_service()
    rules = load_rules()
    emails = fetch_emails()

    if not emails:
        print("📭 No unread emails to process.")
        return

    apply_rules(service, emails, rules)

if __name__ == "__main__":
    process_emails()
