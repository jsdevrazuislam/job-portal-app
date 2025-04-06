import datetime

def static_data(request):
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
        "dashboard_navigation": [
            { "name": "Dashboard", "href": "/dashboard/", "icon": "layout-dashboard" },
            { "name": "Applications", "href": "/dashboard/applications/", "icon": "file-text" },
            { "name": "Saved Jobs", "href": "/dashboard/saved/", "icon": "bookmark-check" },
            { "name": "Profile", "href": "/dashboard/profile/", "icon": "user" },
            { "name": "Settings", "href": "/dashboard/settings/", "icon": "settings" },
        ],
        "job_types":[
            {
                "label":"Full-time"
            },
            {
                "label":"Part-time"
            },
            {
                "label":"Contract"
            },
            {
                "label":"Internship"
            },
        ],
        "work_mode":[
            {"label": "Remote"},
            {"label": "Hybrid"},
            {"label": "On-site"},
        ],
        "experience":[
            {"label": "Entry Level (0-2 years)"},
            {"label": "Mid Level (2-5 years)"},
            {"label": "Senior Level (5+ years)"},
            {"label": "Executive Level"},
        ],
        "education":[
            {"label": "High School"},
            {"label": "Bachelors Degree"},
            {"label": "Masters Degree"},
            {"label": "PhD"},
            {"label": "Any"},
        ]
    }
