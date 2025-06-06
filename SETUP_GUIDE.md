# Quick Setup Guide

Follow these steps to get the Gmail Email Downloader working:

## Prerequisites: Install uv

First, install uv (a fast Python package manager):

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

## Step 1: Set up Google Cloud Project

1. Visit https://console.cloud.google.com/
2. Create a new project:
   - Click project dropdown → "New Project"
   - Name it (e.g., "Gmail Downloader")
   - Click "Create"
3. Enable Gmail API:
   - Go to "APIs & Services" → "Library"
   - Search "Gmail API" and click Enable

## Step 2: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Select "External" user type → Create
3. Fill in the form:
   - App name: "Gmail Email Downloader"
   - User support email: Your email
   - Developer contact: Your email
4. Click "Save and Continue"
5. On Scopes page:
   - Click "Add or Remove Scopes"
   - Search for "gmail"
   - Select `https://www.googleapis.com/auth/gmail.readonly`
   - Click "Update" → "Save and Continue"
6. Add test users:
   - Click "Add Users"
   - Enter your Gmail address
   - Click "Add" → "Save and Continue"
7. Review and click "Back to Dashboard"

## Step 3: Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Select "Desktop app" as application type
4. Name it "Gmail Downloader Desktop"
5. Click "Create"
6. Click "Download JSON"
7. **Important**: Rename downloaded file to `credentials.json`
8. Place it in this project directory

## Step 4: Set Up Python Environment

```bash
# Create virtual environment (uses Python 3.11)
uv venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate      # Windows

# Install dependencies
uv pip install -r requirements.txt
```

## Step 5: Find Your Label ID

```bash
python list_labels.py
```

Copy the ID of the label you want to download from.

## Step 6: Configure and Run

1. Edit `download_emails.py`
2. Replace `Label_123456` with your label ID
3. Run:

```bash
python download_emails.py
```

Your emails will be saved in the `emails/` directory as `.eml` files.

## Alternative: Using uv run (no activation needed)

Instead of activating the virtual environment, you can use `uv run`:

```bash
# Install dependencies
uv run pip install -r requirements.txt

# List labels
uv run python list_labels.py

# Download emails
uv run python download_emails.py
```

## Notes

- First run will open browser for authentication
- `token.json` will be created automatically (don't share it!)
- Default limit is 100 emails (can be changed in the script)
- Keep `credentials.json` secure and never commit to version control

## Troubleshooting

- **"Unverified app" warning**: Click "Advanced" → "Go to Gmail Email Downloader (unsafe)"
- **Authentication errors**: Delete `token.json` and try again
- **"File not found: credentials.json"**: Ensure the file is named exactly `credentials.json`
