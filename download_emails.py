import argparse
import base64
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download emails from a Gmail label")
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=100,
        help="Number of emails to download (default: 100)",
    )
    parser.add_argument(
        "--label",
        "-l",
        type=str,
        default="Label_8860527106742868850",
        help="Gmail label ID or name (e.g., 'INBOX', 'Label_123456')",
    )
    return parser.parse_args()


def download_emails_batch(service, label_id, max_count):
    """Download emails with pagination support."""
    emails_downloaded = 0
    page_token = None
    all_messages = []

    # Gmail API allows max 500 results per request
    max_per_request = 500

    print(f"Fetching up to {max_count} emails from label '{label_id}'...")

    while emails_downloaded < max_count:
        try:
            # Calculate how many to request in this batch
            remaining = max_count - emails_downloaded
            batch_size = min(remaining, max_per_request)

            # Build the request
            if page_token:
                results = (
                    service.users()
                    .messages()
                    .list(
                        userId="me",
                        labelIds=[label_id],
                        maxResults=batch_size,
                        pageToken=page_token,
                    )
                    .execute()
                )
            else:
                results = (
                    service.users()
                    .messages()
                    .list(userId="me", labelIds=[label_id], maxResults=batch_size)
                    .execute()
                )

            messages = results.get("messages", [])
            if not messages:
                break

            all_messages.extend(messages)
            emails_downloaded += len(messages)

            print(f"  Fetched {len(messages)} emails (Total: {emails_downloaded})")

            # Check if there are more pages
            page_token = results.get("nextPageToken")
            if not page_token:
                break

        except Exception as e:
            print(f"Error fetching emails: {e}")
            break

    return all_messages[:max_count]  # Ensure we don't exceed requested count


def main():
    # Parse command line arguments
    args = parse_arguments()

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

    # Get emails using pagination
    messages = download_emails_batch(service, args.label, args.count)

    if not messages:
        print("No messages found.")
        return

    print(f"\nDownloading {len(messages)} emails...")

    # Create directory to save emails
    os.makedirs("emails", exist_ok=True)

    # Download each email
    for i, msg in enumerate(messages, 1):
        msg_id = msg["id"]
        try:
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

            print(f"[{i}/{len(messages)}] Saved email {msg_id}")

        except Exception as e:
            print(f"[{i}/{len(messages)}] Error downloading email {msg_id}: {e}")

    print(
        f"\n✅ Download complete! Saved {len(messages)} emails to 'emails/' directory."
    )


if __name__ == "__main__":
    main()
