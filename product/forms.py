from django import forms
from django.forms import ModelForm

from accounts.models import Location
from .models import ProductLine, ProductCode, Batch


class ProductLineForm(ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product_name', 'description', ]


class ProductCodeForm(ModelForm):
    quantity = forms.IntegerField(label='Quantity of Product Codes that should be generated')

    def __init__(self, manufacturer=None, *args, **kwargs):
        super(ProductCodeForm, self).__init__(*args, **kwargs)
        if manufacturer:
            self.fields['product_line'].queryset = ProductLine.objects.filter(manufacturer=manufacturer)
        else:
            pass

    class Meta:
        model = ProductCode
        fields = ['product_line', 'quantity']

    def save(self, commit=True):
        print(self.cleaned_data['quantity'])
        return super(ProductCodeForm, self).save(commit=commit)


class BatchForm(ModelForm):
    def __init__(self, manufacturer, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = Batch
        fields = '__all__'