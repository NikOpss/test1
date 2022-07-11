from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from djmoney.models.fields import MoneyField
from djmoney.money import Money


class Catalog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')

    def get_absolute_url(self):
        return reverse('view_catalog', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'


class MyCustomUserManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('Вы должны предоставить e-mail адресс'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('e-mail addres'), unique=True)
    username = models.CharField(max_length=191, unique=True)
    first_name = models.CharField(max_length=191)
    date_joined = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # balance = models.DecimalField(max_digits=5, decimal_places=2, default=True)
    # balance = MoneyField(max_digits=10, decimal_places=2, null=True)

    objects = MyCustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username

class UserBalance(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    balance = MoneyField(max_digits=10, decimal_places=2, default_currency=None)

#
# user_nikita = NewUser.objects.create(username='nikita', email='nikita@gmail.com', first_name='Nikita', about='My name is Nikita')
#
#
# nikita_balance1 = UserBalance.objects.create(user=user_nikita, balance=Money(100, 'USD'))
# nikita_balance2 = UserBalance.objects.create(user=user_nikita, baalnce=Money(200, 'EUR'))






# account = NewUser.objects.create(balance=Money(10, 'USD'), email= 'ab12a@gmail.com', username = 'ab12a1',
#                                  first_name = 'ab12a2')
# # swissAccount = NewUser.objects.create(balance=Money(10, 'CHF'), email= 'aboba1@gmail.com', username = 'aboba1',
# #                                  # first_name = '2_b')
#
# NewUser.objects.filter(balance__gt=Money(1, 'USD'))


# class Data(models.Model):
#     name = models.CharField(max_length=100)
#     salary = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

# class Bank(models.Model):
#   name = models.CharField(max_length=50)
#   balance = models.DecimalField(max_digits=5, decimal_places=2)
#   created = models.DateTimeField(auto_now_add=True)
#   updated = models.DateTimeField(auto_now=True)
#
#   def __str__(self):
#     return self.name


