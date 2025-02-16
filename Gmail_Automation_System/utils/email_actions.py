from googleapiclient.discovery import build

def mark_email_read(service, msg_id):
    """Marks an email as read."""
    service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()

def mark_email_unread(service, msg_id):
    """Marks an email as unread."""
    service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': ['UNREAD']}).execute()

def move_email_to_folder(service, msg_id, label_id):
    """Moves email to the specified folder."""
    service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': [label_id]}).execute()

def get_label_id(service, label_name):
    """Returns label ID for the given label name."""
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    return None
