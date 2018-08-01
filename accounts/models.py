import uuid

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from invitations.models import Invitation
from invitations.signals import invite_accepted


def validate_code_length(value):
    if len(str(value)) != 4:
        raise ValidationError(
            _('Manufacturer Code must have a length of 4 should not start with zeros')
        )


class Manufacturer(models.Model):
    code = models.IntegerField(unique=True, validators=[validate_code_length])
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Location(models.Model):
    name = models.CharField(max_length=300)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def manufacturer_name(self):
        return self.manufacturer.name


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, blank=True, null=True)

    # is_admin, boolean

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    @receiver(invite_accepted, sender=auth.models.AnonymousUser)
    def invitation_accepted(sender, instance, **kwargs):
        print(instance)
