# Project Statement — Hostel Life Manager

## 1. Title
**Hostel Life Manager** — A Modular Command-Line Application for Managing
Hostel Expenses, Personal Belongings, and Mess Meals

## 2. Problem Statement
Students and residents living in hostels or PG accommodations routinely
juggle several small but recurring administrative tasks: keeping track of
daily spending, remembering what belongings they own (and who they lent
them to), and monitoring which mess meals they've taken versus skipped
for billing purposes. These tasks are usually handled — if at all — through
scattered notes, memory, or unrelated apps, none of which are designed
for hostel life specifically. This leads to:

- Overspending due to a lack of visibility into where money goes
- Lost or forgotten personal items, especially when lent to others
- Disputes or confusion over mess bills and meal rebates
- No single place to see an overall picture of one's monthly hostel life

**Hostel Life Manager** was built to solve this by giving hostel residents
one lightweight, offline, easy-to-run tool that handles all three
concerns together, plus a combined dashboard to tie them into a single
monthly picture.

## 3. Objectives
1. Provide a simple way to log and categorize daily expenses.
2. Provide a personal inventory system with lending/returning and
   low-stock tracking for consumables.
3. Provide a mess/food tracker that records meals taken or skipped and
   estimates the resulting mess bill and rebate.
4. Provide a dashboard that consolidates data from all modules into a
   single monthly report.
5. Keep the tool dependency-free, offline, and easy to run on any machine
   with Python installed — no setup, accounts, or internet access
   required.
6. Structure the codebase into clearly separated, reusable modules so
   each feature can be maintained, tested, or extended independently.

## 4. Scope
### In scope
- Command-line interface for all four modules
- Local JSON-based data persistence (no external database)
- Expense logging, filtering, and category/monthly summaries
- Inventory tracking including lending status and low-stock alerts
- Meal-by-meal mess tracking with configurable meal rate and fixed fee
- Monthly and all-time reporting via the dashboard module

### Out of scope (possible future work)
- Multi-user accounts or authentication
- Graphical user interface (GUI) or web interface
- Cloud sync or mobile app support
- Automated bill splitting between roommates
- Export to PDF/CSV (data is currently JSON only)

## 5. Target Users
- College and university hostel residents
- PG (paying guest) accommodation residents
- Anyone wanting a minimal, private, offline way to track personal
  expenses, belongings, and meal attendance

## 6. Methodology / Approach
The application was designed around a **modular architecture**: each
feature (Expense Manager, Personal Inventory, Mess Tracker, Dashboard)
is implemented as its own Python module containing a dedicated class
with clearly defined methods for its core operations (add, list, update,
delete, summarize). A shared `utils.py` module centralizes common
concerns — JSON persistence, date handling, and console table
formatting — to avoid duplication across modules.

The `main.py` file acts purely as an orchestrator: it instantiates each
module's class and routes user choices to the corresponding menu, without
containing any business logic itself. This separation means:

- Each module can be tested, reused, or replaced independently.
- The same classes could power a future GUI or web frontend without
  rewriting the underlying logic.
- New features (e.g. a budgeting module) can be added as new files
  without touching existing code.

## 7. Tools & Technologies
| Aspect | Choice | Reason |
|---|---|---|
| Language | Python 3.7+ | Widely available, readable, no compilation step |
| Data storage | JSON files (standard library `json`) | Human-readable, no external database dependency |
| Interface | Command-line (standard library `input`/`print`) | Zero setup, runs anywhere Python runs |
| Dependencies | None (standard library only) | Keeps the project portable and easy to install |

## 8. Deliverables
- `main.py`, `utils.py`, `expense_manager.py`, `inventory_manager.py`,
  `mess_tracker.py`, `dashboard.py` — the full application source code
- `README.md` — setup instructions, feature list, and usage guide
- `STATEMENT.md` — this document
- `data/` — auto-generated folder holding the user's saved records

## 9. Success Criteria
The project is considered successful if a user can, without any
additional setup beyond having Python installed:
- Log and review expenses by category and month
- Track personal items including lending and low-stock status
- Record daily mess meals and see an estimated bill and rebate
- View a single combined snapshot of their spending and mess bill for
  any given month

## 10. Limitations
- Data is stored locally only; there is no backup or sync mechanism
  built in.
- The mess bill calculation is an estimate based on a flat per-meal rate
  and does not account for variable meal pricing.
- The application is single-user; it does not support multiple hostel
  residents sharing one installation with separate data.
