from django.urls import path
# from .views import chat_home
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('chat_session', views.chat_session, name='chat_session'),
    path('home', views.chat_home, name='index'),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
    
     path('chat/<str:current_session>/', views.chat_home, name='chat_home_with_session'),
]
