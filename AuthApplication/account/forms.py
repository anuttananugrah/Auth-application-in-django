from django import forms
from account.models import *
from django.contrib.auth.forms import UserCreationForm

class UserModelForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","phone","email","username"]
        widgets={
            "first_name":forms.TextInput(attrs={'placeholder':'Enter First Name','class':'form-control bg-transparent' }),
            "last_name":forms.TextInput(attrs={'placeholder':'Enter Last Name','class':'form-control'}),
            "phone":forms.TextInput(attrs={'placeholder':'Enter Phone Number','class':'form-control'}),
            "email":forms.EmailInput(attrs={'placeholder':'Enter Email ID','class':'form-control'}),
            "username":forms.TextInput(attrs={'placeholder':'Enter Username','class':'form-control'})
        }

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Enter Username','class':'form-control'})) 
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'})) 
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['owner']