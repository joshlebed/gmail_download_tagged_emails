# Fix OAuth "Access Blocked" Error

You're seeing this error because your email hasn't been added as a test user. Here's how to fix it:

## Quick Fix Steps

1. **Go to Google Cloud Console**

   - Visit: https://console.cloud.google.com/
   - Make sure your project is selected (should be "gmail downloader" or similar)

2. **Navigate to OAuth Consent Screen**

   - In the left sidebar: APIs & Services → OAuth consent screen

3. **Add Test Users**

   - Scroll down to the "Test users" section
   - Click "ADD USERS"
   - Enter: `joshlebed@gmail.com`
   - Click "ADD"
   - Click "SAVE" if there's a save button

4. **Verify Publishing Status**

   - At the top of the OAuth consent screen, check that "Publishing status" shows "Testing"
   - If it shows "In production", you'll need to switch back to "Testing"

5. **Try Again**
   - Run `python list_labels.py` again
   - The authentication should now work

## Alternative: If Test Users Were Already Added

If you already added yourself as a test user, try these:

1. **Clear existing token**:

   ```bash
   rm token.json
   ```

2. **Check the correct email is being used**:

   - Make sure you're logging in with the exact email added as a test user
   - Email addresses are case-sensitive in test user lists

3. **Verify the project**:
   - Ensure your `credentials.json` is from the same project where you added test users
   - You can check the project ID in the credentials.json file

## Still Having Issues?

Double-check these items in Google Cloud Console:

1. **OAuth consent screen status**: Should be "Testing" not "In production"
2. **Test users list**: Should include your exact email address
3. **Gmail API**: Should be enabled (APIs & Services → Enabled APIs)
4. **Credentials**: Should be "Desktop" type OAuth 2.0 Client ID

The error will resolve once your email is properly added as a test user.
