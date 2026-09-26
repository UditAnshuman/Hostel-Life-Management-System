"""
mess_tracker.py
Module 3: Mess / Food Tracker

Tracks which mess meals (breakfast/lunch/dinner) were taken vs. skipped
each day, calculates a monthly mess bill using a per-meal rate, and
estimates the rebate for skipped meals.
"""

from collections import defaultdict
import utils

DATA_FILE = "mess.json"
SETTINGS_FILE = "mess_settings.json"

MEALS = ["Breakfast", "Lunch", "Dinner"]
DEFAULT_SETTINGS = {"meal_rate": 40.0, "monthly_fixed_fee": 0.0}


class MessTracker:
    def __init__(self):
        self.entries = utils.load_json(DATA_FILE, [])   # list of {date, meal, taken}
        self.settings = utils.load_json(SETTINGS_FILE, dict(DEFAULT_SETTINGS))

    def _save(self):
        utils.save_json(DATA_FILE, self.entries)

    def _save_settings(self):
        utils.save_json(SETTINGS_FILE, self.settings)

    # ---------- core operations ----------
    def mark_meal(self, date, meal, taken):
        meal = meal.title()
        existing = next((e for e in self.entries if e["date"] == date and e["meal"] == meal), None)
        if existing:
            existing["taken"] = taken
        else:
            self.entries.append({"date": date, "meal": meal, "taken": taken})
        self._save()

    def day_status(self, date):
        return {e["meal"]: e["taken"] for e in self.entries if e["date"] == date}

    def month_entries(self, month):
        return [e for e in self.entries if utils.month_str(e["date"]) == month]

    def month_summary(self, month):
        entries = self.month_entries(month)
        taken = sum(1 for e in entries if e["taken"])
        skipped = sum(1 for e in entries if not e["taken"])
        rate = self.settings["meal_rate"]
        fixed_fee = self.settings["monthly_fixed_fee"]
        rebate = round(skipped * rate, 2)
        bill = round(fixed_fee + taken * rate, 2)
        return {
            "month": month,
            "meals_taken": taken,
            "meals_skipped": skipped,
            "meal_rate": rate,
            "estimated_bill": bill,
            "estimated_rebate": rebate,
        }

    def set_meal_rate(self, rate):
        self.settings["meal_rate"] = round(float(rate), 2)
        self._save_settings()

    def set_fixed_fee(self, fee):
        self.settings["monthly_fixed_fee"] = round(float(fee), 2)
        self._save_settings()

    # ---------- CLI ----------
    def run_menu(self):
        while True:
            utils.clear_screen()
            print("=" * 50)
            print("  MESS / FOOD TRACKER")
            print("=" * 50)
            print(f"  Current meal rate: Rs.{self.settings['meal_rate']:.2f} | "
                  f"Fixed monthly fee: Rs.{self.settings['monthly_fixed_fee']:.2f}")
            print("  1. Mark today's meals")
            print("  2. Mark meals for a specific date")
            print("  3. View a day's status")
            print("  4. View this month's meal log")
            print("  5. Monthly mess bill summary")
            print("  6. Update meal rate / fixed fee")
            print("  0. Back to main menu")
            choice = utils.ask("\n  Choose an option: ")

            if choice == "1":
                self._menu_mark(utils.today_str())
            elif choice == "2":
                date = utils.ask_date("\n  Date")
                self._menu_mark(date)
            elif choice == "3":
                date = utils.ask_date("\n  Date")
                self._menu_day_status(date)
            elif choice == "4":
                self._menu_month_log(utils.month_str())
            elif choice == "5":
                self._menu_bill_summary()
            elif choice == "6":
                self._menu_settings()
            elif choice == "0":
                return
            else:
                print("  Invalid option.")
                utils.pause()

    def _menu_mark(self, date):
        print(f"\n  Marking meals for {date}. Enter y/n for each meal.")
        for meal in MEALS:
            ans = utils.ask(f"  {meal} taken? (y/n): ", "y").lower()
            self.mark_meal(date, meal, ans.startswith("y"))
        print("  Saved.")
        utils.pause()

    def _menu_day_status(self, date):
        status = self.day_status(date)
        print(f"\n  Status for {date}:")
        utils.print_table(
            ["Meal", "Taken?"],
            [[meal, "Yes" if status.get(meal) else "No"] for meal in MEALS],
        )
        utils.pause()

    def _menu_month_log(self, month):
        entries = sorted(self.month_entries(month), key=lambda e: (e["date"], e["meal"]))
        print(f"\n  Meal log for {month}:")
        utils.print_table(
            ["Date", "Meal", "Taken?"],
            [[e["date"], e["meal"], "Yes" if e["taken"] else "No"] for e in entries],
        )
        utils.pause()

    def _menu_bill_summary(self):
        month = utils.ask("\n  Month (YYYY-MM), blank for current: ", utils.month_str())
        summary = self.month_summary(month)
        print(f"\n  Mess bill summary for {summary['month']}:")
        print(f"    Meals taken:      {summary['meals_taken']}")
        print(f"    Meals skipped:    {summary['meals_skipped']}")
        print(f"    Meal rate:        Rs.{summary['meal_rate']:.2f}")
        print(f"    Estimated bill:   Rs.{summary['estimated_bill']:.2f}")
        print(f"    Estimated rebate: Rs.{summary['estimated_rebate']:.2f}")
        utils.pause()

    def _menu_settings(self):
        rate = utils.ask_float(f"\n  New meal rate [current Rs.{self.settings['meal_rate']:.2f}]: ",
                                self.settings["meal_rate"])
        fee = utils.ask_float(f"  New fixed monthly fee [current Rs.{self.settings['monthly_fixed_fee']:.2f}]: ",
                               self.settings["monthly_fixed_fee"])
        self.set_meal_rate(rate)
        self.set_fixed_fee(fee)
        print("  Settings updated.")
        utils.pause()
