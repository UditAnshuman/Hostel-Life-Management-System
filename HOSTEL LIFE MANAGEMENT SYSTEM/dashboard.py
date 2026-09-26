

import utils


class Dashboard:
    def __init__(self, expense_manager, inventory_manager, mess_tracker):
        self.expenses = expense_manager
        self.inventory = inventory_manager
        self.mess = mess_tracker

    def snapshot(self, month=None):
        month = month or utils.month_str()
        expense_total = self.expenses.total(month=month)
        category_summary = self.expenses.category_summary(month=month)
        mess_summary = self.mess.month_summary(month)
        low_stock = self.inventory.low_stock_items()
        lent_out = [i for i in self.inventory.items if i["status"] == "Lent Out"]

        total_spend = round(expense_total + mess_summary["estimated_bill"], 2)

        return {
            "month": month,
            "expense_total": expense_total,
            "category_summary": category_summary,
            "mess_summary": mess_summary,
            "total_spend_incl_mess": total_spend,
            "low_stock_count": len(low_stock),
            "low_stock_items": low_stock,
            "lent_out_count": len(lent_out),
            "lent_out_items": lent_out,
            "inventory_item_count": len(self.inventory.items),
        }

    
    def run_menu(self):
        while True:
            utils.clear_screen()
            print("=" * 50)
            print("  DASHBOARD & REPORTS")
            print("=" * 50)
            print("  1. This month's snapshot")
            print("  2. Snapshot for another month")
            print("  3. Full expense trend (all months)")
            print("  0. Back to main menu")
            choice = utils.ask("\n  Choose an option: ")

            if choice == "1":
                self._show_snapshot(utils.month_str())
            elif choice == "2":
                month = utils.ask("\n  Month (YYYY-MM): ")
                self._show_snapshot(month)
            elif choice == "3":
                self._show_trend()
            elif choice == "0":
                return
            else:
                print("  Invalid option.")
                utils.pause()

    def _show_snapshot(self, month):
        data = self.snapshot(month)
        utils.clear_screen()
        print("=" * 50)
        print(f"  SNAPSHOT — {data['month']}")
        print("=" * 50)

        print("\n  EXPENSES")
        print(f"    General expenses total: Rs.{data['expense_total']:.2f}")
        if data["category_summary"]:
            utils.print_table(
                ["Category", "Amount"],
                [[cat, f"Rs.{amt:.2f}"] for cat, amt in data["category_summary"].items()],
            )

        print("\n  MESS / FOOD")
        m = data["mess_summary"]
        print(f"    Meals taken: {m['meals_taken']}  |  Meals skipped: {m['meals_skipped']}")
        print(f"    Estimated mess bill: Rs.{m['estimated_bill']:.2f}"
              f"  (rebate for skipped meals: Rs.{m['estimated_rebate']:.2f})")

        print("\n  INVENTORY")
        print(f"    Total items tracked: {data['inventory_item_count']}")
        print(f"    Items lent out: {data['lent_out_count']}")
        print(f"    Low-stock items: {data['low_stock_count']}")
        if data["low_stock_items"]:
            utils.print_table(
                ["Item", "Qty", "Alert Level"],
                [[i["name"], i["quantity"], i["low_stock_at"]] for i in data["low_stock_items"]],
            )

        print("\n  TOTAL SPEND THIS PERIOD (expenses + mess): "
              f"Rs.{data['total_spend_incl_mess']:.2f}")
        utils.pause()

    def _show_trend(self):
        summary = self.expenses.monthly_summary()
        print("\n  Monthly expense trend (excludes mess bill):")
        utils.print_table(
            ["Month", "Total Spent"],
            [[month, f"Rs.{amt:.2f}"] for month, amt in summary.items()],
        )
        utils.pause()
