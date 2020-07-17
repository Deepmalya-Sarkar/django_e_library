from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()

    class Meta:
        model=User
        fields=("username","email","first_name","last_name","password1","password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["designation","profile_pic",]

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField()
    last_name=forms.CharField()
    class Meta:
        model=User
        fields=("username","email","first_name","last_name")

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=("profile_pic",)

