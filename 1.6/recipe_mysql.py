import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

if conn.is_connected():
    print("Connection successful!")
else:
    print("Connection failed!")

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
               id               INT AUTO_INCREMENT PRIMARY KEY,
               name             VARCHAR(50),
               ingredients      VARCHAR(255),
               cooking_time     INT,
               difficulty       VARCHAR(20)    
);''')

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

def create_recipe(conn, cursor):
    name = str(input("What would you like to call this recipe? "))
    cooking_time = int(input("Total Cook + Prep time: "))
    ingredients = list(input("Please list the required ingredients, separated by commas: ").split(", "))
    
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
            id, name, cooking_time, ingredients, difficulty = recipe
            print(f"\n- Name: {name}")
            print(f"  Cooking Time: {cooking_time} mins")
            print(f"  Ingredients: {ingredients}")
            print(f"  Difficulty: {difficulty}")
    else:
        print(f"\nNo recipes found with the ingredient '{searched_ingredient}'")


def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    if results:
        print("\nAvailable recipes:")
        for recipe in results:
            print(f"{recipe[0]}. {recipe[1]}") #ID & name
        
        recipe_id = int(input("\nEnter the ID of the recipe you want to update: "))

        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        
        if recipe:
            print("\nColumns you can update:")
            print("1. Name")
            print("2. Cooking Time")
            print("3. Ingredients")
            
            column_choice = input("Enter the number corresponding to the column you want to update (1-3): ")

            if column_choice == '1':
                new_name = input("Enter the new recipe name: ")
                query = "UPDATE Recipes SET name = %s WHERE id = %s"
                cursor.execute(query, (new_name, recipe_id))
                print(f"Recipe name updated to '{new_name}'!")
            
            elif column_choice == '2':
                new_cooking_time = int(input("Enter the new cooking time (in minutes): "))
                ingredients = recipe[2].split(", ") #Fetch the existing ingredients
                difficulty = calculate_difficulty(new_cooking_time, ingredients)

                query = "UPDATE Recipes SET cooking_time = %s, difficulty = %s WHERE id = %s"
                cursor.execute(query, (new_cooking_time, difficulty, recipe_id))
                print(f"Cooking time updated to {new_cooking_time} minutes and difficulty recalculated to '{difficulty}'!")
            
            elif column_choice == '3':
                new_ingredients = list(input("Enter the new ingredients, separated by commas: ").split(", "))
                new_ingredients_string = ', '.join(ingredient.strip() for ingredient in new_ingredients)
                cooking_time = recipe[1]  # Fetch the existing cooking time
                difficulty = calculate_difficulty(cooking_time, new_ingredients)

                query = "UPDATE Recipes SET ingredients = %s, difficulty = %s WHERE id = %s"
                cursor.execute(query, (new_ingredients_string, difficulty, recipe_id))
                print(f"Ingredients updated to '{new_ingredients_string}' and difficulty recalculated to '{difficulty}'!")
            
            else:
                print("Invalid choice! No update made.")
            
            conn.commit()

        else:
            print(f"No recipe found with ID {recipe_id}.")
    else:
        print("No recipes available to update.")



def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    if results:
        print("\nAvailable recipes:")
        for recipe in results:
            print(f"{recipe[0]}. {recipe[1]}") #ID & Name
        
        recipe_id = int(input("\nEnter the ID of the recipe you want to delete: "))

        cursor.execute("SELECT * FROM Recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()

        if recipe:
            confirmation = input(f"Are you sure you want to delete the recipe '{recipe[1]}'? (yes/no): ").lower()
            if confirmation == 'yes':
                query = "DELETE FROM Recipes WHERE id = %s"
                cursor.execute(query, (recipe_id,))
                conn.commit()
                print(f"Recipe '{recipe[1]}' has been deleted.")
            else:
                print("Deletion canceled.")
        else:
            print(f"No recipe found with ID {recipe_id}.")
    else:
        print("No recipes available to delete.")



def main_menu(conn, cursor):
    choice = None
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

if __name__ == "__main__":
    main_menu(conn, cursor)
