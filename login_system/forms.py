from django import forms
from django.forms import ModelForm
from alldata.models import User


class MyUserCreateForm(ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    password_copy = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','password']