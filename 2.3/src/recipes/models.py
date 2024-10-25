from django.db import models

# Create your models here.


class Recipe (models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.FloatField(help_text='In minutes')
    ingredients = models.CharField(help_text='Please list each ingredient separated by commas', max_length=350)
    description = models.TextField()
    difficulty = None

    def calculate_difficulty(self):
        numberOfIngredients = len(self.ingredients.split(","))
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
        self.save()


    def __str__(self):
        return str(self.name)
    