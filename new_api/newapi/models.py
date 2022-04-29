from multiprocessing.spawn import import_main_path
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
class Recipe(models.Model):
    DIET_CHOICES = [
        ('balanced', 'balanced'),
        ('high-protein', 'high-protein'),
        ('high-fibre', 'balanced'),
        ('low-fat', 'low-fat'),
        ('low-carb', 'low-carb'),
        ('low-sodium', 'low-sodium')
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    time_mins = models.PositiveBigIntegerField()
    ingredients = models.ManyToManyField('Ingredient')
    diet = models.CharField(max_length=12, choices=DIET_CHOICES, default='balanced')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title 
    
    objects = models.Manager()


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    calories = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    objects = models.Manager()

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    objects = models.Manager()


@receiver(post_save, sender=User)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
