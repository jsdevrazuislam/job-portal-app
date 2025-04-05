from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import UpdateCompanyForm
from django.contrib import messages
from django.http import JsonResponse

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
    profile = request.user.company_profile
    if request.method == 'POST':
        form = UpdateCompanyForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        messages.success(request, 'Profile Updated Successfully')
        return render(request, 'profile.html', { 'form': form })
    else:
        form = UpdateCompanyForm(instance=profile)
        return render(request, 'profile.html', { 'form': form })

@login_required(login_url='/auth/login')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='/auth/login')
@csrf_exempt
def delete_company_logo(request):
    if request.method == 'POST':
        user = request.user
        if hasattr(user, 'company_profile') and user.company_profile.logo:
             user.company_profile.logo.delete()
        user.company_profile.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})