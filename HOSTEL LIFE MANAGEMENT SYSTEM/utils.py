"""
utils.py
Shared helper functions used by every module of the Hostel Life Manager:
JSON-based persistence, date helpers, and simple table printing (no
external dependencies required).
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DATE_FMT = "%Y-%m-%d"


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_json(filename, default):
    """Load a JSON file from the data directory, returning `default` if
    the file doesn't exist or is corrupted."""
    ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(filename, data):
    ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def today_str():
    return datetime.now().strftime(DATE_FMT)


def month_str(date_str=None):
    """Return the 'YYYY-MM' month for a given 'YYYY-MM-DD' date string,
    or for today if none is given."""
    d = datetime.strptime(date_str, DATE_FMT) if date_str else datetime.now()
    return d.strftime("%Y-%m")


def valid_date(date_str):
    try:
        datetime.strptime(date_str, DATE_FMT)
        return True
    except ValueError:
        return False


def next_id(records):
    """Return the next integer id for a list of dict records with an 'id' key."""
    if not records:
        return 1
    return max(r["id"] for r in records) + 1


def ask(prompt, default=None):
    """Input helper: returns `default` if the user just presses Enter."""
    raw = input(prompt).strip()
    return raw if raw else default


def ask_float(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a valid number.")


def ask_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a valid whole number.")


def ask_date(prompt, default=None):
    default = default or today_str()
    while True:
        raw = input(f"{prompt} [default {default}]: ").strip()
        if not raw:
            return default
        if valid_date(raw):
            return raw
        print("  Please use YYYY-MM-DD format.")


def print_table(headers, rows):
    """Print a plain-text aligned table without needing external libraries."""
    if not rows:
        print("  (no records found)")
        return
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    header_line = "  " + " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("  " + "-+-".join("-" * w for w in widths))
    for row in rows:
        print("  " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(row)))


def pause():
    input("\n  Press Enter to continue...")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
