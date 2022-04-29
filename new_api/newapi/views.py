from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Ingredient, Recipe, Liked
from .serializers import LikedSerial, RecipeSerial, IngredientSerial, RecipeDetailSerial, UserRegSerial
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.

class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerial
    permissions_classes = [permissions.IsAuthenticated] #Allows only users that have been authenticated

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerial
    permissions_classes = [permissions.AllowAny] #Allows anybody to use the list

class IngredientCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerial

class CreateLikedView(generics.CreateAPIView):
    queryset = Liked.objects.all()
    serializer_class = LikedSerial

    def get_queryset(self):
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        return Liked.objects.filter(user=user, recipe=recipe)
    
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted on this recipe.')
        else:
            user = self.request.user
            recipe = Recipe.objects.get(pk=self.kwargs['pk'])
            serializer.save(user=user, recipe=recipe)

class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerial
    permissions_classes = [permissions.AllowAny] #Allows anybody to use the list

        
class RecipeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerial
    permissions_classes = [permissions.IsAuthenticated]

    def delete_recipe(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(author=self.request.user, pk=kwargs['pk'])
        if recipe.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Recipe does not exist bro.')

    def perform_update(self, serializer, *kwargs):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        if self.request.user != recipe.author:
            raise ValidationError('Sorry, you cannot update this!')
        else:
            serializer.save(user=self.request.user, recipe=recipe)

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegSerial
    permissions_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegSerial(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {'token':token}
        else:
            data = serializer.errors
        return Response(data=data, status=201)


#For the user to login...
class LoginView(generics.CreateAPIView):
    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().as_view()(request=request._request)