# Security Incident Triage Playbook

A practical guide for support engineers responding to security-related user reports — from suspicious activity to potential breaches.

---

## Incident Classification

| Severity | Examples | Response Time |
|---|---|---|
| **P0 — Critical** | Active breach, credential leak, ransomware | Immediate escalation |
| **P1 — High** | Suspicious login from unknown location, MFA bypass attempt | < 1 hour |
| **P2 — Medium** | Repeated failed logins, unusual API key usage | < 4 hours |
| **P3 — Low** | General security questions, policy clarification | < 24 hours |

---

## 1. Suspicious Login / Account Compromise

### Indicators
- Login from unexpected country or IP
- Login at unusual time
- User reports "I didn't do that"

### Triage steps
```
1. Confirm the user's identity (do NOT rely on email alone for account actions)
2. Pull login history — source IP, user agent, timestamp
3. Check if MFA was used or bypassed
4. Look for: password change, API key generation, data export in the same session
5. If compromise confirmed → immediately invalidate all sessions and tokens
```

### Questions to ask the user
- When did you last successfully log in?
- Have you reused this password elsewhere?
- Do you recognize the IP/location in the login log?
- Has anyone else had access to your device recently?

---

## 2. API Key Exposure

### Indicators
- Key found in public GitHub repo
- Unusual API usage spike
- User reports accidental commit

### Triage steps
```
1. Immediately revoke the exposed key — do not wait to investigate first
2. Generate a new key for the user
3. Check API logs for unauthorized usage during the exposure window
4. If malicious usage found → escalate to Security team with timestamps + endpoints hit
5. Advise user on secret scanning tools (e.g., git-secrets, GitHub secret scanning)
```

### Recommended tools to share with user
```bash
# Scan git history for secrets before pushing
git log --all --oneline | xargs git show | grep -iE "api_key|secret|password|token"

# Better: use truffleHog
trufflehog git file://. --only-verified
```

---

## 3. Malware / Ransomware Report

### Immediate steps
```
1. DO NOT attempt to fix — contain first
2. Advise user to isolate the machine (disconnect from network, do not shut down)
3. Escalate to Security team immediately
4. Preserve: running process list, network connections, event logs
5. Do not let user wipe/reinstall until forensics are complete
```

### Preservation commands
```powershell
# Windows — capture running state before isolating
Get-Process | Export-Csv processes.csv
netstat -ano > connections.txt
Get-EventLog -LogName Security -Newest 100 | Export-Csv security_events.csv
```

```bash
# Linux
ps aux > processes.txt
ss -tlnp > connections.txt
last -100 > login_history.txt
```

---

## 4. Common Security Misconfigurations

### Overly permissive API keys
```
Risk: Key with admin scope used for read-only operations
Fix: Issue scoped keys — principle of least privilege
     Rotate keys periodically (recommend 90-day policy)
```

### No MFA enforced
```
Risk: Single factor = single point of failure
Fix: Enforce MFA at the organization level
     Prefer TOTP (e.g. Authy) over SMS-based MFA
```

### Hardcoded credentials in code
```
Risk: Credentials in source = credentials in git history forever
Fix: Use environment variables or secrets managers (AWS Secrets Manager, Vault)
     Add .env to .gitignore before first commit
```

---

## Escalation Checklist

Before escalating a security incident to the Security/Engineering team:

- [ ] Incident severity classified (P0–P3)
- [ ] Timeline established (when did it start, when detected)
- [ ] Affected accounts/systems identified
- [ ] Immediate containment taken (session revoked, key rotated, etc.)
- [ ] Evidence preserved (logs, screenshots, raw data)
- [ ] User notified of next steps
- [ ] Regulatory/compliance implications noted (e.g., does this trigger a breach notification requirement?)
