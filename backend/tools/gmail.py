import os
import re
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', 'token.json')

# ── OTP / sensitive-content filter ───────────────────────────────────────────
# Runs BEFORE any content reaches the LLM — security design decision
SENSITIVE_PATTERNS = [
    r'\b\d{4,8}\b',                          # 4-8 digit codes
    r'otp|one.time|verification code',        # OTP keywords
    r'password reset|reset your password',    # Password reset
    r'confirm your|confirmation code',        # Confirmation codes
    r'security code|auth code|login code',    # Auth codes
    r'do not share|never share',              # Warning phrases in OTP emails
]

SENSITIVE_SENDERS = [
  #  'noreply', 'no-reply', 'donotreply',
    'password' ,
    'accounts@', 'security@', 'verify@',
    'verification@', 'otp@'
]

def is_sensitive(sender: str, subject: str, body: str) -> bool:
    """Returns True if this email should be excluded from LLM context."""
    sender_lower = sender.lower()
    combined = (subject + ' ' + body).lower()

    # Check sender patterns
    for s in SENSITIVE_SENDERS:
        if s in sender_lower:
            return True

    # Check content patterns
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, combined, re.IGNORECASE):
            return True

    return False

# ── Gmail OAuth ───────────────────────────────────────────────────────────────
def authenticate_gmail():
    """
    Handles OAuth flow using client_id and client_secret from .env
    Stores token in backend/token.json after first login
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid token, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import Flow
            client_config = {
                "installed": {
                    "client_id": os.getenv("GMAIL_CLIENT_ID"),
                    "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
                }
            }
            flow = Flow.from_client_config(
                client_config,
                scopes=SCOPES,
                redirect_uri="urn:ietf:wg:oauth:2.0:oob"
            )
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                prompt='consent'
            )
            print("\n" + "="*60)
            print("GMAIL AUTH REQUIRED")
            print("Open this URL in your browser:")
            print(auth_url)
            print("="*60)
            code = input("Paste the authorization code here: ")
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save token for next time
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# ── Main email fetching function ──────────────────────────────────────────────
def get_important_emails(max_results: int = 15) -> list:
    """
    Fetches recent emails, filters out sensitive/OTP content,
    returns a safe list of email summaries for the LLM to read.
    """
    try:
        service = authenticate_gmail()
        import datetime
        today = datetime.date.today().strftime('%Y/%m/%d')
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q=f'after:{today}'
        ).execute()

        messages = results.get('messages', [])
        if not messages:
            return [{"info": "No unread emails found."}]

        emails = []
        filtered_count = 0

        for msg in messages:
            msg_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()

            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

            # Extract plain text body (first 300 chars only)
            body = ''
            payload = msg_data['payload']
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        import base64
                        body = base64.urlsafe_b64decode(
                            part['body']['data'] + '=='
                        ).decode('utf-8', errors='ignore')[:300]
                        break
            elif payload.get('body', {}).get('data'):
                import base64
                body = base64.urlsafe_b64decode(
                    payload['body']['data'] + '=='
                ).decode('utf-8', errors='ignore')[:300]

            # ── SECURITY FILTER — runs before LLM sees anything ──
            if is_sensitive(sender, subject, body):
                filtered_count += 1
                continue

            emails.append({
                "from": sender,
                "subject": subject,
                "date": date,
                "preview": body[:200] if body else "No preview available"
            })

        result = emails if emails else [{"info": "No important emails found (some were filtered for security)."}]

        # Add a note about filtered emails so Claude can mention it
        if filtered_count > 0:
            result.append({"info": f"{filtered_count} sensitive/OTP email(s) were automatically excluded for security."})

        return result

    except Exception as e:
        return [{"error": f"Gmail error: {str(e)}"}]