from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class':'input','placehloder':'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placehloder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class':'input','placehloder':'First_name'}),
            'last_name': forms.TextInput(attrs={'class':'input','placehloder':'Last_name'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        CITY = [
            ('Astana','Astana'),
            ('Almaty', 'Almaty'),
            ('Shimkent','Shimkent'),
        ]
        model = UserProfile
        fields = ('phone','address','city','country','image')
        widgets = {
            'phone': forms.TextInput(attrs={'class':'input','placehloder':'Phone:'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placehloder': 'Address:'}),
            'city': forms.Select(attrs={'class':'input','placehloder':'City:'},choices=CITY),
            'country': forms.TextInput(attrs={'class':'input','placehloder':'Country'}),
            'image': forms.FileInput(attrs={'class':'input','placehloder':'Image:'  })
        }

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=150, label='User name: ')
    email = forms.EmailField(max_length=200, label='Email: ')
    first_name = forms.CharField(max_length=150, label='First_name: ')
    last_name = forms.CharField(max_length=150, label='Last_name: ')

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1',
                  'password2')

