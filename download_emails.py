import base64
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    creds = None
    # Token stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials available, let user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    # Replace 'Label_123456' with your Gmail label ID or use 'INBOX' etc.
    label_id = "Label_123456"  # example label ID

    # Get list of message IDs for the label
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=[label_id], maxResults=100)
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        print("No messages found.")
        return

    # Create directory to save emails
    os.makedirs("emails", exist_ok=True)

    for msg in messages:
        msg_id = msg["id"]
        message = (
            service.users()
            .messages()
            .get(userId="me", id=msg_id, format="raw")
            .execute()
        )
        raw_msg = message["raw"]

        # Decode base64url email message
        msg_bytes = base64.urlsafe_b64decode(raw_msg.encode("ASCII"))

        # Save the email as .eml file with message ID as filename
        eml_path = os.path.join("emails", f"{msg_id}.eml")
        with open(eml_path, "wb") as eml_file:
            eml_file.write(msg_bytes)

        print(f"Saved email {msg_id} to {eml_path}")


if __name__ == "__main__":
    main()
