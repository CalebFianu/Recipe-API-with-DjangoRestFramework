from asyncore import read
from rest_framework import serializers
from .models import Recipe, Ingredient, Liked
from django.db.models import Sum
from django.contrib.auth.models import User

class RecipeSerial(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    total_calories = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_total_calories(self, recipe):
        return Ingredient.objects.filter(recipe=recipe).aggregate(Sum('calories'))

    def get_likes(self, recipe):
        return Liked.objects.filter(recipe=recipe).count()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'title', 'image', 'time_mins', 'ingredients', 'diet', 'created', 'updated', 'total_calories', 'likes')
        read_only_fields = ('id', 'author')

class IngredientSerial(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'calories')
        read_only_fields = ('id',)

class LikedSerial(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = ('id',)
        read_only_fields = ('id',)

class RecipeDetailSerial(RecipeSerial):
    ingredients = IngredientSerial(many=True, read_only=True)


class UserRegSerial(serializers.ModelSerializer):
    password = serializers.CharField(style={'input type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
