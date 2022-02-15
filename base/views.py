from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room
from .forms import RoomForm
import random

# Create your views here.
# rooms = [
#     {'id':1, 'name':'Indian'},
#     {'id':2, 'name':'Chinese'},
#     {'id':3, 'name':'Vietnamese'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page='register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    # return HttpResponse('Home page')
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    # return HttpResponse('Room')
    room = Room.objects.get(id=pk)
    messages = room.message_set.all()
    context = {'room':room}
    return render(request, 'base/room.html',context)

def contactUs(request):
    return render(request,'base/contact-us.html')

def helpPage(request):
    return render(request,'base/help-page.html')

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = Room.objects.all()
    form = UserCreationForm()
    if request.method == 'POST':
        submitbutton = request.POST.get('submit')
        print(request)
        rand = random.randint(1,5)
        recipe_txt = None
        with open(f'static//{rand}.txt') as f:
            recipe_txt = f.readlines()
        pic_path = str(rand)+'.png'
        # rooms = Room.objects.create()s
        context = {"submitbutton":submitbutton, "recipe":recipe_txt, "pic_path":pic_path}
        return render(request,'base/recipe.html',context)
    context = {'user':user,'rooms':rooms,'form':form, 'pk':pk} 
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def likeRecipe(request,recipe):
    print("recipe-->",recipe)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        # request.POST.get('name') --> get the name
        # print(request.POST) #All the data
    context = {'form':form}
    return render(request,'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form  = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Restricted action')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Restricted action')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})