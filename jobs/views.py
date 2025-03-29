from django.shortcuts import render
from joblisting.views import get_footer_data
# Create your views here.
def view_jobs(request):
    footer_data = get_footer_data()
    return render(request, 'view_jobs.html', footer_data)