from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['fullname','classname','joined_number']