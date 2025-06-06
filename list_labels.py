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

    # List all labels
    labels = service.users().labels().list(userId="me").execute().get("labels", [])

    print("Gmail Labels:")
    print("-" * 50)
    for label in labels:
        print(f"{label['name']} - {label['id']}")


if __name__ == "__main__":
    main()
