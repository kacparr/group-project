from django.shortcuts import render, redirect, get_object_or_404
from .models import Products, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ChangeUserInfoForm, ChangeBillingForm, ChangePasswordForm
from payment.forms import ChangeShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def category(request, slug):
	# Replace Hyphens with Spaces
	# foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = get_object_or_404(Category, slug=slug)
		products = Products.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def product(request,pk):
	product = Products.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})
def home(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products':products, 'categories':categories})
# Create your views here.

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)
                for k,v in converted_cart.items():
                    cart.db_add(product=k, quantity=v)

            messages.success(request, ('You Have Been Logged In!'))
            return redirect('home')
        else:
            messages.success(request, ('There was an error.'))
            return redirect('login')
    else:

        return render(request, 'login.html', {})

def logout_user(requset):
    logout(requset)
    messages.success(requset, ("You have been logged out..."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered succesfully..."))
            return redirect('home')
        else:
            messages.success(request, ("Whoopsie, there was a problem, try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})

def profile(request):
    if not request.user.is_authenticated:
        messages.success(request=request, message="You must be logged in!")
        return redirect('home')
    
    current_user = User.objects.get(id=request.user.id)

    try:
        shipping_user = ShippingAddress.objects.get(user=current_user)
    except ShippingAddress.DoesNotExist:
        shipping_user = None

    try:
        current_profile = Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
        current_profile = None

    user_form = ChangeUserInfoForm(request.POST or None, instance=current_user)
    ship_form = ChangeShippingForm(request.POST or None, instance=shipping_user)
    bill_form = ChangeBillingForm(request.POST or None, instance=current_profile)
    pass_form = ChangePasswordForm(current_user, request.POST or None)
    if request.method == 'POST':
        print(request.POST)
        if 'user_form_submit' in request.POST:
            if user_form.is_valid():
                user_form.save()
                login(request=request, user=current_user)
                messages.success(request=request, message="User updated successfully.")
                return redirect('home')
        
        if 'bill_form_submit' in request.POST:
             if bill_form.is_valid() or ship_form.is_valid():
                bill_form.save()
                ship_form.save()
                messages.success(request=request, message="Shipping info updated successfully.")
                return redirect('home')
        if 'pass_form_submit' in request.POST:
            if pass_form.is_valid():
                pass_form.save()
                messages.success(request=request, message="Password updated successfully, please log in again.")
                return redirect('login')
            else:
                for err in list(pass_form.errors.values()):
                    messages.error(request=request, message=err)
                    return redirect('profile')

    return render(request, 'profile.html', {
        'user_form':user_form, 
        'pass_form':pass_form, 
        'bill_form':bill_form, 
        'ship_form':ship_form})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Products.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))   
        if not searched:
            messages.success(request=request, message="This product does not exist.")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})

    return render(request, 'search.html', {})
