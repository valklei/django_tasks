from django.shortcuts import render
from django.http import HttpResponse


def hello_world(request):
    return HttpResponse("<h1>hello world</h1>")

def second_view(request):
    return HttpResponse("<h1>Hello! It's my second view!</h1>")

def home(request):
    return render(request, 'home.html')


# Create your views here.
