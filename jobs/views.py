from django.shortcuts import render
# Create your views here.
def view_jobs(request):
    return render(request, 'view_jobs.html')