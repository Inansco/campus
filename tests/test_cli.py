"""Engineer B CLI tests with simulated input/output."""
import unittest
from campusflow.cli import (
    add_note_menu, choose_filter, report_menu, run_menu, search_menu, view_notes_menu,
)

TICKETS = [
    {"id": "T001", "title": "Wi-Fi outage", "category": "Network",
     "priority": "critical", "status": "open", "assigned_to": None,
     "notes": [{"id": "N001", "text": "Router checked"}]},
    {"id": "T002", "title": "Laptop broken", "category": "Hardware",
     "priority": "medium", "status": "resolved", "assigned_to": "Ada", "notes": []},
]


def scripted_input(*answers):
    values = iter(answers)
    return lambda prompt="": next(values)


class CliTests(unittest.TestCase):
    def test_invalid_filter_reprompts(self):
        lines = []
        selected = choose_filter("Status", ("open", "resolved"),
                                 scripted_input("wrong", "OPEN"), lines.append)
        self.assertEqual(selected, "open")
        self.assertIn("Invalid", lines[0])

    def test_empty_filter_means_any(self):
        self.assertEqual(choose_filter("Status", ("open",), scripted_input("")), "")

    def test_search_menu_uses_all_filters(self):
        lines = []
        result = search_menu(TICKETS,
                             scripted_input("wi-fi", "Network", "open", "critical", "n"),
                             lines.append)
        self.assertEqual([t["id"] for t in result], ["T001"])
        self.assertTrue(any("Unassigned" in line for line in lines))

    def test_empty_report_menu(self):
        lines = []
        result = report_menu([], lines.append)
        self.assertEqual(result["resolution_percentage"], 0)
        self.assertIn("Resolution: 0.0%", lines)

    def test_invalid_main_menu_retries(self):
        lines = []
        run_menu([], None, scripted_input("invalid", "0"), lines.append)
        self.assertTrue(any("Invalid option" in line for line in lines))

    def test_view_notes(self):
        lines = []
        notes = view_notes_menu(TICKETS, scripted_input("t001"), lines.append)
        self.assertEqual(notes[0]["id"], "N001")
        self.assertTrue(any("Router checked" in line for line in lines))

    def test_view_notes_unknown_ticket(self):
        lines = []
        self.assertEqual(view_notes_menu(TICKETS, scripted_input("T999"), lines.append), [])
        self.assertIn("Ticket not found.", lines)

    def test_add_note_delegates_to_engineer_a_api(self):
        calls = []
        def fake_add(ticket_id, text):
            calls.append((ticket_id, text))
            return {"id": "N002", "text": text}
        lines = []
        note = add_note_menu(TICKETS, fake_add, scripted_input("T001", "Restart requested"), lines.append)
        self.assertEqual(calls, [("T001", "Restart requested")])
        self.assertEqual(note["id"], "N002")
        self.assertIn("Note added.", lines)

    def test_add_note_rejects_empty_text(self):
        calls = []
        lines = []
        result = add_note_menu(TICKETS, lambda *args: calls.append(args),
                               scripted_input("T001", "   "), lines.append)
        self.assertIsNone(result)
        self.assertEqual(calls, [])
        self.assertIn("Note cannot be empty.", lines)

    def test_add_note_handles_service_error(self):
        def broken_service(ticket_id, text):
            raise ValueError("invalid note")
        lines = []
        result = add_note_menu(TICKETS, broken_service,
                               scripted_input("T001", "hello"), lines.append)
        self.assertIsNone(result)
        self.assertTrue(any("Could not add note" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
