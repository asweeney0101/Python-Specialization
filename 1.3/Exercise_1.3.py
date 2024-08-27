recipes_list = []
ingredients_list = []

def take_recipe():
    name = str(input("What would you like to call this recipe? "))
    cooking_time = int(input("Total Cook + Prep time: "))
    ingredients = list(input("Please list the required ingredients, separated by commas: ").split(", "))
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe

n = int(input("How many recipes would you like to enter: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"
print(" ")
print("All Recipes: ")
print("__________________________")
print(" ")

for recipe in recipes_list:
    print("Recipe: " + recipe["name"])
    print("Cook Time: ", recipe["cooking_time"])
    print("Ingredients: ")
    print("____________")
    for ingredient in recipe["ingredients"]:
        print(ingredient, sep='\n')
    print("Difficulty: " + recipe["difficulty"])
    print("")


print(" ")
print("All Ingredients: ")
print("__________________________")
print(" ")
ingredients_list.sort()
for ingredient in ingredients_list:
    print(ingredient, sep='\n')
