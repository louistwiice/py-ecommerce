from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from mptt.models import MPTTModel, TreeForeignKey

from utilities.common_model import TimestampBase
from utilities.choices import Colors


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        self.name = str(self.name).title()
        super(Category, self).save(*args, **kwargs)


class Item(TimestampBase):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    size = models.CharField(max_length=25)
    color = models.CharField(max_length=80, choices=Colors.CHOICES, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    category = models.ForeignKey(Category, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)


class Image(TimestampBase):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="items/images/")


