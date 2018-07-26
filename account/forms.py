from django.forms import ModelForm

from .models import Manufacturer, Location, Profile


class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['code', 'name', 'industry']


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name']


class ProfileForm(ModelForm):
    