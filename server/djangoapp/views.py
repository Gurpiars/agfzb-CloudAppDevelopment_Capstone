from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def base(request):
    return render(request, 'base.html')

def about(request):
    return render (request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render (request, 'djangoapp/contact.html')

def registration(request):
    return render (request, 'djangoapp/registration.html')

# Create a `login_request` view to handle sign in request
def login_req(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'djangoapp/index.html')

def signout(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def signup(request):
        if request.method == 'POST':
            first_name=request.POST['first_name']
            username = request.POST['username']
            password = request.POST['password']
            user= User.objects.create_user(username,'',password)
            user.first_name=first_name
            user.save()
            return redirect('djangoapp:index')
        return render(request,'django/index.html')



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    url='https://gurpiarsingh-3000.theiadocker-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

