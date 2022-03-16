from django.urls import path
from . import views

#URLs for the application are located here
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/',views.registerUser,name='register'),
    path('', views.home, name="home"),
    path('recipe_page/<str:pk>/', views.recipe, name="recipe"),
    path('profile/<str:pk>/', views.recipeGenerator, name="recipe-generator"),
    path('like-recipe/<slug:recipe>',views.likeRecipe,name="like-recipe"),
    path('create-recipe/', views.createRecipe, name="create-recipe"),
    path('update-recipe/<str:pk>/', views.updateRecipe, name="update-recipe"),
    path('delete-recipe/<str:pk>/', views.deleteRecipe, name="delete-recipe"),
    path('contact-us/', views.contactUs, name="contact-us"),
    path('help-page/', views.helpPage, name="help-page")
]