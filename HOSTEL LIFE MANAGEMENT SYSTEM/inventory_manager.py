


import utils

DATA_FILE = "inventory.json"


class InventoryManager:
    def __init__(self):
        self.items = utils.load_json(DATA_FILE, [])

    def _save(self):
        utils.save_json(DATA_FILE, self.items)

    
    def add_item(self, name, category, quantity, location="Room", low_stock_at=1):
        record = {
            "id": utils.next_id(self.items),
            "name": name,
            "category": category,
            "quantity": int(quantity),
            "location": location,
            "low_stock_at": int(low_stock_at),
            "status": "In Room",
            "lent_to": None,
        }
        self.items.append(record)
        self._save()
        return record

    def find(self, item_id):
        return next((i for i in self.items if i["id"] == item_id), None)

    def update_quantity(self, item_id, delta):
        item = self.find(item_id)
        if not item:
            return None
        item["quantity"] = max(0, item["quantity"] + delta)
        self._save()
        return item

    def remove_item(self, item_id):
        before = len(self.items)
        self.items = [i for i in self.items if i["id"] != item_id]
        self._save()
        return len(self.items) < before

    def lend_item(self, item_id, person):
        item = self.find(item_id)
        if not item:
            return None
        item["status"] = "Lent Out"
        item["lent_to"] = person
        self._save()
        return item

    def return_item(self, item_id):
        item = self.find(item_id)
        if not item:
            return None
        item["status"] = "In Room"
        item["lent_to"] = None
        self._save()
        return item

    def list_items(self, category=None):
        results = self.items
        if category:
            results = [i for i in results if i["category"].lower() == category.lower()]
        return sorted(results, key=lambda i: i["name"].lower())

    def low_stock_items(self):
        return [i for i in self.items if i["quantity"] <= i["low_stock_at"]]

    
    def run_menu(self):
        while True:
            utils.clear_screen()
            print("=" * 50)
            print("  PERSONAL INVENTORY")
            print("=" * 50)
            print("  1. Add item")
            print("  2. View all items")
            print("  3. Filter by category")
            print("  4. Update quantity (use/restock)")
            print("  5. Lend an item")
            print("  6. Mark item returned")
            print("  7. Low-stock alerts")
            print("  8. Remove item")
            print("  0. Back to main menu")
            choice = utils.ask("\n  Choose an option: ")

            if choice == "1":
                self._menu_add()
            elif choice == "2":
                self._menu_list(self.list_items())
            elif choice == "3":
                category = utils.ask("\n  Category: ")
                self._menu_list(self.list_items(category=category))
            elif choice == "4":
                self._menu_update_qty()
            elif choice == "5":
                self._menu_lend()
            elif choice == "6":
                self._menu_return()
            elif choice == "7":
                self._menu_low_stock()
            elif choice == "8":
                self._menu_remove()
            elif choice == "0":
                return
            else:
                print("  Invalid option.")
                utils.pause()

    def _menu_add(self):
        name = utils.ask("\n  Item name: ")
        category = utils.ask("  Category (e.g. Toiletries, Electronics, Clothing, Books): ", "General")
        quantity = utils.ask_int("  Quantity: ", 1)
        location = utils.ask("  Location (e.g. Cupboard, Desk): ", "Room")
        low_stock_at = utils.ask_int("  Alert when quantity falls to: ", 1)
        record = self.add_item(name, category, quantity, location, low_stock_at)
        print(f"\n  Added item #{record['id']}: {record['name']} (qty {record['quantity']})")
        utils.pause()

    def _menu_list(self, records):
        print()
        utils.print_table(
            ["ID", "Name", "Category", "Qty", "Location", "Status", "Lent To"],
            [[i["id"], i["name"], i["category"], i["quantity"], i["location"],
              i["status"], i["lent_to"] or "-"] for i in records],
        )
        utils.pause()

    def _menu_update_qty(self):
        item_id = utils.ask_int("\n  Item ID: ")
        delta = utils.ask_int("  Change amount (positive to restock, negative to use up): ")
        item = self.update_quantity(item_id, delta)
        if item:
            print(f"  {item['name']} quantity is now {item['quantity']}.")
            if item["quantity"] <= item["low_stock_at"]:
                print("  ⚠ This item is now low on stock!")
        else:
            print("  No item found with that ID.")
        utils.pause()

    def _menu_lend(self):
        item_id = utils.ask_int("\n  Item ID: ")
        person = utils.ask("  Lend to (name): ")
        item = self.lend_item(item_id, person)
        print(f"  {item['name']} marked as lent to {person}." if item else "  No item found.")
        utils.pause()

    def _menu_return(self):
        item_id = utils.ask_int("\n  Item ID: ")
        item = self.return_item(item_id)
        print(f"  {item['name']} marked as returned." if item else "  No item found.")
        utils.pause()

    def _menu_low_stock(self):
        print()
        low = self.low_stock_items()
        utils.print_table(
            ["ID", "Name", "Qty", "Alert Level"],
            [[i["id"], i["name"], i["quantity"], i["low_stock_at"]] for i in low],
        )
        utils.pause()

    def _menu_remove(self):
        item_id = utils.ask_int("\n  Item ID to remove: ")
        print("  Removed." if self.remove_item(item_id) else "  No item found with that ID.")
        utils.pause()
