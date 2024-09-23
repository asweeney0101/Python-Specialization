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
    return 1

def search_recipe(conn, cursor):
    return 1

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