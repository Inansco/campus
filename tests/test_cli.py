"""CLI tests use injected input/output so no manual typing is required."""
import unittest
from campusflow.cli import choose_filter, search_menu, report_menu, run_menu

TICKETS = [
    {"id": "T001", "title": "Wi-Fi outage", "category": "Network",
     "priority": "critical", "status": "open", "assigned_to": None},
    {"id": "T002", "title": "Laptop broken", "category": "Hardware",
     "priority": "medium", "status": "resolved", "assigned_to": "Ada"},
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
        run_menu([], scripted_input("invalid", "0"), lines.append)
        self.assertTrue(any("Invalid option" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
