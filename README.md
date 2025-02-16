

# **Gmail Email Processing Script**

## **Overview**
This Python script is designed to streamline email processing by leveraging the Gmail API. It allows users to fetch emails, apply custom rules to process them, and perform various actions (like marking emails as read/unread, moving them to specific folders, etc.) in an automated and efficient manner.

The solution demonstrates robust integration with the Gmail API and provides rule-based email management functionality. All emails are stored locally in an SQLite database for easy retrieval and management.

---

## **Features**
- 📩 **Fetch Emails**: Retrieve emails from the Gmail inbox using Gmail API.
- 🗃️ **Database Storage**: Store email details (e.g., sender, subject, snippet) in a SQLite database.
- ⚙️ **Rule-Based Processing**: Define rules to filter, categorize, or perform actions on emails.
- ✅ **Actions**:
  - Mark emails as read/unread.
  - Move emails to specific folders/labels.
- 🔒 **Secure Authentication**: Uses Gmail OAuth 2.0 for secure access to your Gmail account.

---

## **Tech Stack**
- **Language**: Python 3.x
- **Database**: SQLite
- **Google API Libraries**:
  - `google-api-python-client`
  - `google-auth`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`

---

## **Prerequisites**
1. **Python 3.x** installed on your machine.
2. **Gmail API enabled** for your Google Cloud project.
3. **OAuth 2.0 credentials**:
   - Download the `credentials.json` file from the Google Developer Console.

---

## **Installation & Setup**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repository/gmail-email-processor.git
cd gmail-email-processor
```

### **2. Install Required Dependencies**
Use `pip` to install the necessary Python libraries:
```bash
pip install --upgrade google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
```

### **3. Configure Gmail API**
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Enable the Gmail API for your project.
- Create **OAuth 2.0 credentials** and download the `credentials.json` file.
- Place the `credentials.json` file in the root directory of the project.

### **4. Run the Scripts**
1. **Create the database**:
   ```bash
   python database.py
   ```
   This script initializes the SQLite database to store emails.

2. **Fetch emails**:
   ```bash
   python fetch_emails.py
   ```
   This script fetches emails from your Gmail inbox and stores metadata (e.g., sender, subject, snippet) in the database.

3. **Set rules**:
   ```bash
   python set_rules.py
   ```
   Define custom rules for processing emails (e.g., mark emails as read, move to folders).

4. **Process emails**:
   ```bash
   python process_emails.py
   ```
   Apply the defined rules to process emails and perform actions on them.

---

## **How It Works**
1. **Authentication**:
   - The script uses Gmail API’s OAuth 2.0 flow to authenticate the user and grant access to the Gmail inbox.
   - A `token.pickle` file is created to store the user’s credentials for future runs.

2. **Email Fetching**:
   - The `fetch_emails.py` script retrieves unread emails from the Gmail inbox using the Gmail API and stores metadata (e.g., sender, subject, snippet) in an SQLite database.

3. **Rule Definition**:
   - The `set_rules.py` script allows users to define rules in JSON format. Each rule consists of:
     - **Conditions**: Filters based on fields like `from`, `subject`, or `received_at`.
     - **Predicates**: Specify whether **all** conditions must match (`All`) or **any** condition can match (`Any`).
     - **Actions**: Actions to perform if the rule matches, such as marking emails as read or moving them to folders.

4. **Email Processing**:
   - The `process_emails.py` script applies the defined rules to the emails in the database, modifies their status using the Gmail API, and updates the database accordingly.

---

## **Example Rule**
Here’s an example of a rule defined in JSON:
```json
{
    "predicate": "All",
    "conditions": [
        {"field": "from", "operator": "contains", "value": "notifications@example.com"},
        {"field": "subject", "operator": "contains", "value": "Alert"}
    ],
    "actions": [
        "mark_as_read",
        "move_to_folder:Important"
    ]
}
```
- **Conditions**:
  - Emails must be from `notifications@example.com`.
  - The subject must contain the word `Alert`.
- **Actions**:
  - Mark the email as read.
  - Move the email to the folder labeled "Important."

---

## **Testing**
Unit tests are included to ensure the functionality of core components. Example test cases:
- **Database Operations**:
  - Verify that emails are correctly inserted into the database and fetched as expected.
- **Rule Evaluation**:
  - Ensure rules are evaluated correctly based on conditions and predicates.
- **API Mocking**:
  - Mock Gmail API calls to test email fetching and rule processing without requiring real API interactions.

To run the tests, use:
```bash
pytest tests/
```

---

## **Future Enhancements**
1. **Date-Based Rules**:
   - Add support for conditions based on email dates (e.g., `received_at > 2025-01-01`).
2. **Attachment Handling**:
   - Extend functionality to handle emails with attachments (e.g., download or filter based on file type).
3. **Enhanced User Interface**:
   - Provide a GUI or web-based interface for managing rules and viewing email statuses.
4. **Multi-Account Support**:
   - Enable processing for multiple Gmail accounts within the same application.
5. **Integration with Other Services**:
   - Integrate with third-party tools like Slack, Trello, or Google Sheets for extended email actions.
