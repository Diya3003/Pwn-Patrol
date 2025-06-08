# email_sender.py

from email.mime.text import MIMEText
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from risk_model import calculate

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def write_email(results):
    body = "Here is your report of compromised/insecure passwords:\n\n"
    results.sort(key=lambda x: x['pwned_count'], reverse=True)
    emojis = ["✅", "🟩", "🟨", "🟧", "🟥"]
    for r in results:
        emoji = emojis[calculate(r['pwned_count'])]
        body += emoji + f" Website: {r['website']}, (User/Email: {r['user']}): Found in {r['pwned_count']} breaches\n\n"
    return body


def send_email(to, results):
    body = write_email(results)
    subject = "Pwned Passwords Report"
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        sent = service.users().messages().send(
            userId='me', body={'raw': raw_message}).execute()
        print(f"✅ Email sent! Message ID: {sent['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")