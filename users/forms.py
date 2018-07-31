from .models import User
from django.forms import ModelForm
from django.forms import Form
from django import forms


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['country_code', 'phone_number', 'password']
        widgets = {'password': forms.PasswordInput()}


class PhoneVerificationForm(Form):
    verification_code = forms.CharField(max_length=10)