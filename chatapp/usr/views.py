from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import NewUserForm



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
            return redirect('/')
        else:
            messages.info(request, "Username or password is incorrect")
            return redirect('/login')
    return render(request, "login.html")


def registerView(request):
    if request.method=="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = NewUserForm()
    return render(request,'register.html',{"form":form})
    #if request.method =="POST":
    #    name = request.POST['yourname']
    #    print(name)
    #return render(request, 'register.html')

def logout_page(request):

    logout(request)
    return redirect('/')
"""

"""