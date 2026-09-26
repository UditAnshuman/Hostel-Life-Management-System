

import utils
from expense_manager import ExpenseManager
from inventory_manager import InventoryManager
from mess_tracker import MessTracker
from dashboard import Dashboard


def main_menu():
    expense_manager = ExpenseManager()
    inventory_manager = InventoryManager()
    mess_tracker = MessTracker()
    dashboard = Dashboard(expense_manager, inventory_manager, mess_tracker)

    while True:
        utils.clear_screen()
        print("=" * 50)
        print("        🏠  HOSTEL LIFE MANAGER")
        print("=" * 50)
        print("  1. Expense Manager")
        print("  2. Personal Inventory")
        print("  3. Mess / Food Tracker")
        print("  4. Dashboard & Reports")
        print("  0. Exit")
        choice = utils.ask("\n  Choose an option: ")

        if choice == "1":
            expense_manager.run_menu()
        elif choice == "2":
            inventory_manager.run_menu()
        elif choice == "3":
            mess_tracker.run_menu()
        elif choice == "4":
            dashboard.run_menu()
        elif choice == "0":
            print("\n  Goodbye! Your data has been saved.")
            break
        else:
            print("  Invalid option.")
            utils.pause()


if __name__ == "__main__":
    main_menu()
