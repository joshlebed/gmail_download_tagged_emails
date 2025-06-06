import glob
import json
import os
from email import policy
from email.parser import BytesParser


def extract_plain_text_body(msg):
    """Extract plain text body from email message."""
    body = ""

    if msg.is_multipart():
        # Walk through all parts of the email
        for part in msg.walk():
            # Look for text/plain parts
            if part.get_content_type() == "text/plain":
                try:
                    # Decode the content
                    body = part.get_content()
                    break  # Use the first text/plain part found
                except Exception as e:
                    print(f"Error extracting body: {e}")
                    continue
    else:
        # For non-multipart messages
        if msg.get_content_type() == "text/plain":
            try:
                body = msg.get_content()
            except Exception as e:
                print(f"Error extracting body: {e}")

    return body.strip() if body else ""


def convert_eml_to_json(eml_path, json_path):
    """Convert a single EML file to JSON with sender, subject, and body."""
    try:
        # Read the EML file
        with open(eml_path, "rb") as f:
            # Parse the email using BytesParser with policy for better handling
            msg = BytesParser(policy=policy.default).parse(f)

        # Extract the required fields
        sender = msg.get("From", "")
        subject = msg.get("Subject", "")
        body = extract_plain_text_body(msg)

        # Create the JSON data
        email_data = {"sender": sender, "subject": subject, "body": body}

        # Save to JSON file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(email_data, f, indent=2, ensure_ascii=False)

        print(
            f"Converted {os.path.basename(eml_path)} to {os.path.basename(json_path)}"
        )
        return True

    except Exception as e:
        print(f"Error processing {eml_path}: {e}")
        return False


def main():
    # Check if emails directory exists
    if not os.path.exists("emails"):
        print("No 'emails' directory found. Please run download_emails.py first.")
        return

    # Find all EML files in the emails directory
    eml_files = glob.glob(os.path.join("emails", "*.eml"))

    if not eml_files:
        print("No EML files found in the emails directory.")
        return

    print(f"Found {len(eml_files)} EML files to convert.")

    # Create directory for JSON files
    os.makedirs("emails_json", exist_ok=True)

    # Convert each EML file
    successful = 0
    failed = 0

    for eml_path in eml_files:
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(eml_path))[0]

        # Create JSON filename with same base name
        json_path = os.path.join("emails_json", f"{base_name}.json")

        if convert_eml_to_json(eml_path, json_path):
            successful += 1
        else:
            failed += 1

    print("\nConversion complete!")
    print(f"Successfully converted: {successful} files")
    if failed > 0:
        print(f"Failed to convert: {failed} files")


if __name__ == "__main__":
    main()
