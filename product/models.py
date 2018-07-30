import uuid
from django.utils.timezone import now
from random import randint

from django.conf import settings
from django.db import models

from accounts.models import Manufacturer, Location


class ProductLine(models.Model):
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='images', blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.manufacturer, self.product_name)


class Batch(models.Model):
    production_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    batch_number = models.IntegerField(unique=True, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.location.manufacturer_name, self.batch_number)


class ProductCode(models.Model):
    product_code = models.IntegerField(unique=True, blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    batch_number = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)


    def __str__(self):
        return str(self.product_code)

    def get_code(self):

        return randint(100, 3000)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.product_code = self.get_code()
        super().save(*args, **kwargs)


