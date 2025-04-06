from django.shortcuts import render,redirect
from jobs.decorators import subscription_required
from .forms import JobPostForm
from django.contrib import messages
# Create your views here.
def view_jobs(request):
    return render(request, 'view_jobs.html')

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