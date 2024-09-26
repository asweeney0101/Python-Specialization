import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
               id               INT PRIMARY KEY,
               name             VARCHAR(50)
               ingredients      VARCHAR(255)
               cooking_time     INT,
               difficulty       VARCHAR(20)    
);''')


def create_recipe(conn, cursor):
    name = str(input("What would you like to call this recipe? "))
    cooking_time = int(input("Total Cook + Prep time: "))
    ingredients = list(input("Please list the required ingredients, separated by commas: ").split(", "))
    
    def calculate_difficulty(cooking_time, ingredients):
        numberOfIngredients = len(ingredients)
        if cooking_time < 10:
            if numberOfIngredients < 4:
                return "Easy"
            else:
                return "Medium"
        else:
            if numberOfIngredients < 4:
                return "Intermediate"
            else:
                return "Hard" 

    difficulty = calculate_difficulty(cooking_time, ingredients)        
    returned_string = ', '.join(ingredient.strip() for ingredient in ingredients)

    query = """
    INSERT INTO recipes (name, cooking_time, ingredients, difficulty)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (name, cooking_time, returned_string, difficulty))
    conn.commit()

    print(f"Recipe '{name}' has been added to the database!")


def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    for result in results:
       ingredients = result[0].split(', ') 
       all_ingredients.extend(ingredients) 

    unique_ingredients = list(set(all_ingredients))

    print("\nAvailable ingredients:")
    for idx, ingredient in enumerate(sorted(unique_ingredients), start=1):
        print(f"{idx}. {ingredient}")

    choice = int(input("Choose an ingredient by number to search: ")) - 1
    searched_ingredient = sorted(unique_ingredients)[choice]
    
    query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(query, ('%' + searched_ingredient + '%',))
    matching_recipes = cursor.fetchall()

    if matching_recipes:
        print(f"\nRecipes containing '{searched_ingredient}':")
        for recipe in matching_recipes:
            # Each recipe is a tuple with (name, cooking_time, ingredients, difficulty)
            name, cooking_time, ingredients, difficulty = recipe
            print(f"\n- Name: {name}")
            print(f"  Cooking Time: {cooking_time} mins")
            print(f"  Ingredients: {ingredients}")
            print(f"  Difficulty: {difficulty}")
    else:
        print(f"\nNo recipes found with the ingredient '{searched_ingredient}'")


def update_recipe(conn, cursor):
    return 1

def delete_recipe(conn, cursor):
    return 1


def main_menu(conn, cursor):
    while (choice != '5'):
        print("\nMain Menu:")
        print("1. Create a new recipe")
        print("2. Search existing recipes")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Exiting...")
            conn.commit()
            cursor.close()
            conn.close()
            break
        else:
            print("Invalid choice, please try again.")



