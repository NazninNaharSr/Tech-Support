# Linux/Unix Enterprise Troubleshooting Reference

Practical commands for diagnosing and resolving issues on Linux servers in enterprise environments.

---

## System Health

```bash
# Uptime and load average
uptime

# CPU, memory, swap at a glance
free -h && top -bn1 | head -20

# Disk usage
df -h

# Inode usage (often overlooked)
df -i

# Who is logged in
w

# Last logins
last -20
```

---

## Process Management

```bash
# Find resource-hungry processes
ps aux --sort=-%cpu | head -10     # Top CPU
ps aux --sort=-%mem | head -10     # Top memory

# Find process using a specific port
ss -tlnp | grep :443
lsof -i :443

# Kill a stuck process
kill -9 <PID>

# Check process open files (useful for "too many open files" errors)
lsof -p <PID> | wc -l
```

---

## Networking

```bash
# Interface status and IPs
ip addr show
ip link show

# Routing table
ip route show

# Active connections
ss -tlnp          # listening
ss -tnp           # established

# DNS resolution test
dig hostname
nslookup hostname
cat /etc/resolv.conf

# Test connectivity
curl -Iv https://hostname         # HTTP with headers
nc -zv hostname 443               # TCP port test
traceroute hostname

# Packet capture (save for escalation)
sudo tcpdump -i eth0 host <target_ip> -w capture.pcap
```

---

## Log Analysis

```bash
# System logs
sudo journalctl -xe                        # Recent errors
sudo journalctl -u servicename --since "1 hour ago"

# Auth logs — login attempts
sudo tail -100 /var/log/auth.log           # Debian/Ubuntu
sudo tail -100 /var/log/secure             # RHEL/CentOS

# Application logs
tail -f /var/log/nginx/error.log
tail -f /var/log/syslog

# Find errors in logs quickly
grep -iE "error|fatal|critical" /var/log/syslog | tail -50

# Disk I/O issues
iostat -x 2 5
```

---

## File System & Permissions

```bash
# Find files modified in last 24 hours (useful in incident response)
find /etc -mtime -1 -type f

# Check file permissions
ls -la /path/to/file
stat /path/to/file

# Find world-writable files (security check)
find / -xdev -type f -perm -o+w 2>/dev/null

# Check disk I/O usage by process
sudo iotop -o
```

---

## Services (systemd)

```bash
# Check service status
systemctl status nginx

# Start / stop / restart
systemctl start nginx
systemctl restart nginx
systemctl stop nginx

# Enable on boot
systemctl enable nginx

# List failed services
systemctl --failed

# View service logs
journalctl -u nginx -n 50 --no-pager
```

---

## Security Checks

```bash
# List listening ports and owning processes
ss -tlnp

# Check for unauthorized SSH keys
cat ~/.ssh/authorized_keys
find / -name "authorized_keys" 2>/dev/null

# Failed SSH login attempts
grep "Failed password" /var/log/auth.log | tail -20

# Check sudoers
sudo cat /etc/sudoers

# List users with login shells (potential accounts to audit)
grep -v '/nologin\|/false' /etc/passwd

# Check for SUID binaries (privilege escalation risk)
find / -perm -4000 -type f 2>/dev/null
```

---

## Performance Triage — Quick Runbook

```
User reports: "Server is slow"

Step 1 — CPU
  top or htop → is any process at 100%?
  → If yes: identify PID, check what it is, restart if appropriate

Step 2 — Memory
  free -h → is swap in use?
  → Heavy swap = memory pressure → identify memory hog via ps aux --sort=-%mem

Step 3 — Disk
  df -h → any filesystem at >90%?
  iostat -x 2 3 → high await time = I/O bottleneck
  → find large files: du -sh /* 2>/dev/null | sort -rh | head -10

Step 4 — Network
  ss -tnp → unusual number of connections?
  iftop or nload → bandwidth saturation?

Step 5 — Logs
  journalctl -xe → any OOM kills, segfaults, or service crashes?
```
