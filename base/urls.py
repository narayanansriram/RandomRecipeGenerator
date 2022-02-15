from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/',views.registerUser,name='register'),
    path('', views.home, name="home"),
    path('room_page/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('like-recipe/<slug:recipe>',views.likeRecipe,name="like-recipe"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('contact-us/', views.contactUs, name="contact-us"),
    path('help-page/', views.helpPage, name="help-page")
]