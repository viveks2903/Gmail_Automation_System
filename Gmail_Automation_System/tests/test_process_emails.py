import unittest
from unittest.mock import patch
from process_emails import process_emails

class TestProcessEmails(unittest.TestCase):
    
    @patch('process_emails.get_gmail_service')
    @patch('process_emails.fetch_emails')
    @patch('process_emails.apply_rules')
    def test_process_emails_success(self, mock_apply_rules, mock_fetch_emails, mock_service):
        mock_service.return_value = mock_service
        mock_fetch_emails.return_value = [{'id': 'msg1', 'from': 'test@example.com', 'subject': 'Update'}]
        
        process_emails()
        mock_apply_rules.assert_called_once()

if __name__ == '__main__':
    unittest.main()
