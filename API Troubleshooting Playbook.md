# Troubleshooting: AI Autocomplete Not Working

**Applies to:** AI-powered developer tools with inline code suggestions
**Last updated:** April 2025

---

## Quick Checklist

Before diving in, confirm:
- [ ] You're signed in to your account
- [ ] AI suggestions are enabled in Settings
- [ ] You have an active subscription

---

## Common Issues & Fixes

### 1. Autocomplete not triggering at all

**Possible cause:** Conflicting keybinding from another extension.

**Fix:**
1. Open Command Palette → `Preferences: Open Keyboard Shortcuts`
2. Search for `Tab` — check if another extension has claimed it
3. Re-bind `editor.action.inlineSuggest.commit` to `Tab`

---

### 2. Suggestions appear but are always empty / grey

**Possible cause:** Unsupported file type, or the model is timing out.

**Fix:**
- Check the status bar at the bottom for error indicators
- Open the developer console and look for network errors
- Try on a `.py` or `.ts` file to confirm it's file-type specific

---

### 3. Not working on a corporate network / VPN

**Possible cause:** Corporate proxy or SSL inspection blocking AI backend requests.

**Fix:**
```json
// Add to your settings.json:
{
  "proxyStrictSSL": false
}
```
If your company uses a custom CA certificate, set:
```bash
export NODE_EXTRA_CA_CERTS=/path/to/your-ca-bundle.crt
```
Then restart the app.

> 🔒 **IT admins:** Whitelist the app's backend domains from SSL inspection for best results.

---

### 4. Autocomplete stopped working after an update

**Fix:**
1. Confirm you're on the latest version
2. Disable all extensions temporarily and test
3. Reset AI settings via the Command Palette

---

## Still stuck?

Collect the following before contacting support — it helps us resolve faster:

- App version
- OS and version
- Any errors from the developer console
- Does the issue reproduce in a new empty project?
