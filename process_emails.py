#!/usr/bin/env python3
"""
Process downloaded emails: Convert EML to JSON and combine into a single file.
This script runs both conversion steps with a single command.
"""

import os
import subprocess
import sys


def run_script(script_name):
    """Run a Python script and return success status."""
    try:
        print(f"\n{'=' * 60}")
        print(f"Running {script_name}...")
        print("=" * 60)

        result = subprocess.run(
            [sys.executable, script_name], capture_output=False, text=True
        )

        if result.returncode != 0:
            print(f"Error: {script_name} failed with exit code {result.returncode}")
            return False

        return True

    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False


def main():
    """Main function to process emails."""
    print("Email Processing Pipeline")
    print("========================")
    print("This will convert your downloaded EML files to JSON and combine them.")

    # Check if emails directory exists
    if not os.path.exists("emails"):
        print("\nError: No 'emails' directory found.")
        print("Please run 'python download_emails.py' first to download emails.")
        return 1

    # Check if there are any EML files
    eml_files = [f for f in os.listdir("emails") if f.endswith(".eml")]
    if not eml_files:
        print("\nError: No EML files found in the 'emails' directory.")
        print("Please run 'python download_emails.py' first to download emails.")
        return 1

    print(f"\nFound {len(eml_files)} EML files to process.")

    # Step 1: Convert EML to JSON
    if not run_script("convert_eml_to_json.py"):
        print("\nError: Failed to convert EML files to JSON.")
        return 1

    # Step 2: Combine JSON files
    if not run_script("combine_json_files.py"):
        print("\nError: Failed to combine JSON files.")
        return 1

    print("\n" + "=" * 60)
    print("✅ Email processing complete!")
    print("=" * 60)
    print("\nOutput files created:")
    print("  - Individual JSON files in: emails_json/")
    print("  - Combined JSON file: all_emails.json")

    # Check if backup was created
    if os.path.exists("email_backups"):
        backups = [
            f for f in os.listdir("email_backups") if f.startswith("all_emails_")
        ]
        if backups:
            latest_backup = sorted(backups)[-1]
            print(f"  - Backup file: email_backups/{latest_backup}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
