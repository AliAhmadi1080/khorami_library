from django import forms
from .models import CustomeUser

class CustomeUserForm(forms.ModelForm):

    class Meta:
        model = CustomeUser
        fields = ['fullname','classname','joined_number']