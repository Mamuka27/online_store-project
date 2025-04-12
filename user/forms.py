# user/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            user.profile.phone_number = self.cleaned_data.get('phone_number')
            user.profile.save()
        return user
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']