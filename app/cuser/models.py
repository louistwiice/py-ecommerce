from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    picture = models.ImageField(blank=True, null=True, upload_to="users/images/",)
    phone_number = PhoneNumberField(blank=True)
