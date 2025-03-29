from django.shortcuts import render
import datetime


def get_footer_data():
    return {
        "year": datetime.datetime.now().year,
        "social_links": [
            {"name": "Facebook", "url": "#", "icon": 'facebook'},
            {"name": "Twitter", "url": "#", "icon": 'twitter'},
            {"name": "LinkedIn", "url": "#", "icon": 'linkedin'},
        ],
        "job_seeker_links": [
            {"name": "Browse Jobs", "url": "/jobs"},
            {"name": "Career Advice", "url": "/career-advice"},
            {"name": "Resume Builder", "url": "/resume-builder"},
            {"name": "Salary Guide", "url": "/salary-guide"},
            {"name": "Job Alerts", "url": "/job-alerts"},
        ],
        "employer_links": [
            {"name": "Post a Job", "url": "/post-job"},
            {"name": "Pricing", "url": "/pricing"},
            {"name": "Resources", "url": "/employer-resources"},
            {"name": "Success Stories", "url": "/success-stories"},
            {"name": "Contact Sales", "url": "/contact-sales"},
        ],
        "company_links": [
            {"name": "About Us", "url": "/about"},
            {"name": "Contact", "url": "/contact"},
            {"name": "Privacy Policy", "url": "/privacy"},
            {"name": "Terms of Service", "url": "/terms"},
            {"name": "FAQ", "url": "/faq"},
        ],
    }

def home(request):
    footer_data = get_footer_data()
    return render(request, 'index.html', footer_data)