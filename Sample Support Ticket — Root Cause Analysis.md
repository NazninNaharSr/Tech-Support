# Sample Support Ticket — Root Cause Analysis

> A real-world style enterprise ticket worked end-to-end, demonstrating triage, reproduction, root cause analysis, and escalation.

---

## Ticket T-0042

**User:** Enterprise customer, 50-seat team  
**Channel:** Slack (shared channel)  
**Severity:** High  
**Subject:** "AI-powered code suggestions stopped working after company proxy update"

---

### 📥 Initial Report

> "Hey team — since our IT updated our network proxy settings yesterday, the AI code suggestions in our dev tooling have completely stopped working for our whole engineering org. Regular editing works fine but suggestions never load. We're a 50-person team and this is blocking productivity. Please help ASAP."

---

### 🔍 Triage & Reproduction

**Questions asked:**
1. What OS and app version? → macOS 14.3, app v0.38.1
2. Any errors in the developer console / output panel? → `net::ERR_TUNNEL_CONNECTION_FAILED`
3. Does it reproduce on a personal network (outside the proxy)? → **No, works fine off-proxy**

This immediately points to a **proxy/TLS inspection issue**, not a Cursor bug.

---

### 🧪 Root Cause

The company's proxy performs **TLS interception (SSL inspection)**, replacing Cursor's server certificates with the proxy's own CA cert. Cursor's AI backend requests fail because the certificate chain can't be verified.

---

### ✅ Resolution

**For the user (immediate workaround):**
```json
// In app settings (settings.json):
{
  "proxyStrictSSL": false
}
```
Or, if the company CA cert is available:
```bash
# Point Node.js to the company cert bundle
export NODE_EXTRA_CA_CERTS=/path/to/company-ca.crt
```

**Long-term fix:** Ask IT to whitelist the app's backend domains from SSL inspection.

---

### 📤 Engineering Escalation Note

> **Not a product bug** — corporate proxy TLS interception breaks the cert chain for AI backend calls. Recommend adding proxy/SSL docs to the troubleshooting guide. Similar issues likely for other enterprise customers using Zscaler, Netskope, or Palo Alto proxies. Flagging to Docs team.

---

### 📊 Outcome

- Issue resolved within 2 hours of initial report
- Entire 50-person team unblocked same day
- Docs updated with proxy troubleshooting section
- Flagged pattern to PM as potential candidate for in-app proxy detection feature
