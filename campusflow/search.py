"""Read-only CampusFlow ticket search."""
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def search_tickets(tickets, title="", category="", status="", priority="", sort_by_priority=False):
    """Return tickets matching ALL supplied filters without changing input."""
    values = tickets.values() if isinstance(tickets, dict) else tickets
    result = [
        ticket for ticket in values
        if title.casefold() in ticket["title"].casefold()
        and (not category or ticket["category"].casefold() == category.casefold())
        and (not status or ticket["status"].casefold() == status.casefold())
        and (not priority or ticket["priority"].casefold() == priority.casefold())
    ]
    if sort_by_priority:
        result.sort(key=lambda t: (PRIORITY_ORDER[t["priority"].lower()], int(t["id"][1:])))
    return result
