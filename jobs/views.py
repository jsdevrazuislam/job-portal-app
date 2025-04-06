from django.shortcuts import render,redirect
from jobs.decorators import subscription_required
from .forms import JobPostForm
from django.contrib import messages
from .models import PostJobModel
# Create your views here.
def view_jobs(request):
    jobs = PostJobModel.objects.all()
    job_type = request.GET.getlist('type')
    work_mode = request.GET.getlist('workMode')
    salary = request.GET.get('salary')
    location = request.GET.get('location')
    title = request.GET.get('search')
    company_size = request.GET.getlist('company_size')
    sort = request.GET.get('sort')

    if job_type:
        jobs = jobs.filter(type__in=job_type)

    if work_mode:
        jobs = jobs.filter(workMode__in=work_mode)

    if salary:
        jobs = jobs.filter(salary__icontains=salary)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if title:
        jobs = jobs.filter(title__icontains=title)

    if company_size:
        jobs = jobs.filter(user__company_profile__company_size__in=company_size)
        
    if sort == "newest":
        jobs = jobs.order_by("-created_at")
    elif sort == "oldest":
        jobs = jobs.order_by("created_at")
    elif sort == "salary-high":
        jobs = jobs.order_by("-salary")
    elif sort == "salary-low":
        jobs = jobs.order_by("salary")

    return render(request, 'view_jobs.html', {"jobs": jobs})

def job_details(request, job_id):
    return render(request, 'single_job_details.html')

@subscription_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        salary = f"৳ {request.POST.get('min_salary')} - {request.POST.get('max_salary')}"
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.user = request.user
            job_post.salary = salary
            job_post.save()
            messages.success(request, "Job Create Successfully")
            return redirect('view_jobs')
        else:
            print(form.errors)
    else:
        form = JobPostForm()
        return render(request, 'post_job.html', {'form': form})