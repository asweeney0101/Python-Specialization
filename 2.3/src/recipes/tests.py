from django.test import TestCase
from recipes.models import Recipe

class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            cooking_time=15,
            ingredients="ingredient1, ingredient2, ingredient3",
            description="This is a test recipe"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Test Recipe")
        self.assertEqual(self.recipe.cooking_time, 15)
        self.assertEqual(self.recipe.ingredients, "ingredient1, ingredient2, ingredient3")
        self.assertEqual(self.recipe.description, "This is a test recipe")

    def test_calculate_difficulty_easy(self):
        self.recipe.cooking_time = 5
        self.recipe.ingredients = "ingredient1, ingredient2"
        self.recipe.calculate_difficulty()
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.difficulty, "Easy")

    def test_calculate_difficulty_medium(self):
        self.recipe.cooking_time = 5
        self.recipe.ingredients = "ingredient1, ingredient2, ingredient3, ingredient4"
        self.recipe.calculate_difficulty()
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.difficulty, "Medium")

    def test_calculate_difficulty_intermediate(self):
        self.recipe.cooking_time = 15
        self.recipe.ingredients = "ingredient1, ingredient2"
        self.recipe.calculate_difficulty()
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.difficulty, "Intermediate")

    def test_calculate_difficulty_hard(self):
        self.recipe.cooking_time = 15
        self.recipe.ingredients = "ingredient1, ingredient2, ingredient3, ingredient4"
        self.recipe.calculate_difficulty()
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.difficulty, "Hard")

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Test Recipe")