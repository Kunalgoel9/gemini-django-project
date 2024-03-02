from django.urls import path
# from .views import chat_home
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('home', views.chat_home, name='index'),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
]