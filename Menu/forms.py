from django import forms
from .models import *

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'phone_number','email', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user