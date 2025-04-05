from django import forms
from authentication.models import CompanyProfile

class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ["name", "industry", "company_size", "build_year", "website", "location", "description", "logo"]