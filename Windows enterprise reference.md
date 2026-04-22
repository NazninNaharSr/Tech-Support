# Windows Enterprise Troubleshooting Reference

Quick-reference commands and playbooks for diagnosing Windows issues in enterprise environments.

---

## System Health Check

```powershell
# System info snapshot
Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, CsProcessors, CsTotalPhysicalMemory

# Check uptime
(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime

# Disk usage
Get-PSDrive -PSProvider FileSystem | Select-Object Name, Used, Free

# Top CPU-consuming processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet
```

---

## Networking

```powershell
# Full network adapter info (IPs, DNS, gateway)
ipconfig /all

# Flush DNS cache
ipconfig /flushdns

# Test connectivity
Test-NetConnection google.com -Port 443

# View routing table
route print

# Active connections
netstat -ano

# Map PID to process name
Get-Process -Id (netstat -ano | Select-String "ESTABLISHED" | ForEach-Object { ($_ -split "\s+")[5] } | Select-Object -Unique)
```

---

## Active Directory / Domain

```powershell
# Check domain join status
(Get-WmiObject Win32_ComputerSystem).PartOfDomain

# Current user's group memberships
whoami /groups

# Query AD user account status
net user username /domain

# Force Group Policy update
gpupdate /force

# View applied GPOs
gpresult /r
```

---

## Services & Processes

```powershell
# List all running services
Get-Service | Where-Object {$_.Status -eq "Running"}

# Check a specific service
Get-Service -Name "wuauserv"  # Windows Update

# Restart a service
Restart-Service -Name "Spooler" -Force

# Find what's using a port
netstat -ano | findstr :443
Get-Process -Id <PID_from_above>
```

---

## Event Logs

```powershell
# Last 20 system errors
Get-EventLog -LogName System -EntryType Error -Newest 20

# Last 20 security events (login attempts)
Get-EventLog -LogName Security -Newest 20 | Select-Object TimeGenerated, EventID, Message

# Key Security Event IDs
# 4624 — Successful logon
# 4625 — Failed logon
# 4648 — Logon with explicit credentials
# 4720 — User account created
# 4726 — User account deleted
# 7045 — New service installed (common malware indicator)

# Export logs for escalation
Get-EventLog -LogName Security -Newest 100 | Export-Csv security_events.csv -NoTypeInformation
```

---

## Windows Firewall

```powershell
# Check firewall status for all profiles
Get-NetFirewallProfile | Select-Object Name, Enabled

# List inbound rules
Get-NetFirewallRule -Direction Inbound | Where-Object {$_.Enabled -eq "True"} | Select-Object DisplayName, Action

# Temporarily disable firewall (for testing — re-enable after!)
Set-NetFirewallProfile -All -Enabled False
# Re-enable:
Set-NetFirewallProfile -All -Enabled True
```

---

## Common Enterprise Issues

### User can't log in after password reset
```powershell
# Check account lockout status
net user username /domain | findstr "Account active"
net user username /domain | findstr "locked"

# Unlock account (run as Domain Admin)
Unlock-ADAccount -Identity username
```

### Application won't start — DLL errors
```powershell
# Check for missing dependencies
# Run the app from cmd and capture error
cmd /c "app.exe" 2>&1

# Check if Visual C++ redistributable is installed
Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Visual C++*"}
```

### Slow machine — quick triage
```powershell
# CPU + Memory at a glance
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5 Name, CPU, @{N='RAM_MB';E={[math]::Round($_.WorkingSet/1MB,1)}}

# Check for disk I/O bottleneck
# Open Resource Monitor → Disk tab (GUI)
# Or:
Get-Counter '\PhysicalDisk(*)\Disk Bytes/sec' -SampleInterval 2 -MaxSamples 5
```
