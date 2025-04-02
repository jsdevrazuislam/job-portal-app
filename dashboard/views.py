from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/auth/login')
def dashboard_home(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/auth/login')
def applications(request):
    return render(request, 'applications.html')

@login_required(login_url='/auth/login')
def saved(request):
    return render(request, 'saved.html')

@login_required(login_url='/auth/login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='/auth/login')
def settings(request):
    return render(request, 'settings.html')