

from collections import defaultdict
import utils

DATA_FILE = "expenses.json"

CATEGORIES = [
    "Food", "Travel", "Stationery", "Laundry", "Mobile/Internet",
    "Entertainment", "Groceries", "Medical", "Other",
]


class ExpenseManager:
    def __init__(self):
        self.expenses = utils.load_json(DATA_FILE, [])


    def _save(self):
        utils.save_json(DATA_FILE, self.expenses)

    
    def add_expense(self, date, category, description, amount):
        record = {
            "id": utils.next_id(self.expenses),
            "date": date,
            "category": category,
            "description": description,
            "amount": round(float(amount), 2),
        }
        self.expenses.append(record)
        self._save()
        return record

    def delete_expense(self, expense_id):
        before = len(self.expenses)
        self.expenses = [e for e in self.expenses if e["id"] != expense_id]
        self._save()
        return len(self.expenses) < before

    def list_expenses(self, month=None, category=None):
        results = self.expenses
        if month:
            results = [e for e in results if utils.month_str(e["date"]) == month]
        if category:
            results = [e for e in results if e["category"].lower() == category.lower()]
        return sorted(results, key=lambda e: e["date"])

    def total(self, month=None, category=None):
        return round(sum(e["amount"] for e in self.list_expenses(month, category)), 2)

    def category_summary(self, month=None):
        totals = defaultdict(float)
        for e in self.list_expenses(month=month):
            totals[e["category"]] += e["amount"]
        return dict(sorted(totals.items(), key=lambda kv: -kv[1]))

    def monthly_summary(self):
        totals = defaultdict(float)
        for e in self.expenses:
            totals[utils.month_str(e["date"])] += e["amount"]
        return dict(sorted(totals.items()))

    
    def run_menu(self):
        while True:
            utils.clear_screen()
            print("=" * 50)
            print("  EXPENSE MANAGER")
            print("=" * 50)
            print("  1. Add expense")
            print("  2. View all expenses")
            print("  3. View this month's expenses")
            print("  4. Filter by category")
            print("  5. Category-wise summary (this month)")
            print("  6. Delete an expense")
            print("  0. Back to main menu")
            choice = utils.ask("\n  Choose an option: ")

            if choice == "1":
                self._menu_add()
            elif choice == "2":
                self._menu_list(self.list_expenses())
            elif choice == "3":
                self._menu_list(self.list_expenses(month=utils.month_str()))
            elif choice == "4":
                self._menu_filter_category()
            elif choice == "5":
                self._menu_category_summary()
            elif choice == "6":
                self._menu_delete()
            elif choice == "0":
                return
            else:
                print("  Invalid option.")
                utils.pause()

    def _menu_add(self):
        print("\n  Categories:", ", ".join(CATEGORIES))
        date = utils.ask_date("  Date")
        category = utils.ask("  Category: ", "Other")
        description = utils.ask("  Description: ", "")
        amount = utils.ask_float("  Amount: Rs. ")
        record = self.add_expense(date, category, description, amount)
        print(f"\n  Added expense #{record['id']}: Rs.{record['amount']} on {record['date']}")
        utils.pause()

    def _menu_list(self, records):
        print()
        utils.print_table(
            ["ID", "Date", "Category", "Description", "Amount"],
            [[e["id"], e["date"], e["category"], e["description"], f"Rs.{e['amount']:.2f}"] for e in records],
        )
        print(f"\n  Total: Rs.{round(sum(e['amount'] for e in records), 2):.2f}")
        utils.pause()

    def _menu_filter_category(self):
        category = utils.ask("\n  Category to filter by: ")
        self._menu_list(self.list_expenses(category=category))

    def _menu_category_summary(self):
        summary = self.category_summary(month=utils.month_str())
        print(f"\n  Category summary for {utils.month_str()}:")
        utils.print_table(
            ["Category", "Total"],
            [[cat, f"Rs.{amt:.2f}"] for cat, amt in summary.items()],
        )
        utils.pause()

    def _menu_delete(self):
        expense_id = utils.ask_int("\n  Enter expense ID to delete: ")
        if self.delete_expense(expense_id):
            print("  Deleted.")
        else:
            print("  No expense found with that ID.")
        utils.pause()
