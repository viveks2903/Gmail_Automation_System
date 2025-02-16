import pytest
from fetch_emails import authenticate_gmail, fetch_emails
from unittest.mock import patch, MagicMock

# Test case to mock the authenticate_gmail function
def test_authenticate_gmail():
    # Mock the credentials object
    mock_creds = MagicMock()
    mock_creds.valid = True
    mock_creds.expired = False
    mock_creds.refresh_token = None

    with patch("fetch_emails.pickle.load", return_value=mock_creds):
        service = authenticate_gmail()
        assert service is not None, "Failed to authenticate Gmail service"

# Test case to mock fetch_emails function
@patch('fetch_emails.authenticate_gmail')


def test_fetch_emails(mock_authenticate):
    # Mock the authenticate_gmail function to return a mock service
    mock_service = MagicMock()
    mock_authenticate.return_value = mock_service

    # Mock the response from the Gmail API
    mock_service.users().messages().list.return_value.execute.return_value = {
        'messages': [{'id': '123'}]
    }
    mock_service.users().messages().get.return_value.execute.return_value = {
        'payload': {'headers': [{'name': 'From', 'value': 'test@example.com'},
                               {'name': 'Subject', 'value': 'Test Email'},
                               {'name': 'Date', 'value': '2025-01-25'}]},
        'snippet': 'This is a test email snippet',
        'labelIds': ['UNREAD']
    }

    with patch('fetch_emails.store_email') as mock_store_email:
        fetch_emails()
        mock_store_email.assert_called_once()  # Check if store_email was called

        # Check if the mocked service is used correctly
        mock_service.users().messages().list.assert_called_once_with(userId="me", maxResults=15)
        mock_service.users().messages().get.assert_called_once_with(userId="me", id='123', format="full")

