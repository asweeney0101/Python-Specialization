class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if not item in self.shopping_list:
            self.shopping_list.append(item)
        else:
            print("item already on list")

    def remove_item(self, item):
        try:
            self.shopping_list.remove(item)
        except:
            print("Item not found.")

    def view_list(self):
        print(self.list_name + ":")
        print("------------")
        for item in self.shopping_list:
            print('-' + str(item))
        

