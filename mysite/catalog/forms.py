import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from djmoney.models.fields import MoneyField

from .models import Catalog, NewUser, MyCustomUserManager


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='E-mail адресс',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               help_text='Не более 150 символов. Имена пользователей могут содержать буквенно-цифровые, _, @, +, . и - символы',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = NewUser
        fields = ('username', 'email', 'first_name', 'password1', 'password2')


class Payment(forms.Form):
  payor = forms.CharField(max_length=30)
  payee = forms.CharField(max_length=30)
  amount = forms.CharField(max_length=30)


