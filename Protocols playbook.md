# Network Protocols — Troubleshooting Playbook

A practical reference for diagnosing network issues at the protocol/configuration level in enterprise environments.

---

## DNS

### How it works
DNS resolves hostnames to IPs via a hierarchy: Resolver → Root → TLD → Authoritative nameserver.

### Common issues & fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `NXDOMAIN` | Hostname doesn't exist | Check spelling, verify DNS zone |
| `SERVFAIL` | Authoritative server unreachable | Check nameserver health |
| Resolution works externally, fails internally | Split-horizon DNS misconfiguration | Compare internal vs. external resolver results |
| Stale IP returned | TTL too high / cached record | `ipconfig /flushdns` (Win) or `resolvectl flush-caches` (Linux) |

### Useful commands
```bash
# Query specific DNS server
nslookup hostname 8.8.8.8

# Detailed DNS trace
dig +trace hostname

# Check what resolver is being used
cat /etc/resolv.conf              # Linux
ipconfig /all | grep "DNS"        # Windows
```

---

## TCP/IP

### Three-way handshake
```
Client → SYN      →  Server
Client ← SYN-ACK  ←  Server
Client → ACK       →  Server
[Connection established]
```

### Common issues & fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `Connection refused` | Service not listening on port | Check service status, correct port |
| `Connection timed out` | Firewall dropping packets silently | Check firewall rules, security groups |
| High retransmissions | Packet loss / congestion | Check `netstat -s`, MTU mismatch |
| SYN flood symptoms | DDoS / misconfigured client | Check SYN cookies, rate limiting |

```bash
# Check open ports and listening services
ss -tlnp                          # Linux (preferred over netstat)
netstat -ano | findstr LISTENING  # Windows

# Test TCP connectivity
nc -zv hostname 443               # Linux
Test-NetConnection hostname -Port 443  # Windows PowerShell
```

---

## TLS/SSL

### Handshake flow
```
Client Hello (supported ciphers, TLS version)
  → Server Hello (chosen cipher, certificate)
  → Client verifies cert chain
  → Key exchange → Session keys derived
  → Encrypted communication begins
```

### Common issues & fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `certificate verify failed` | Self-signed or expired cert | Check cert validity, add CA to trust store |
| `ERR_TUNNEL_CONNECTION_FAILED` | Corporate proxy doing TLS inspection | Whitelist domain or add corporate CA cert |
| `SSL_ERROR_RX_RECORD_TOO_LONG` | HTTP traffic hitting HTTPS port | Confirm scheme (http vs https) |
| Cipher mismatch | Client/server TLS version gap | Update TLS config, check min version |

```bash
# Inspect certificate details
openssl s_client -connect hostname:443

# Check cert expiry
echo | openssl s_client -servername hostname -connect hostname:443 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## HTTP/HTTPS

### Key status codes for support engineers

| Code | Meaning | Common cause |
|---|---|---|
| 401 | Unauthorized | Missing/invalid auth token |
| 403 | Forbidden | Token valid but lacks permission |
| 429 | Too Many Requests | Rate limit hit |
| 502 | Bad Gateway | Upstream service down |
| 504 | Gateway Timeout | Upstream too slow, request timeout |

---

## DHCP

### Lease process (DORA)
```
Discover → Offer → Request → Acknowledge
```

### Common issues
```bash
# Release and renew lease
ipconfig /release && ipconfig /renew     # Windows
dhclient -r && dhclient                  # Linux

# Check current lease
ipconfig /all                            # Windows
cat /var/lib/dhcp/dhclient.leases        # Linux
```

---

## Firewall & Routing

```bash
# View routing table
ip route show          # Linux
route print            # Windows

# Check if traffic is being dropped
sudo tcpdump -i eth0 host <target_ip>    # Linux packet capture

# Test path MTU (helps diagnose fragmentation issues)
ping -M do -s 1472 hostname             # Linux
ping -f -l 1472 hostname               # Windows
```

---

## Escalation Template — Network Issue

```
Issue: [Brief description]
Affected users: [Count / team]
Onset: [When did it start?]

Diagnostics run:
- DNS: [resolved / failed — output]
- TCP: [port reachable / refused / timed out]
- Traceroute: [where does it drop?]
- Packet capture: [any anomalies?]

Works on: [personal network / different VLAN / external]
Fails on: [corporate network / specific subnet / VPN]

Hypothesis: [Your best guess at root cause]
Impact: [Blocking / degraded / intermittent]
```
