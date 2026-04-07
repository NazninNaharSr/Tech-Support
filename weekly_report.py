"""
weekly_report.py
----------------
Generates a weekly support metrics summary from a CSV of ticket data.
Useful for sharing trends with PM and Engineering.

Expected CSV columns: id, date, priority, category, status, resolution_time_hrs
"""

import csv
import json
from collections import Counter, defaultdict
from statistics import mean

SAMPLE_DATA = [
    {"id": "T-001", "date": "2025-04-01", "priority": "high",     "category": "editor",      "status": "resolved", "resolution_time_hrs": 2.5},
    {"id": "T-002", "date": "2025-04-01", "priority": "medium",   "category": "auth",        "status": "resolved", "resolution_time_hrs": 4.0},
    {"id": "T-003", "date": "2025-04-02", "priority": "critical", "category": "billing",     "status": "resolved", "resolution_time_hrs": 1.0},
    {"id": "T-004", "date": "2025-04-02", "priority": "low",      "category": "editor",      "status": "open",     "resolution_time_hrs": None},
    {"id": "T-005", "date": "2025-04-03", "priority": "high",     "category": "api",         "status": "resolved", "resolution_time_hrs": 3.5},
    {"id": "T-006", "date": "2025-04-03", "priority": "medium",   "category": "performance", "status": "resolved", "resolution_time_hrs": 6.0},
    {"id": "T-007", "date": "2025-04-04", "priority": "high",     "category": "editor",      "status": "open",     "resolution_time_hrs": None},
    {"id": "T-008", "date": "2025-04-05", "priority": "low",      "category": "auth",        "status": "resolved", "resolution_time_hrs": 8.0},
]


def generate_report(tickets):
    total = len(tickets)
    resolved = [t for t in tickets if t["status"] == "resolved"]
    open_tickets = [t for t in tickets if t["status"] == "open"]

    priority_counts = Counter(t["priority"] for t in tickets)
    category_counts = Counter(t["category"] for t in tickets)

    resolution_times = [t["resolution_time_hrs"] for t in resolved if t["resolution_time_hrs"]]
    avg_resolution = round(mean(resolution_times), 2) if resolution_times else "N/A"

    report = {
        "week_summary": {
            "total_tickets": total,
            "resolved": len(resolved),
            "open": len(open_tickets),
            "resolution_rate": f"{round(len(resolved)/total*100)}%",
            "avg_resolution_time_hrs": avg_resolution,
        },
        "by_priority": dict(priority_counts),
        "by_category": dict(category_counts),
        "open_tickets": [t["id"] for t in open_tickets],
    }
    return report


if __name__ == "__main__":
    report = generate_report(SAMPLE_DATA)
    print("=" * 50)
    print("  Weekly Support Report")
    print("=" * 50)
    print(json.dumps(report, indent=2))
