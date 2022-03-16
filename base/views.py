
# This file contains the business logic for the application
# Curator: Sriram Narayanan
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Recipe
from .forms import RecipeForm
import random
import json
import requests
import os
import time


# Function for logging in a user (accessed via POST)
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

# Function for logging out a user
def logoutUser(request):
    logout(request)
    return redirect('home')

# Function for registering first time user via POST request
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

# Home page route - renders the home page template
def home(request):
    recipe = Recipe.objects.all()
    context = {'recipes':recipe}
    return render(request, 'base/home.html', context)

# Displays all recipes
def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    messages = recipe.message_set.all()
    context = {'recipe':recipe}
    return render(request, 'base/recipe-entry.html',context)

# Contact us Page Generator
def contactUs(request):
    return render(request,'base/contact-us.html')

# Help Page Generator
def helpPage(request):
    return render(request,'base/help-page.html')

# Recipe Generator which calls the microservices
def recipeGenerator(request,pk):
    user = User.objects.get(id=pk)
    recipes = Recipe.objects.all()
    form = UserCreationForm()
    if request.method == 'POST':
        # Trigger the submit button
        submitbutton = request.POST.get('submit')
        data = None
        # Assemble input for microservice
        input_data = {}
        rand = random.randint(0,12)
        data_pool = {"cuisine":["nordic","spanish","cajun","indian","thai","mediterranean","mexican","japanese","lebanese","vietnamese", "french"],
        "diets":["vegan","paleo","whole","gluten free"]}
        input_data["maxCalories"] = 100*rand
        input_data["minCalories"] = 100
        input_data["cuisine"] = data_pool["cuisine"][rand%10]
        print(input_data["cuisine"])
        time.sleep(2)
        input_data["diets"] = data_pool["diets"][rand%len(data_pool["diets"])]
        #Write input to JSON
        jsonWrite = open(f"static//microservice//recipe_input.json","w")
        jsonWrite.write(json.dumps(input_data))
        #close JSON
        jsonWrite.close()
        #Call microservice
        os.system('python3 static//microservice//RecipeService.py')
        with open(f'static//microservice//recipe.json') as f:
            data = json.load(f)
        image_file = f'temp.{data["imageType"]}'
        r = requests.get(data['image'])
        with open(f'static//{image_file}', 'wb') as img:
            print(img)
            img.write(r.content)  
        #Publish to front end
        context = {"submitbutton":submitbutton, "title":data['title'],"recipe":data['instructions'], "pic_path":image_file}
        return render(request,'base/recipe.html',context)
    context = {'user':user,'recipes':recipes,'form':form, 'pk':pk} 
    return render(request, 'base/profile.html', context)

# Function for liking a recipe
@login_required(login_url='login')
def likeRecipe(request,recipe):
    return "logged in"

# Function for creating a recipe
@login_required(login_url='login')
def createRecipe(request):
    form = RecipeForm()
    if request.method=='POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.host = request.user
            recipe.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/recipe_form.html', context)

# Function for updating a recipe
@login_required(login_url='login')
def updateRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    form  = RecipeForm(instance=recipe)
    #Form created only if the user is valid
    if request.user != recipe.host:
        return HttpResponse('Restricted action')
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/recipe_form.html', context)

#Function for deleting a recipe
# Login is required
@login_required(login_url='login')
def deleteRecipe(request,pk):
    recipe = Recipe.objects.get(id=pk)
    if request.user != recipe.host:
        return HttpResponse('Restricted action')
    if request.method == "POST":
        recipe.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':recipe})