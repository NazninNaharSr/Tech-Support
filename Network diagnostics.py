"""
network_diagnostics.py
----------------------
A comprehensive network diagnostics toolkit for support engineers.
Covers DNS resolution, TCP connectivity, HTTP response, latency, and traceroute.

Usage: python network_diagnostics.py <hostname>
Example: python network_diagnostics.py api.example.com
"""

import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error


def separator(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)


def check_dns(hostname):
    separator("DNS Resolution")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"  ✅ {hostname} resolved to {ip}")
        results = socket.getaddrinfo(hostname, None)
        ips = set(r[4][0] for r in results)
        if len(ips) > 1:
            print(f"  ℹ️  Multiple IPs (round-robin/CDN): {', '.join(ips)}")
        return ip
    except socket.gaierror as e:
        print(f"  ❌ DNS resolution failed: {e}")
        print("     → Check /etc/resolv.conf or corporate DNS settings")
        return None


def check_tcp(hostname, ports=(80, 443)):
    separator("TCP Connectivity")
    for port in ports:
        try:
            start = time.time()
            sock = socket.create_connection((hostname, port), timeout=5)
            latency = round((time.time() - start) * 1000, 2)
            sock.close()
            print(f"  ✅ Port {port} open — {latency}ms")
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            print(f"  ❌ Port {port} unreachable: {e}")
            print(f"     → Possible firewall block or service down on :{port}")


def check_http(hostname):
    separator("HTTP/HTTPS Response")
    for scheme in ("http", "https"):
        url = f"{scheme}://{hostname}"
        try:
            start = time.time()
            req = urllib.request.urlopen(url, timeout=5)
            elapsed = round((time.time() - start) * 1000, 2)
            print(f"  ✅ {url} → {req.status} {req.reason} ({elapsed}ms)")
            print(f"     Server: {req.headers.get('Server', 'not disclosed')}")
        except urllib.error.HTTPError as e:
            print(f"  ⚠️  {url} → HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            print(f"  ❌ {url} failed: {e.reason}")


def check_latency(hostname, count=5):
    separator(f"Latency (ping x{count})")
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), hostname],
            capture_output=True, text=True, timeout=15
        )
        lines = result.stdout.strip().split("\n")
        for line in lines[-3:]:
            print(f"  {line}")
    except FileNotFoundError:
        # Windows fallback
        result = subprocess.run(
            ["ping", "-n", str(count), hostname],
            capture_output=True, text=True, timeout=15
        )
        print(result.stdout)
    except subprocess.TimeoutExpired:
        print("  ❌ Ping timed out — host may be blocking ICMP")


def check_traceroute(hostname):
    separator("Traceroute (first 10 hops)")
    cmd = ["traceroute", "-m", "10", hostname]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)
    except FileNotFoundError:
        print("  ℹ️  traceroute not available — try tracert on Windows")
    except subprocess.TimeoutExpired:
        print("  ❌ Traceroute timed out")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python network_diagnostics.py <hostname>")
        sys.exit(1)

    host = sys.argv[1]
    print(f"\n🔍 Running diagnostics for: {host}")

    check_dns(host)
    check_tcp(host)
    check_http(host)
    check_latency(host)
    check_traceroute(host)

    print("\n✅ Diagnostics complete.\n")
