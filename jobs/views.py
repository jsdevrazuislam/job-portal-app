from django.shortcuts import render
from jobs.decorators import subscription_required
# Create your views here.
def view_jobs(request):
    return render(request, 'view_jobs.html')

def job_details(request, job_id):
    return render(request, 'single_job_details.html')

@subscription_required
def post_job(request):
    return render(request, 'post_job.html')