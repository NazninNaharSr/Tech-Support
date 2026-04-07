# Sample Support Ticket — Root Cause Analysis

> This demonstrates how I'd handle a real enterprise ticket end-to-end.

---

## Ticket T-0042

**User:** Enterprise customer, 50-seat team  
**Channel:** Slack (shared channel)  
**Severity:** High  
**Subject:** "Cursor Tab autocomplete stopped working after company proxy update"

---

### 📥 Initial Report

> "Hey team — since our IT updated our network proxy settings yesterday, Cursor's autocomplete has completely stopped working for our whole engineering org. Regular editing works fine but Tab suggestions never load. We're a 50-person team and this is blocking productivity. Please help ASAP."

---

### 🔍 Triage & Reproduction

**Questions asked:**
1. What OS and Cursor version? → macOS 14.3, Cursor 0.38.1
2. Any errors in the Output panel (Help → Toggle Developer Tools)? → `net::ERR_TUNNEL_CONNECTION_FAILED`
3. Does it reproduce on a personal network (outside the proxy)? → **No, works fine off-proxy**

This immediately points to a **proxy/TLS inspection issue**, not a Cursor bug.

---

### 🧪 Root Cause

The company's proxy performs **TLS interception (SSL inspection)**, replacing Cursor's server certificates with the proxy's own CA cert. Cursor's AI backend requests fail because the certificate chain can't be verified.

---

### ✅ Resolution

**For the user (immediate workaround):**
```json
// In Cursor Settings (settings.json):
{
  "cursor.proxyStrictSSL": false
}
```
Or, if the company CA cert is available:
```bash
# Point Node.js (which Cursor uses) to the company cert bundle
export NODE_EXTRA_CA_CERTS=/path/to/company-ca.crt
```

**Long-term fix:** Ask IT to whitelist `*.cursor.sh` and `*.anysphere.co` from SSL inspection.

---

### 📤 Engineering Escalation Note

> **Not a product bug** — proxy TLS interception breaks cert chain for AI backend calls. Recommend adding proxy/SSL docs to the troubleshooting guide. Similar issues may arise for other enterprise customers with Zscaler, Netskope, or Palo Alto proxies. Flagging to Docs team.

---

### 📊 Outcome

- Issue resolved within 2 hours of initial report
- User unblocked same day
- Docs updated with proxy troubleshooting section
- Flagged pattern to PM for potential in-app proxy detection feature
