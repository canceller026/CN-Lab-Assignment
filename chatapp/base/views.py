from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
# Create your views here.

@login_required(login_url=('login'))
def chat(request):
    return render(request, 'chat.html')
    
@login_required(login_url=('login'))
def index(request):
    return render(request, 'index.html')