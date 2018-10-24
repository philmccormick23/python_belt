from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime 
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
import bcrypt
from .models import User

# the index function is called when root is visited

def index(request):
    dictionary = {
        'users' : User.objects.all()
    }
    
    return render(request, 'index.html', dictionary)

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        print(errors)
        return redirect('/')
    new_user = User(
        name=request.POST['name'],
        alias=request.POST['alias'],
        email=request.POST['email'],
        password=bcrypt.hashpw(request.POST['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        #Password.objects.create(pwd = password.decode('utf-8') 
        #user = User.objects.get(id = new_user.id)
    )
    new_user.save()
    request.session['id'] = new_user.id 
    request.session['name']= new_user.name
    return redirect('/pokes')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors):
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    #request.POST['password'].encode('utf-8')
    
    request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
    request.session['name']= User.objects.get(email=request.POST['email']).name 
    return redirect('/pokes')

def success(request):
    dictionary = {
        'users' : User.objects.exclude(name=request.session['name']).order_by('-counter', 'name'), 
        'currUser' : User.objects.get(id=request.session['id'])

    }
    return render(request,'success.html', dictionary)


def poke(request, id):
    x = User.objects.get(id=id)
    x.counter+=1
    x.save()
    return redirect('/pokes')