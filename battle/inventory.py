class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity=1):
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name, quantity=1):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]

    def check_item(self, item_name):
        return self.items.get(item_name, 0)

    def add_debug_items(self):
        self.add_item("HP Potion", 5)
        self.add_item("MP Potion", 5)
        self.add_item("Mixed Potion", 5)
        self.add_item("Revival Potion", 5)

    def update_item(self, item_name, new_count):
        if item_name in self.items:
            self.items[item_name] = new_count
            
    def get_items_with_quantities(self):
        return [f"{item_name}: {quantity}" for item_name, quantity in self.items.items()]