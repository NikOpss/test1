from django.db import transaction
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
import requests
from .models import *
from django.views.generic import DetailView, CreateView
from django.views.generic import ListView
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import F
import decimal
from django.forms import ModelForm


class HomeCatalog(ListView):
    model = Catalog
    template_name = 'HomePage/home.html'
    context_object_name = 'catalog'

    # extra_context = {'title': 'Главная'}

    def get_context_data(self, *, object_list=None, **kwargs):
        init = super()
        context = init.get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Catalog.objects.all()


def exchange(request):
    response = requests.get(url='https://v6.exchangerate-api.com/v6/6e59cbcc93c862476157b095/latest/USD').json()
    currencies = response.get('conversion_rates')

    if request.method == 'GET':
        context = {
            'currencies': currencies
        }
        return render(request=request, template_name='exchange_app/index.html', context=context)

    if request.method == 'POST':
        from_amount = float(request.POST.get('from-amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': currencies,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='exchange_app/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


def payment(request):
    if request.method == 'POST':
        form = Payment(request.POST)

        if form.is_valid():
            x = form.cleaned_data['payor']
            y = form.cleaned_data['payee']
            z = decimal.Decimal(form.cleaned_data['amount'])

            payor = UserBalance.objects.select_for_update().get(user=x)
            payee = UserBalance.objects.select_for_update().get(user=y)

        with transaction.atomic():
            payor.balance -= z
            payor.save()

            payee.balance += z
            payee.save()

            return redirect('home')

    else:
        form = Payment()

    return render(request, 'Payment/payment.html', {'form': form})


class BalanceUser(forms.ModelForm):
    class Meta:
        model = UserBalance
        fields = ['user', 'balance']


def account(request):
    if request.method == 'POST':
        form = BalanceUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = BalanceUser()

    return render(request, 'Account/accountbalance.html', {'form': form})
