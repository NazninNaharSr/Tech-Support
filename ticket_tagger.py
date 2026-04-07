"""
ticket_tagger.py
----------------
Automatically tags and prioritizes incoming support tickets
based on keyword matching and severity heuristics.

Use case: Scale support ops by reducing manual triage time.
"""

import json
from dataclasses import dataclass, field
from typing import List

PRIORITY_KEYWORDS = {
    "critical": ["data loss", "can't log in", "billing error", "account locked", "security"],
    "high":     ["crash", "broken", "not working", "error", "bug", "extension fails"],
    "medium":   ["slow", "lag", "unexpected", "glitch", "autocomplete", "missing"],
    "low":      ["question", "how do i", "feature request", "documentation", "suggestion"],
}

CATEGORY_KEYWORDS = {
    "auth":        ["login", "sign in", "oauth", "token", "session", "password"],
    "editor":      ["cursor", "extension", "vscode", "keybinding", "tab", "autocomplete"],
    "billing":     ["invoice", "charge", "subscription", "plan", "payment", "refund"],
    "api":         ["api", "endpoint", "rate limit", "request", "response", "key"],
    "performance": ["slow", "lag", "freeze", "memory", "cpu", "latency"],
}


@dataclass
class Ticket:
    id: str
    subject: str
    body: str
    priority: str = "low"
    categories: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "priority": self.priority,
            "categories": self.categories,
        }


def triage(ticket: Ticket) -> Ticket:
    text = (ticket.subject + " " + ticket.body).lower()

    # Assign priority (highest match wins)
    for priority, keywords in PRIORITY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            ticket.priority = priority
            break

    # Assign categories (multi-label)
    ticket.categories = [
        cat for cat, keywords in CATEGORY_KEYWORDS.items()
        if any(kw in text for kw in keywords)
    ]
    if not ticket.categories:
        ticket.categories = ["general"]

    return ticket


if __name__ == "__main__":
    sample_tickets = [
        Ticket("T-001", "Can't log in after update", "Getting OAuth error since the latest release."),
        Ticket("T-002", "Autocomplete feels slow", "There's noticeable lag when using Tab completions on large files."),
        Ticket("T-003", "Feature request: better keybindings", "Would love vim-style navigation in the chat panel."),
        Ticket("T-004", "Billing charge issue", "I was charged twice this month, please help urgently."),
    ]

    triaged = [triage(t) for t in sample_tickets]
    print(json.dumps([t.to_dict() for t in triaged], indent=2))
