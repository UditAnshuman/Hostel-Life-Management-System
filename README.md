#  Hostel Life Manager

A simple, dependency-free **command-line application** to help hostel and
PG residents manage their daily life — expenses, belongings, mess meals,
and an at-a-glance dashboard — all from one terminal menu.

Built entirely with Python's standard library. No installation of
third-party packages required, no database server, no internet
connection needed. All your data is saved locally as JSON files.

---

##  Features

The app is organized into four independent modules, tied together by a
single main menu.

### 1.  Expense Manager (`expense_manager.py`)
Track every rupee you spend.
- Add expenses with date, category, description, and amount
- Built-in categories: Food, Travel, Stationery, Laundry, Mobile/Internet,
  Entertainment, Groceries, Medical, Other
- View all expenses or filter by month / category
- Category-wise spending summary for the current month
- Delete an expense by ID

### 2.  Personal Inventory (`inventory_manager.py`)
Keep track of everything you own in your room.
- Add items with category, quantity, and storage location
- Increase/decrease quantity (e.g. use up toiletries, restock supplies)
- Lend items to friends and mark them as returned
- Automatic **low-stock alerts** based on a threshold you set per item
- Filter items by category

### 3.  Mess / Food Tracker (`mess_tracker.py`)
Log which meals you actually ate.
- Mark Breakfast / Lunch / Dinner as taken or skipped, for any date
- View your meal log for the current month
- Set a **per-meal rate** and an optional fixed monthly mess fee
- Get an **estimated monthly mess bill** and the **rebate** you're owed
  for skipped meals

### 4.  Dashboard & Reports (`dashboard.py`)
Everything pulled together in one view.
- Monthly snapshot: total spending, category breakdown, mess bill,
  low-stock items, and items currently lent out
- Combined **total spend** (expenses + mess bill) for the period
- All-time monthly expense trend

---

##  Project Structure

```
hostel_life_manager/
├── main.py                # Entry point — run this file
├── utils.py                # Shared helpers (storage, dates, table printing)
├── expense_manager.py      # Module 1: Expense Manager
├── inventory_manager.py    # Module 2: Personal Inventory
├── mess_tracker.py         # Module 3: Mess / Food Tracker
├── dashboard.py             # Module 4: Dashboard & Reports
└── data/                   # Auto-created on first run — your saved data
    ├── expenses.json
    ├── inventory.json
    ├── mess.json
    └── mess_settings.json
```

Each feature is a self-contained module with its own class
(`ExpenseManager`, `InventoryManager`, `MessTracker`, `Dashboard`), so
you can import and reuse them independently of the CLI — for example,
in a script, a Jupyter notebook, or a future GUI/web frontend.

---

##  Requirements

- Python **3.7+**
- No external libraries — only the standard library (`json`, `os`,
  `datetime`, `collections`) is used

---

##  Getting Started

1. Unzip / clone the project and move into the folder:
   ```bash
   cd hostel_life_manager
   ```
2. Run the app:
   ```bash
   python main.py
   ```
3. You'll see the main menu:
   ```
   ==================================================
             HOSTEL LIFE MANAGER
   ==================================================
     1. Expense Manager
     2. Personal Inventory
     3. Mess / Food Tracker
     4. Dashboard & Reports
     0. Exit
   ```
4. Pick a number and follow the on-screen prompts. Press **Enter** at any
   "press Enter to continue" step to move on.

That's it — no setup, no config files to edit. A `data/` folder is
created automatically the first time you save something.

---

##  Data Storage

All records are stored as plain, human-readable JSON files inside the
`data/` folder next to `main.py`:

| File | Contents |
|---|---|
| `expenses.json` | All logged expenses |
| `inventory.json` | All inventory items |
| `mess.json` | Daily meal taken/skipped records |
| `mess_settings.json` | Your meal rate and fixed monthly fee |

Because it's plain JSON, you can back it up, sync it across devices, or
inspect/edit it by hand if needed.

---

##  Example Workflows

**Logging an expense**
```
Expense Manager → 1. Add expense
Date [default 2026-09-21]:
Category: Food
Description: Canteen dinner
Amount: Rs. 120
```

**Tracking today's meals**
```
Mess / Food Tracker → 1. Mark today's meals
Breakfast taken? (y/n): y
Lunch taken? (y/n): n
Dinner taken? (y/n): y
```

**Checking your monthly snapshot**
```
Dashboard & Reports → 1. This month's snapshot
```
Shows total expenses by category, your mess bill and rebate, low-stock
inventory items, and your combined total spend for the month.

---

##  Extending the Project

Some ideas if you want to build on this:
- Add a `budget_manager.py` module for setting and tracking monthly budgets
- Export reports to CSV or PDF
- Add a roommate/split-expense feature
- Wrap the modules in a Flask or Tkinter frontend for a GUI/web version
- Add authentication if multiple users share the same install

Since every module reads/writes through simple class methods (not
directly through the CLI), it's straightforward to reuse them in a new
interface without touching the underlying logic.

---

##  License

Free to use, modify, and share for personal or educational purposes.
