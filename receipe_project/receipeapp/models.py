from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prep_time = models.PositiveIntegerField()  # In minutes
    difficulty = models.PositiveIntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')])
    vegetarian = models.BooleanField()
    image=models.ImageField(upload_to='media_file')

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.recipe)

