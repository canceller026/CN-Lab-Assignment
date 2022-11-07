from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def loginView(request):
    if request.method == 'POST':
        print("Press login page")
        username = request.POST.get('username')
        password = request.POST.get('password')

        #   Verify information: exception: no field is empty
        if len(username) == 0 or len(password) == 0:
            messages.info(request, "These boxes are not allowed to leave blank")
            return redirect('/login')

        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/chat')
        else:
            messages.info(request, "Username or password is incorrect")
            return redirect('/login')
    return render(request, "login.html")


def register(request):
    return render(request, 'register.html')

def logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('login'))
"""

"""