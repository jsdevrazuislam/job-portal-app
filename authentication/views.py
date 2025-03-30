from django.shortcuts import render, redirect
from joblisting.views import get_footer_data
from .forms import UserRegisterForm
from django.contrib.auth import login as loginUser, authenticate
from django.contrib import messages

def login(request):
    footer_data = get_footer_data()
    if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html', footer_data)

def register(request):
    footer_data = get_footer_data()
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    context = {**footer_data, "form": form} 
    return render(request, 'register.html', context)