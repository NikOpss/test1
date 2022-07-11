from django.urls import path, include
from .views import exchange
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', HomeCatalog.as_view(), name='home'),
    path('exchange', exchange, name='exchange'),
    path('payment', payment, name='payment'),
    path('account', account, name='account')
    # path('exchange_app/index/', ExchangeApp.as_view(), name='index'),

]