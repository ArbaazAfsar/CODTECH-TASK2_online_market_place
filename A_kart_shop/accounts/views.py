from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Customer
from store.models import Category  

from django.contrib.auth import login, logout, authenticate




def log_in(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Ensure both fields are provided
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'login.html', {'Categories': categories})
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            # Incorrect credentials
            messages.error(request, "Invalid username or password. Please try again or register.")
            return render(request, 'login.html', {'Categories': categories})
    
    return render(request, 'login.html', {'Categories': categories})

        
        
        
        

def register(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if password matches confirm_password
        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please try again.")
            return render(request, 'register.html', {'Categories': categories})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "The username already exists. Please choose a different username.")
            return render(request, 'register.html', {'Categories': categories})
        
        # Check if email already exists
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'register.html', {'Categories': categories})
        
        # Create User and Customer
        try:
            user = User.objects.create_user(username=username, password=password)
            Customer.objects.create(
                name=username,
                email=email,
                user=user,
                phone=phone,
            )
            messages.success(request, "You have been successfully registered. Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    
    return render(request, 'register.html', {'Categories': categories})

def log_out(request):
    logout(request)
    return redirect('login')
