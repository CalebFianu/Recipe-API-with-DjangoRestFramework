"""new_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from newapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/newapi/', views.RecipeListView.as_view()),
    path('api/newapi/create', views.RecipeCreateView.as_view()),
    path('api/ingredients', views.IngredientCreateView.as_view()),
    path('api/newapi/<int:pk>/upvote/', views.CreateLikedView.as_view()),
    path('api/newapi/<int:pk>/', views.RecipeDetailView.as_view()),
    path('api/newapi/<int:pk>/update/', views.RecipeUpdateView.as_view()),
    path('api/register/', views.UserView.as_view()),
    path('api/login/', views.LoginView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
