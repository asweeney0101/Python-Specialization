import pickle

def display_recipe(recipe):
    print("Recipe: " + recipe["name"])
    print("Total Time: " + str(recipe["cooking_time"]))
    for i in recipe["ingredients"]: 
        print(i)
    print("Difficulty: " + recipe["difficulty"])

def search_ingredient(data):
    ingredients = enumerate(data["all_ingredients"])
    all_ingredients = list(ingredients)

    print("All Ingredients:")
    print("----------------")
    for i in all_ingredients:
        print(i)

    try:
        n = int(input("Enter the number of an ingredient to search: "))
        ingredient_searched = all_ingredients[n][1]

    except ValueError:
        print("Error, please enter a number: ")

    else:
        for recipe in data["recipes_list"]:
            
            if ingredient_searched in recipe["ingredients"]:
                print("-----------------")
                display_recipe(recipe)
        

fileName = input("Name of file where data is stored: ")

try:
    with open(fileName, "rb") as file:
        data = pickle.load(file)

except FileNotFoundError:
    print("Couldn't find a file with that name, please try again. ")

else:
     search_ingredient(data)