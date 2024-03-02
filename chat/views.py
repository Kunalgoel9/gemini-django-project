# import openai
from rest_framework.views import APIView
from rest_framework.response import Response
# from .models import ChatSession
import uuid
from django.shortcuts import render,redirect
from .models import ChatSession, Message
from . forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required


# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

import google.generativeai as genai
import os

gemini_api_key = ""#<<- put ur gemini key here
genai.configure(api_key = gemini_api_key)








from django.template import loader
from django.http import HttpResponse  

# def chat_home(request):
#     # Logic for the view
#     template = loader.get_template('chat/home.html')
#     return HttpResponse(template.render()) # Adjust the template as necessary

def chat_session(request):
    # Logic for handling chat sessions
    template = loader.get_template('chat/session.html')
    return HttpResponse(template.render())

#c24b16ec0ae791f3752c37b665c73858-us18

def chat_home(request):
   session_key = request.session.session_key
   print(request.user,request.user.id)
   if not session_key:
       request.session.create()
       session_key = request.session.session_key

   messages = Message.objects.filter(user=request.user.id)   

   if request.method == 'POST':
        session, created = ChatSession.objects.get_or_create(id=request.session.session_key, user=request.user.id)
        messages = Message.objects.filter(session=session)
        request.session.save()    
       
        user_input = request.POST.get('user_input')
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        print(response.text)
        Message.objects.create(session=session,text=user_input, response=response.text,user=request.user.id)
        messages = Message.objects.filter(session=session,user=request.user.id)
        return render(request, 'chat/home.html', {'messages': messages})

   return render(request, 'chat/home.html', {'messages': messages})

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("my-login")


    context = {'registerform':form}

    return render(request, 'crm/register.html', context=context)



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("my-login")



@login_required(login_url="my-login")
def dashboard(request):

    return render(request, 'crm/dashboard.html')
    
 
