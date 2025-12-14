from .models import student
from django import forms
class studentform(forms.ModelForm):
    class Meta:
        model=student
        fields=['name','cls','reg','fee']