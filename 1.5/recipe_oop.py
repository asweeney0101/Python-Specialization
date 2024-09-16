class Recipe:

    all_ingredients = set()

    def __init__(self, name, cooking_time, ingredients):
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = list(ingredients)
        self.difficulty = None
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getCookingTime(self):
        return self.name
    
    def setCookingTime(self, cooking_time):
        self.cooking_time = cooking_time

    def getIngredients(self):
        return self.ingredients
    
    def calculate_difficulty(self):
        numberOfIngredients = len(self.ingredients)
        if self.cooking_time < 10:
            if numberOfIngredients < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if numberOfIngredients < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"

    def add_ingredients(self, *ingredientsLocal):
        for i in ingredientsLocal:
            self.ingredients.append(i)
        self.update_all_ingredients()
    
    def update_all_ingredients(self):
        for i in self.ingredients:
            Recipe.all_ingredients.add(i)

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients         

    
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty
    
    def __str__(self):
        return f"Recipe: {self.name}\nCooking Time: {self.cooking_time} mins\nIngredients: {', '.join(self.ingredients)}\nDifficulty: {self.difficulty}\n"

def recipe_search(data, search_term):
    print("Recipies that contain " + search_term)
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


tea = Recipe("Tea", 5, ["Tea Leaves", "Sugar", "Water"])
coffee = Recipe("Coffee", 5, ["Coffee Powder", "Sugar", "Water"])
cake = Recipe("Cake", 50, ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"])
smoothie = Recipe("Banana Smoothie", 5, ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"])

recipes_list = [tea, coffee, cake, smoothie]


for recipe in recipes_list:
    print(recipe)

for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)