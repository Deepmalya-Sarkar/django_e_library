from django.shortcuts import render
from ebook.decorators import unauthenticated_user

@unauthenticated_user
def home(request):
    return render(request,'ebook/home.html')

def welcome(request):
    return render(request,'ebook/welcome.html')

def instructions(request):
    return render(request,'ebook/instructions.html')