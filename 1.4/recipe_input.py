import pickle


def take_recipe():
    name = str(input("What would you like to call this recipe? "))
    cooking_time = int(input("Total Cook + Prep time: "))
    ingredients = list(input("Please list the required ingredients, separated by commas: ").split(", "))
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

    return recipe

fileName = str(input("Which file would you like to store this to? "))

try:
    file = open('fileName', 'rb')
    data = pickle.load(file)
    print('File Found')
except FileNotFoundError:
     print("File not found, no worries, we'll create it for you! ")
     data = {"recipes_list": [], "all_ingredients": []}
except:
     data = {"recipes_list": [], "all_ingredients": []}
else:   
    data = {"recipes_list": [], "all_ingredients": []}
finally:
     recipes_list = data["recipes_list"]
     all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to enter: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

with open(fileName, 'wb') as updated_file:
    pickle.dump(data, updated_file)

