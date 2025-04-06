# store/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        help_text="Enter your phone number."
    )
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        # The UserProfile is automatically created by our signal.
        # Set the phone number on the profile.
        user.profile.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.profile.save()
        return user

class ReviewForm(forms.ModelForm):
    reviewer_last_name = forms.CharField(
        max_length=50, required=True, label="Last Name"
    )
    rating = forms.ChoiceField(
        choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rating"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Review Text",
        required=True
    )
    class Meta:
        model = Review
        fields = ['reviewer_last_name', 'rating', 'comment']
