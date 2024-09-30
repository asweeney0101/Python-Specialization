from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_ 

#   PyMySQL is used, as vanilla MySQL couldn't connect to MySQLdb, 
#   PyMySQL was a workaround for this problem found online

engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name} - {self.difficulty}>"

    def __str__(self):
        return (
            f"{'-'*10}\n"
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {self.ingredients}\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*10}\n"
        )

    def calculate_difficulty(self):
        ingredients_list = self.ingredients.split(', ')
        numberOfIngredients = len(ingredients_list)
        if self.cooking_time < 10:
            if numberOfIngredients < 4:
                self.difficulty ='Easy'
            else:
                self.difficulty = 'Medium'
        else:
            if numberOfIngredients < 4:
                self.difficulty = 'Intermediate'
            else:
                self.difficulty = 'Hard'

    def return_ingredients_as_list(self):
        if not self.ingredients:  
            return []
        else:
            return self.ingredients.split(', ')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def create_recipe():
    while True:
        name = input("Enter the recipe name (Max length 50 characters): ")
        if len(name) >= 50:
            print("Name too long! ") 
        else:
            break   

    while True:        
        cooking_time = input("Enter the cooking time of the recipe (in minutes): ")
        if not cooking_time.isnumeric():
            print("Cooking Time must be a number")
        else:
            break
        
    ingredients = list(input("Please list the required ingredients, separated by commas: ").split(', '))
    ingredients_str = ', '.join(ingredients)

    recipe_entry = Recipe(
        name=name, ingredients=ingredients_str, cooking_time=int(cooking_time)
    )
    recipe_entry.calculate_difficulty()
     
    try:
        session.add(recipe_entry)
        session.commit()
        print("Recipe added successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

def view_all_recipes():
    recipes_list = session.query(Recipe).all()

    if not recipes_list:
        print("No recipes found in the database.")
        return None

    for recipe in recipes_list:
        print(recipe)

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("No recipes found.")
        return

    results = session.query(Recipe.ingredients).all()

    all_ingredients = []
    for result in results:
        ingredients_list = result[0].split(', ')
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    print("Available ingredients:")
    for i, ingredient in enumerate(all_ingredients, start=1):
        print(f"{i}. {ingredient}")

    user_input = input("Enter the numbers corresponding to the ingredients you want to search by (e.g., 1 3 5): ").split()

    try:
        selected_numbers = [int(num) for num in user_input]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    if any(num < 1 or num > len(all_ingredients) for num in selected_numbers):
        print("One or more selected numbers are out of range.")
        return

    search_ingredients = [all_ingredients[num - 1] for num in selected_numbers] 

    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"  
        conditions.append(Recipe.ingredients.like(like_term))

    matching_recipes = session.query(Recipe).filter(or_(*conditions)).all()

    if matching_recipes:
        print(f"Recipes matching ingredients: {', '.join(search_ingredients)}")
        for recipe in matching_recipes:
            print(recipe)
    else:
        print(f"No recipes found with ingredients: {', '.join(search_ingredients)}")
