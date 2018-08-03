from django import forms

from .models import Manufacturer, Location, Profile


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, label='Last Name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    field_order = ['first_name', 'last_name']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('position',)
        labels = {
            "position": "Position At Company"
        }


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = "__all__"
        labels = {
            "name": "Company",
            "address": "Company Address"
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']
