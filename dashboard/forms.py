from django import forms
from authentication.models import CompanyProfile, UserProfile
from django.contrib import messages 

class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["name", "industry", "company_size", "build_year", "website", "location", "description", "logo"]

class JobPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["title", "location", "years_of_experience", "work_mode", "phone_number", "about_me", "job_type", "salary"]

class ResumeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['resume']

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if resume.size > 2 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 2MB.")
        return resume
