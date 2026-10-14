# CampusFlow — Engineer B Development Branch

This is a personal practice branch for Engineer B's **CampusFlow Next** work. The current code provides ticket searching, reporting, and an interactive menu. It is not yet the full original CampusFlow application.

## Requirements

Python 3.10 or later; Python standard library only. Run commands from the repository root.

## Clone and switch to the Engineer B branch

```bash
git clone https://github.com/Inansco/campus.git
cd campus
git switch feat/engineer-b-search-and-reports
```

If you already cloned the repository, use:

```bash
cd campus
git fetch origin
git switch feat/engineer-b-search-and-reports
git pull
```

## Run automated tests

```bash
python3 -m unittest discover -s tests -v
```

On Windows, replace `python3` with `python` (or `py`) if needed.

## Start the interactive CLI

```bash
python3 -c "from campusflow.cli import run_menu; run_menu([])"
```

The `[]` means **no tickets are loaded**. The menu lets you choose:

- `1` — Search Tickets (title, category, status, priority, optional priority/ID sorting)
- `2` — Ticket Reports (total, status, priority, category, unresolved, resolved, resolution percentage)
- `0` — Exit

An empty dataset returns no search results and 0.0% resolution. This starter menu **does not yet create tickets or load JSON**.

### Try the CLI with sample tickets

To experiment with nonempty search results, create a file called `demo.py` in the repository root:

```python
from campusflow.cli import run_menu

tickets = [
    {"id": "T001", "title": "Wi-Fi outage", "category": "Network",
     "urgency": "high", "affected_users": 12, "priority": "critical",
     "status": "open", "assigned_to": None, "notes": []},
    {"id": "T002", "title": "Laptop issue", "category": "Hardware",
     "urgency": "medium", "affected_users": 1, "priority": "medium",
     "status": "resolved", "assigned_to": "Ada", "notes": []},
]
run_menu(tickets)
```

Then run `python3 demo.py` (or `python demo.py` on Windows). This demonstration uses temporary in-memory sample data only.

## Project layout

- `campusflow/search.py` — read-only title substring search with case-insensitive matching and AND-combined filters.
- `campusflow/reports.py` — summary counts and resolution percentage, including the zero-ticket case.
- `campusflow/cli.py` — interactive search and report menus, with retry on invalid filter choices.
- `tests/test_engineer_b.py` — initial search and report tests.
- `tests/test_cli.py` — CLI tests with simulated user input.

## Scope and remaining work

Engineer B still needs the six-question Engineering Understanding Check, note-entry and note-view menus connected to Engineer A's business APIs, and integration with the existing CampusFlow ticket workflow. The shared assignment requires preserving original ticket creation, priority rules, assignment, transitions, Open Work Queue, and safe JSON storage. The personal repository is for practice before contributing to the shared repository.

## Working with the shared repository

Develop on the feature branch, run the tests, then open a pull request against the **shared original CampusFlow repository** once the code is integrated and reviewed. Do not assume the personal repo's `main` is the instructor's required original application.
