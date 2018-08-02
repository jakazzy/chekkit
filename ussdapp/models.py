from django.db import models
from jsonfield import JSONField

from product.models import ProductLine


class UssdRecord(models.Model):
    COMPLAINT_CHOICES = (('1', 'No complaint'),
                         ('2', 'Product below quality'),
                         ('3', 'Product too expensive'),)
    session_id = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15)
    product_line = models.ForeignKey(ProductLine, blank=True, null=True, on_delete=models.SET_NULL)
    complaint = models.CharField(max_length=100, choices=COMPLAINT_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gateway = models.CharField(max_length=10)
    data = JSONField(default=dict())
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('session_id', 'gateway')
        ordering = ['-created']



    def __str__(self):
        return '{}: {}'.format(self.session_id, self.phone_no)


