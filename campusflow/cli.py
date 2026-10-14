"""Engineer B CLI: search/filtering, reports, notes UI, and friendly error handling.

Ticket/note validation, ID generation, and persistence remain Engineer A responsibilities.
The CLI delegates note creation to an injected add_note_fn when one is available.
"""
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


def _ticket_by_id(tickets, ticket_id):
    values = tickets.values() if isinstance(tickets, dict) else tickets
    wanted = ticket_id.strip().casefold()
    return next((t for t in values if str(t.get("id", "")).casefold() == wanted), None)


def search_menu(tickets, input_fn=input, output_fn=print):
    """Prompt for search criteria and display matching tickets, without mutations."""
    title = input_fn("Title contains (Enter=any): ").strip()
    category = choose_filter("Category", CATEGORIES, input_fn, output_fn)
    status = choose_filter("Status", STATUSES, input_fn, output_fn)
    priority = choose_filter("Priority", PRIORITIES, input_fn, output_fn)
    ordered = input_fn("Sort by priority and numeric ticket ID? (y/N): ").strip().casefold() == "y"
    try:
        matches = search_tickets(tickets, title, category, status, priority, ordered)
    except (KeyError, TypeError, ValueError) as exc:
        output_fn(f"Unable to search tickets: {exc}")
        return []
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
    try:
        report = ticket_report(tickets)
    except (KeyError, TypeError, ValueError) as exc:
        output_fn(f"Unable to generate report: {exc}")
        return None
    output_fn(f"Total tickets: {report['total']}")
    for heading, key in (("By status", "by_status"), ("By priority", "by_priority"), ("By category", "by_category")):
        output_fn(f"{heading}:")
        for label, count in sorted(report[key].items()):
            output_fn(f"  {label}: {count}")
    output_fn(f"Unresolved: {report['unresolved']}")
    output_fn(f"Resolved: {report['resolved']}")
    output_fn(f"Resolution: {report['resolution_percentage']:.1f}%")
    return report


def view_notes_menu(tickets, input_fn=input, output_fn=print):
    """View notes for one ticket. Reading notes is an Engineer B CLI responsibility."""
    ticket_id = input_fn("Ticket ID: ").strip()
    ticket = _ticket_by_id(tickets, ticket_id)
    if ticket is None:
        output_fn("Ticket not found.")
        return []
    notes = ticket.get("notes", [])
    output_fn(f"Notes for {ticket['id']}: {len(notes)}")
    for note in notes:
        if isinstance(note, dict):
            note_id = note.get("id", "NOTE")
            text = note.get("text", note.get("body", ""))
            output_fn(f"{note_id}: {text}")
        else:
            output_fn(str(note))
    return notes


def add_note_menu(tickets, add_note_fn, input_fn=input, output_fn=print):
    """Collect note input, then delegate validation/ID/persistence to Engineer A's API."""
    ticket_id = input_fn("Ticket ID: ").strip()
    if _ticket_by_id(tickets, ticket_id) is None:
        output_fn("Ticket not found.")
        return None
    text = input_fn("Note: ").strip()
    if not text:
        output_fn("Note cannot be empty.")
        return None
    if add_note_fn is None:
        output_fn("Note service is not connected.")
        return None
    try:
        note = add_note_fn(ticket_id, text)
    except (KeyError, TypeError, ValueError) as exc:
        output_fn(f"Could not add note: {exc}")
        return None
    output_fn("Note added.")
    return note


def run_menu(tickets, add_note_fn=None, input_fn=input, output_fn=print):
    """Run Engineer B views against a supplied ticket collection."""
    while True:
        output_fn("\n1. Search Tickets\n2. Ticket Reports\n3. Add Ticket Note\n4. View Ticket Notes\n0. Exit")
        choice = input_fn("Choose an option: ").strip()
        if choice == "1":
            search_menu(tickets, input_fn, output_fn)
        elif choice == "2":
            report_menu(tickets, output_fn)
        elif choice == "3":
            add_note_menu(tickets, add_note_fn, input_fn, output_fn)
        elif choice == "4":
            view_notes_menu(tickets, input_fn, output_fn)
        elif choice == "0":
            return
        else:
            output_fn("Invalid option. Please enter 1, 2, 3, 4 or 0.")
