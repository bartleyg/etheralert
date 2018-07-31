from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, country_code, password=None):
        user = self.model(phone_number = phone_number,
                          country_code = country_code)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, country_code, email, password=None):
        user = self.model(email = email)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=10, unique=True)
    country_code = models.CharField(default='1', max_length=3)
    phone_number_verified = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'

    '''
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"phone_number": self.phone_number})
    '''


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    ethereum_address = models.CharField('Ethereum address', max_length=42)
    count = models.PositiveIntegerField(default=0)
    on_receive = models.BooleanField()
    on_send = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    txHash = models.CharField(max_length=66)
    block = models.IntegerField()
    _from = models.CharField(max_length=42)
    to = models.CharField(max_length=42)
    eth_value = models.DecimalField(max_digits=30, decimal_places=18)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    task_id = models.CharField(max_length=50, blank=True, editable=False)

