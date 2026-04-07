# API Troubleshooting Playbook

A structured guide for diagnosing common API issues reported by developers.

---

## 1. Authentication Errors (401 / 403)

**Symptoms:** `401 Unauthorized`, `403 Forbidden`, token rejected

**Checklist:**
- [ ] Is the API key present in the request header? (`Authorization: Bearer <token>`)
- [ ] Has the key expired or been revoked?
- [ ] Is the key scoped correctly for this endpoint?
- [ ] Are you hitting a staging vs. production endpoint mismatch?

**Reproduction steps:**
```bash
curl -I https://api.example.com/v1/resource \
  -H "Authorization: Bearer YOUR_TOKEN"
```
Check the response headers — `WWW-Authenticate` often hints at the root cause.

---

## 2. Rate Limiting (429)

**Symptoms:** `429 Too Many Requests`, requests suddenly failing at scale

**Checklist:**
- [ ] Check `Retry-After` or `X-RateLimit-Reset` headers in the response
- [ ] Is the user sharing an API key across multiple processes/machines?
- [ ] Is there a burst vs. sustained rate limit distinction?

**Mitigation:**
```python
import time, requests

def call_with_backoff(url, headers, retries=3):
    for i in range(retries):
        r = requests.get(url, headers=headers)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 2 ** i))
            print(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        else:
            return r
    raise Exception("Max retries exceeded")
```

---

## 3. Unexpected 500 / 502 / 504 Errors

**Symptoms:** Server errors, timeouts, gateway errors

**Checklist:**
- [ ] Is the issue reproducible consistently or intermittent?
- [ ] What's the request payload size? (Large payloads can cause gateway timeouts)
- [ ] Check the status page for ongoing incidents
- [ ] Capture the full request + response (headers + body) for escalation

**Escalation template:**
```
- Endpoint: POST /v1/completions
- Timestamp: 2025-04-07 10:32 UTC
- Request ID: (from response headers, e.g. X-Request-Id)
- Payload size: ~4KB
- Error: 502 Bad Gateway
- Frequency: ~30% of requests over the past hour
- Impact: Blocking production deployment for Enterprise customer
```

---

## 4. Malformed Responses / JSON Parsing Errors

**Symptoms:** Client crashes parsing response, unexpected nulls, schema mismatch

**Checklist:**
- [ ] Print raw response before parsing — is it valid JSON?
- [ ] Is there a deprecation notice in the docs for this field?
- [ ] Are you on an old SDK version with an outdated schema?

```python
import requests, json

r = requests.post(url, json=payload, headers=headers)
print("Status:", r.status_code)
print("Raw body:", r.text)  # Always inspect raw before parsing

try:
    data = r.json()
except json.JSONDecodeError as e:
    print("Parse error:", e)
```

---

## 5. Escalation Decision Tree

```
User reports API issue
        │
        ▼
Can you reproduce it?
   ├── No → Collect: request ID, timestamp, payload, headers
   └── Yes
        │
        ▼
Is it auth-related? → Yes → Check token scope, expiry, env mismatch
        │
        No
        ▼
Is it a 5xx? → Yes → Check status page → Escalate to Eng with request ID
        │
        No
        ▼
Is it a schema/data issue? → Yes → Check SDK version, changelog, deprecations
        │
        No
        ▼
Escalate with full repro steps + impact assessment
```
