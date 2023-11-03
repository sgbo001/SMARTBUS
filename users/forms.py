from django import forms
from django.contrib.auth.models import User  # Import User from django.contrib.auth.models
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your email address')

    class Meta:
        model = User  # Use User from django.contrib.auth.models
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'city', 'state', 'address']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'phone_number', 'city', 'state', 'address']