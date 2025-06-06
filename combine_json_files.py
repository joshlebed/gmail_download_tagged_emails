import glob
import json
import os
from datetime import datetime


def combine_json_files(json_dir="emails_json", output_file="all_emails.json"):
    """Combine all JSON files in a directory into a single JSON file."""

    # Check if the JSON directory exists
    if not os.path.exists(json_dir):
        print(
            f"Directory '{json_dir}' not found. Please run convert_eml_to_json.py first."
        )
        return False

    # Find all JSON files in the directory
    json_files = glob.glob(os.path.join(json_dir, "*.json"))

    if not json_files:
        print(f"No JSON files found in '{json_dir}' directory.")
        return False

    print(f"Found {len(json_files)} JSON files to combine.")

    # List to store all email objects
    all_emails = []
    successful = 0
    failed = 0

    # Read each JSON file and add to the list
    for json_path in json_files:
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                email_data = json.load(f)

                # Add the filename (without extension) as an ID field
                email_id = os.path.splitext(os.path.basename(json_path))[0]
                email_data["id"] = email_id

                all_emails.append(email_data)
                successful += 1

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {json_path}: {e}")
            failed += 1
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
            failed += 1

    # Sort emails by ID (which are the original message IDs from Gmail)
    all_emails.sort(key=lambda x: x.get("id", ""))

    # Save the combined data to a single JSON file
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_emails, f, indent=2, ensure_ascii=False)

        print(f"\nSuccessfully combined {successful} emails into '{output_file}'")
        if failed > 0:
            print(f"Failed to process {failed} files")

        # Print summary statistics
        print("\nSummary:")
        print(f"- Total emails: {len(all_emails)}")
        print(f"- Output file: {output_file}")
        print(f"- File size: {os.path.getsize(output_file) / 1024:.2f} KB")

        return True

    except Exception as e:
        print(f"Error writing combined JSON file: {e}")
        return False


def main():
    # Create backups directory if it doesn't exist
    backups_dir = "email_backups"
    os.makedirs(backups_dir, exist_ok=True)

    # You can customize the output filename here
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = os.path.join(backups_dir, f"all_emails_{timestamp}.json")

    # Combine all JSON files
    if combine_json_files(output_file=output_filename):
        print("\nYou can also run this script with a custom output filename:")
        print(f"  python {os.path.basename(__file__)} --output custom_name.json")

    # Also create a simplified version without timestamp for easy access
    combine_json_files(output_file="all_emails.json")


if __name__ == "__main__":
    import sys

    # Simple command line argument handling
    if len(sys.argv) > 2 and sys.argv[1] == "--output":
        output_file = sys.argv[2]
        combine_json_files(output_file=output_file)
    else:
        main()
