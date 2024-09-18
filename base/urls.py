from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.registeruser, name="register"),
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('createRoom/', views.createRoom, name="createRoom"),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete_messages/<str:pk>/', views.deleteMessages, name='delete_message'),
    path('updateuser/', views.updateUser, name='update-user'),
    path('topics/', views.topic, name='topic'),
    path('activity/', views.activity, name='activity'),
]