"""Ticket analytics with safe zero-ticket handling."""
from collections import Counter

def ticket_report(tickets):
    values = list(tickets.values() if isinstance(tickets, dict) else tickets)
    total = len(values)
    statuses = Counter(t["status"] for t in values)
    priorities = Counter(t["priority"] for t in values)
    categories = Counter(t["category"] for t in values)
    resolved = statuses["resolved"]
    return {
        "total": total,
        "by_status": dict(statuses),
        "by_priority": dict(priorities),
        "by_category": dict(categories),
        "unresolved": statuses["open"] + statuses["in_progress"],
        "resolved": resolved,
        "resolution_percentage": resolved / total * 100 if total else 0.0,
    }
