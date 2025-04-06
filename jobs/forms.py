from django import forms
from .models import PostJobModel
from ckeditor.fields import RichTextFormField



class JobPostForm(forms.ModelForm):
    class Meta:
        model = PostJobModel
        fields = "__all__"
        exclude = ['created_by', 'updated_at', 'user', "salary"]
        widgets = {
            'body': RichTextFormField(),
        }