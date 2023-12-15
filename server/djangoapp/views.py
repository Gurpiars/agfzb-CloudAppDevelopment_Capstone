from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from .models import CarModel
from .restapis import get_dealers_from_cf , get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
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
    if request.method == "GET":
        context={}
        url='https://gurpiarsingh-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context={'dealerships':dealerships}
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerid):
    if request.method =="GET":
        url='https://gurpiarsingh-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews'
        context={}
        reviews = get_dealer_reviews_from_cf(url,dealerid)
        context={'reviews':reviews,'id':dealerid}
    return render(request,'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
@login_required
def add_review(request, dealerid):
    if request.method=='POST':
        user= request.user
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": user.username,  # Assuming user's username as the name
            "dealership": dealerid,
            "review": request.POST.get("review"),
            "purchase": request.POST.get("purchase"),
            "name":request.POST.get('name'),
            "review":request.POST.get('review'),
            "purchase_date":request.POST.get('purchase_date'),
            "car_make":request.POST.get("car_make"),
            "car_model":request.POST.get('car_model'),
            "car_year":request.POST.get('car_year'),
        }
        json_payload={'review':review}
        url='https://gurpiarsingh-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review'
        response=post_request(url,json_payload)
        if response:
            return response
        else:
            return HttpResponse("An error occurred while submitting the review.")
    elif request.method=="GET":
        context={}
        url='https://gurpiarsingh-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        results=get_dealers_from_cf(url,dealer_id = dealerid)
        context={'cars':CarModel.objects.all(), 'dealer':results, 'id':dealerid}
        return render(request, 'djangoapp/add_review.html', context)



