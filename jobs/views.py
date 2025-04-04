from django.shortcuts import render
# Create your views here.
def view_jobs(request):
    return render(request, 'view_jobs.html')

def job_details(request, job_id):
    return render(request, 'single_job_details.html')

def post_job(request):
    return render(request, 'post_job.html')