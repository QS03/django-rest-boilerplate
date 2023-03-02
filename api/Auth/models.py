# Create your models here.
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class AuthUser(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    username = models.EmailField(_('Email address'), max_length=256, unique=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    address_1 = models.CharField(max_length=256, null=True, blank=True)
    address_2 = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    zip_code = models.CharField(max_length=32, null=True, blank=True)
    image = models.ImageField(upload_to='static/image/', null=True, blank=True)
    history = HistoricalRecords()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.username}({self.first_name} {self.last_name})'
