import copy
import unittest
from campusflow.search import search_tickets
from campusflow.reports import ticket_report

SAMPLE = [
    {"id": "T002", "title": "Wi-Fi broken", "category": "Network", "status": "open", "priority": "high"},
    {"id": "T010", "title": "Wi-Fi slow", "category": "Network", "status": "resolved", "priority": "high"},
    {"id": "T001", "title": "Laptop issue", "category": "Hardware", "status": "in_progress", "priority": "low"},
]

class EngineerBTests(unittest.TestCase):
    def test_title_casefold(self):
        self.assertEqual(len(search_tickets(SAMPLE, title="WI-FI")), 2)
    def test_combined_filters_and(self):
        self.assertEqual([t["id"] for t in search_tickets(SAMPLE, title="wifi", category="Network", status="open")], [])
        self.assertEqual([t["id"] for t in search_tickets(SAMPLE, title="wi-fi", category="Network", status="open")], ["T002"])
    def test_search_does_not_mutate(self):
        before = copy.deepcopy(SAMPLE)
        search_tickets(SAMPLE, title="wifi", sort_by_priority=True)
        self.assertEqual(SAMPLE, before)
    def test_empty_report(self):
        self.assertEqual(ticket_report([])["resolution_percentage"], 0.0)
    def test_report_counts(self):
        report = ticket_report(SAMPLE)
        self.assertEqual((report["total"], report["unresolved"], report["resolved"]), (3, 2, 1))
    def test_priority_tie_numeric_id(self):
        result = search_tickets(SAMPLE, priority="high", sort_by_priority=True)
        self.assertEqual([t["id"] for t in result], ["T002", "T010"])
if __name__ == "__main__":
    unittest.main()
