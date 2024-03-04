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

gemini_api_key = "AIzaSyBdiXgnE8p0SL5VdhNC0cHsdOcO1-FB_jM"#<<- put ur gemini key here
genai.configure(api_key = gemini_api_key)








from django.template import loader
from django.http import HttpResponse  

# def chat_home(request):
#     # Logic for the view
#     template = loader.get_template('chat/home.html')
#     return HttpResponse(template.render()) # Adjust the template as necessary

def chat_session(request):
    session_id = request.GET.get('session_id', None)
    if session_id:
        # Now you can use session_id to filter your models or any other logic
        session,created=ChatSession.objects.get_or_create(id=session_id, user=request.user.id)
        messages=Message.objects.filter(session=session, user=request.user.id)
        print(messages)
    # Logic for handling chat sessions
    template = loader.get_template('chat/session.html')
    print("hello")
    return render(request, 'chat/session.html', {'messages': messages})

#c24b16ec0ae791f3752c37b665c73858-us18


def chat_home(request,current_session=None):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('my-login')
        # Create a new session_key for a new chat session
        if current_session:
            session = ChatSession.objects.get(id=current_session, user=request.user.id)
            messages = Message.objects.filter(session=session, user=request.user.id)
            chat_sessions=ChatSession.objects.filter(user=request.user.id).order_by('-created_at')
            return render(request, 'chat/home.html', {'messages': messages,"chat_sessions":chat_sessions})
        else:
            new_session_key = uuid.uuid4().hex
            print(new_session_key)  # Generate a new session key
            request.session['session_key'] = new_session_key  # Store it in the session

            # Create a new ChatSession object with the new session_key
            ChatSession.objects.create(id=new_session_key, user=request.user.id)
            # request.session.save()
            print(request.user.id)

            # Retrieve messages for the new session
            # messages = Message.objects.filter(session=session, user=request.user.id)
            chat_sessions=ChatSession.objects.filter(user=request.user.id).order_by('-created_at')
            return render(request, 'chat/home.html', {'messages': [],"chat_sessions":chat_sessions})

    elif request.method == 'POST':
        # Use the existing session_key from the user's session
        session_key = request.session.get('session_key')
        if session_key:
            # Retrieve the existing ChatSession object using the session_key
            session = ChatSession.objects.get(id=session_key, user=request.user.id)
            user_input = request.POST.get('user_input')
            
            if user_input:
                # Generate response and save the new message
                model = genai.GenerativeModel('gemini-pro')
              
                messages = Message.objects.filter(session=session, user=request.user.id)


                conversation_context = ""
                for record in messages:
                    conversation_context += f"{record.text}\n{record.response}\n"


                full_prompt = f"{conversation_context}{user_input}"
                response = model.generate_content(full_prompt)
                Message.objects.create(session=session, text=user_input, response=response.text, user=request.user.id)      


                messages = Message.objects.filter(session=session, user=request.user.id)
                chat_sessions=ChatSession.objects.filter(user=request.user.id)

                # return render(request, 'chat/home.html', {'messages': messages,"chat_sessions":chat_sessions})
                return redirect('chat_home_with_session',current_session=str(session_key))

        else:
            # Handle the case where session_key is not found
            return redirect('chat_home') 
# def chat_home(request):
# #    if request.method == 'GET':
# #         request.session.create()
# #         session_key = request.session.session_key
# #         print(session_key)
      
# #         session, created = ChatSession.objects.create(id=session_key, user=request.user.id)    

# #         messages = Message.objects.filter(session=session,user=request.user.id)

# #         return render(request, 'chat/home.html', {'messages': messages})   

#    if request.method == 'POST':     
#         user_input = request.POST.get('user_input')
        
#         if user_input!="":
#             session, created = ChatSession.objects.get_or_create(id=request.session.session_key, user=request.user.id)
#             messages = Message.objects.filter(session=session)
#             request.session.save() 
#             model = genai.GenerativeModel('gemini-pro')
#             response = model.generate_content(user_input)
#             print(response.text)
#             Message.objects.create(session=session,text=user_input, response=response.text,user=request.user.id)
#             messages = Message.objects.filter(session=session,user=request.user.id)
#             user_input=""
#             return render(request, 'chat/home.html', {'messages': messages})
 



        # model = genai.GenerativeModel('gemini-pro')
        # response = model.generate_content(user_input)
        # print(response.text)
        # Message.objects.create(session=session,text=user_input, response=response.text,user=request.user.id)
        # messages = Message.objects.filter(session=session,user=request.user.id)
        # user_input=""
        # return render(request, 'chat/session.html', {'messages': messages})   

   

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
    
 
