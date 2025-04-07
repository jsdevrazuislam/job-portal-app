from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import UpdateCompanyForm, JobPreferencesForm, ResumeForm
from django.contrib import messages
from django.http import JsonResponse
from jobs.models import PostJobModel
from django.db import models
from .decorators import role_verify

# Create your views here.
@login_required(login_url='/auth/login')
def dashboard_home(request):
    user = request.user
    jobs = PostJobModel.objects.filter(user=user)
    total_active_jobs = jobs.filter(status='active').count()
    total_views = jobs.aggregate(total=models.Sum('views'))['total'] or 0
    total_applications = jobs.aggregate(total=models.Sum('application_count'))['total'] or 0
    
    context = {
        "jobs": jobs,
        "total_active_jobs": total_active_jobs,
        "total_applications": total_applications,
        "total_views": total_views
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/auth/login')
@role_verify
def applications(request):
    return render(request, 'applications.html')

@login_required(login_url='/auth/login')
def saved(request):
    return render(request, 'saved.html')

@login_required(login_url='/auth/login')
def profile(request):
    if request.user.role == 'employer':
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
    else:
        user_profile = request.user.job_seeker_profile
        resume_form = ResumeForm(instance=user_profile)
        basic_form = JobPreferencesForm(instance=user_profile)

        if request.method == "POST":
            form_type = request.POST.get("form_type")

            if form_type == "resume":
                resume_form = ResumeForm(request.POST, request.FILES, instance=user_profile)
                print(request.FILES)
                if resume_form.is_valid():
                    resume_file = request.FILES.get("resume")
                    if resume_file:
                        user_profile.resume = resume_file
                        user_profile.save(update_fields=["resume"])
                    messages.success(request, "Resume uploaded successfully")

            elif form_type == "basic_info":
                basic_form = JobPreferencesForm(request.POST, instance=user_profile)
                if basic_form.is_valid():
                    user_basic_form = basic_form.save(commit=False)
                    user_basic_form.user = request.user
                    user_basic_form.save()
                    basic_form.save()
                    messages.success(request, "Profile updated successfully")

        return render(request, "profile.html", {
            "resume_form": resume_form,
            "basic_form": basic_form,
        })

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