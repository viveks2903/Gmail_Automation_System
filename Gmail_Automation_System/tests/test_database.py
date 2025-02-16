import unittest
import sqlite3
from database import create_table, insert_email, get_unread_emails  

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Initialize in-memory database for testing
        self.conn = sqlite3.connect(':memory:')  # Using in-memory database
        self.cursor = self.conn.cursor()
        create_table(self.cursor)  # Directly calling the create_table function from database.py
    
    def test_insert_email(self):
        # Email data tuple to insert
        email = ('msg1', 'test@example.com', 'Update', 'This is an update.', '2025-01-01 10:00:00', 'This is a snippet.', 0)
        
        # Insert email into database
        insert_email(self.cursor, email)
        self.conn.commit()
        
        # Fetch and verify inserted email
        self.cursor.execute("SELECT * FROM emails WHERE id = 'msg1'")
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 'msg1')  # Check if the ID matches
    
    def test_get_unread_emails(self):
        # Insert sample emails
        email1 = ('msg1', 'test1@example.com', 'Subject 1', 'Body 1', '2025-01-01 10:00:00', 'Snippet 1', 0)
        email2 = ('msg2', 'test2@example.com', 'Subject 2', 'Body 2', '2025-01-02 10:00:00', 'Snippet 2', 0)
        insert_email(self.cursor, email1)
        insert_email(self.cursor, email2)
        self.conn.commit()

        # Get unread emails
        unread_emails = get_unread_emails(self.cursor)
        self.assertGreater(len(unread_emails), 0)  # Check if there are unread emails

if __name__ == '__main__':
    unittest.main()

