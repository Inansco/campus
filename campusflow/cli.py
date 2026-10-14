"""Engineer B command-line views. Business logic lives in search.py and reports.py."""
from campusflow.search import search_tickets
from campusflow.reports import ticket_report

CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def choose_filter(label, options, input_fn=input, output_fn=print):
    """Return a canonical choice or empty string; retry invalid input."""
    while True:
        value = input_fn(f"{label} ({'/'.join(options)}; Enter=any): ").strip()
        if not value:
            return ""
        for option in options:
            if option.casefold() == value.casefold():
                return option
        output_fn(f"Invalid {label.lower()}. Choose one of: {', '.join(options)}.")


def search_menu(tickets, input_fn=input, output_fn=print):
    """Prompt for search criteria and display matching tickets, without mutations."""
    title = input_fn("Title contains (Enter=any): ").strip()
    category = choose_filter("Category", CATEGORIES, input_fn, output_fn)
    status = choose_filter("Status", STATUSES, input_fn, output_fn)
    priority = choose_filter("Priority", PRIORITIES, input_fn, output_fn)
    ordered = input_fn("Sort by priority and numeric ticket ID? (y/N): ").strip().casefold() == "y"
    matches = search_tickets(tickets, title, category, status, priority, ordered)
    output_fn(f"Found {len(matches)} ticket(s).")
    for ticket in matches:
        output_fn(
            f"{ticket['id']} | {ticket['title']} | {ticket['category']} | "
            f"{ticket['priority']} | {ticket['status']} | "
            f"{ticket.get('assigned_to') or 'Unassigned'}"
        )
    return matches


def report_menu(tickets, output_fn=print):
    """Display statistics and return the report for independent testing."""
    report = ticket_report(tickets)
    output_fn(f"Total tickets: {report['total']}")
    for heading, key in (
        ("By status", "by_status"),
        ("By priority", "by_priority"),
        ("By category", "by_category"),
    ):
        output_fn(f"{heading}:")
        for label, count in sorted(report[key].items()):
            output_fn(f"  {label}: {count}")
    output_fn(f"Unresolved: {report['unresolved']}")
    output_fn(f"Resolved: {report['resolved']}")
    output_fn(f"Resolution: {report['resolution_percentage']:.1f}%")
    return report


def run_menu(tickets, input_fn=input, output_fn=print):
    """Run standalone Engineer B views against a supplied ticket collection."""
    while True:
        output_fn("\n1. Search Tickets\n2. Ticket Reports\n0. Exit")
        choice = input_fn("Choose an option: ").strip()
        if choice == "1":
            search_menu(tickets, input_fn, output_fn)
        elif choice == "2":
            report_menu(tickets, output_fn)
        elif choice == "0":
            return
        else:
            output_fn("Invalid option. Please enter 1, 2 or 0.")
