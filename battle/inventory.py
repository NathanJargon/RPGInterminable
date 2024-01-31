class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, effects, quantity=1):
        if item_name in self.items:
            _, current_quantity = self.items[item_name]
            self.items[item_name] = (effects, current_quantity + quantity)
        else:
            self.items[item_name] = (effects, quantity)

    def add_debug_items(self):
        self.add_item("HP Potion", (20, 0, "Restores 20 HP"), 1)
        self.add_item("Stamina Potion", (0, 20, "Restores 20 MP"), 1)
        self.add_item("Mixed Potion", (10, 10, "Restores 10 HP and 10 MP"), 1)
        self.add_item("Revival Potion", (30, 30, "Restores 30 HP and 30 MP"), 1)


    def remove_item(self, item_name, quantity=1):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            # if self.items[item_name] == 0:
            #     del self.items[item_name]

    def check_item(self, item_name):
        return self.items.get(item_name, 0)


    def update_item(self, item_name, new_count):
        if item_name in self.items:
            effects, _ = self.items[item_name]
            self.items[item_name] = (effects, new_count)
            
    def get_items_with_quantities(self):
        return [f"{item_name}: {quantity}" for item_name, quantity in self.items.items()]