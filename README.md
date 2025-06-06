# Gmail Email Downloader

This Python script uses the Gmail API to download emails from a specific Gmail label (folder) and save them as `.eml` files locally.

## Prerequisites

### 1. Install uv (Python Package Manager)

uv is a fast, modern Python package and project manager. Install it using one of these methods:

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using Homebrew (macOS):**

```bash
brew install uv
```

Verify installation:

```bash
uv --version
```

### 2. Set up Google Cloud Project & Enable Gmail API

#### Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "Gmail Email Downloader")
5. Click "Create"
6. Wait for the project to be created, then make sure it's selected in the project dropdown

#### Enable the Gmail API

1. In the left sidebar, click on "APIs & Services" > "Library"
2. In the search box, type "Gmail API"
3. Click on "Gmail API" from the search results
4. Click the "Enable" button
5. Wait for the API to be enabled (this may take a few moments)

### 3. Create OAuth 2.0 Credentials

#### Configure OAuth Consent Screen

Before creating credentials, you must configure the OAuth consent screen:

1. In Google Cloud Console, go to "APIs & Services" > "OAuth consent screen"
2. Select **User Type**:
   - Choose "External" if you don't have a Google Workspace account
   - Choose "Internal" if you have a Google Workspace account and only want internal users
3. Click "Create"
4. Fill in the OAuth consent screen form:
   - **App name**: Enter a name (e.g., "Gmail Email Downloader")
   - **User support email**: Select your email address
   - **Developer contact information**: Enter your email address
   - Leave other fields blank for now
5. Click "Save and Continue"
6. On the "Scopes" page:
   - Click "Add or Remove Scopes"
   - In the filter box, search for "gmail"
   - Select the checkbox for `https://www.googleapis.com/auth/gmail.readonly`
   - Click "Update"
   - Click "Save and Continue"
7. On the "Test users" page:
   - Click "Add Users"
   - Enter your Gmail address (and any other test accounts)
   - Click "Add"
   - Click "Save and Continue"
8. Review the summary and click "Back to Dashboard"

#### Create Desktop Application Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" at the top
3. Select "OAuth client ID"
4. For "Application type", select **Desktop app**
5. Enter a name (e.g., "Gmail Downloader Desktop Client")
6. Click "Create"
7. A dialog will appear with your Client ID and Client Secret
8. Click "Download JSON" to download the credentials file
9. **Important**: Rename the downloaded file to exactly `credentials.json`
10. Move `credentials.json` to this project directory

**Note**: Keep your `credentials.json` file secure and never commit it to version control!

## Installation

### 1. Clone or download this repository

```bash
git clone <repository-url>
cd gmail_download_tagged_emails
```

### 2. Set up Python virtual environment with uv

Create and activate a virtual environment using uv:

```bash
# uv will automatically use Python 3.11 as specified in .python-version
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

With the virtual environment activated:

```bash
# Install dependencies using uv
uv pip install -r requirements.txt
```

Alternatively, you can use uv without activating the virtual environment:

```bash
# Run commands with uv run (no activation needed)
uv run pip install -r requirements.txt
```

## Usage

### Step 1: Find Your Label ID

First, run the label listing script to find the ID of the Gmail label you want to download emails from:

```bash
# With virtual environment activated:
python list_labels.py

# Or using uv run:
uv run python list_labels.py
```

This will:

- Prompt you to authenticate with your Google account (first time only)
- Display all your Gmail labels with their IDs
- Look for your target label and copy its ID

### Step 2: Download Emails

1. Open `download_emails.py` and replace `'Label_123456'` with your actual label ID:

```python
label_id = 'Label_123456'  # Replace with your label ID
```

2. Run the download script:

```bash
# With virtual environment activated:
python download_emails.py

# Or using uv run:
uv run python download_emails.py
```

The script will:

- Create an `emails` directory if it doesn't exist
- Download up to 100 emails from the specified label
- Save each email as a `.eml` file named with its message ID

## Virtual Environment Management with uv

### Basic Commands

```bash
# Create a virtual environment (uses Python version from .python-version)
uv venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Deactivate virtual environment
deactivate

# Install packages
uv pip install package-name

# Install from requirements.txt
uv pip install -r requirements.txt

# Show installed packages
uv pip list

# Upgrade a package
uv pip install --upgrade package-name
```

### Using uv run (without activation)

You can run Python scripts without activating the virtual environment:

```bash
# Run Python scripts
uv run python script.py

# Install packages
uv run pip install package-name

# Run any command in the virtual environment context
uv run command-name
```

### Using pyproject.toml (Alternative Setup)

This project includes a `pyproject.toml` file for modern Python packaging. You can use it with uv:

```bash
# Install the project and its dependencies
uv pip install -e .

# Or sync dependencies from pyproject.toml
uv pip sync

# Create a new virtual environment with dependencies from pyproject.toml
uv venv
uv pip install -e .
```

### Managing Python Versions

```bash
# Install a specific Python version
uv python install 3.11

# List available Python versions
uv python list

# Use a different Python version for a project
echo "3.12" > .python-version
uv venv --python 3.12
```

## File Structure

```
gmail_download_tagged_emails/
├── download_emails.py       # Main script to download emails
├── list_labels.py          # Helper script to list Gmail labels
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project metadata and dependencies
├── .python-version         # Python version for uv (3.11)
├── credentials.json        # OAuth 2.0 credentials (you need to add this)
├── token.json             # Generated auth token (created automatically)
├── emails/                # Downloaded emails directory (created automatically)
├── .gitignore             # Git ignore file
├── README.md              # This file
└── SETUP_GUIDE.md         # Quick setup guide
```

## Security Notes

- **Never commit `credentials.json` or `token.json` to version control**
- The `.gitignore` file is configured to exclude these sensitive files
- The `token.json` file is created automatically after first authentication
- Store credentials securely and rotate them periodically

## Common OAuth Issues and Solutions

### "Access blocked: This app's request is invalid"

- Make sure you've properly configured the OAuth consent screen
- Verify that you've added your email as a test user
- Check that the Gmail API is enabled in your project

### "Unverified app" warning

- This is normal for development/personal use
- Click "Advanced" and then "Go to [Your App Name] (unsafe)"
- For production apps, you'll need to submit for Google verification

### "Redirect URI mismatch" error

- For Desktop apps, this shouldn't occur
- If it does, ensure you selected "Desktop app" as the application type

## Customization

- To download more than 100 emails, modify the `maxResults` parameter in `download_emails.py`
- To download from INBOX or other system labels, use:
  - `'INBOX'` for inbox
  - `'SENT'` for sent emails
  - `'TRASH'` for trash
  - `'SPAM'` for spam folder

## Troubleshooting

1. **"File not found: credentials.json"**

   - Make sure you've downloaded the OAuth credentials from Google Cloud Console
   - Rename the downloaded file to exactly `credentials.json`
   - Ensure it's in the project root directory

2. **Authentication issues**

   - Delete `token.json` and run the script again to re-authenticate
   - Ensure your Google account is added as a test user in the OAuth consent screen
   - Check that the Gmail API is enabled in your Google Cloud project

3. **"No messages found"**

   - Verify the label ID is correct using `list_labels.py`
   - Check that the label contains emails

4. **uv command not found**
   - Ensure uv is installed and added to your PATH
   - Try reopening your terminal after installation
   - On macOS/Linux, you may need to add `~/.local/bin` to your PATH

## Additional Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
