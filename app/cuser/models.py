from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    picture = models.ImageField(
        blank=True,
        null=True,
        upload_to="users/images/",
    )
