from django import forms
from django.forms import ModelForm

from accounts.models import Location
from .models import ProductLine, ProductCode, Batch


class ProductLineForm(ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product_name', 'description']


class BaseProductCodeForm(ModelForm):
    quantity = forms.IntegerField(label='Quantity of Product Codes that should be generated')

    class Meta:
        model = ProductCode
        fields = ['quantity']


class ProductCodeForm(BaseProductCodeForm):
    def __init__(self, manufacturer=None, *args, **kwargs):
        super(ProductCodeForm, self).__init__(*args, **kwargs)
        if manufacturer:
            self.fields['product_line'].queryset = ProductLine.objects.filter(manufacturer=manufacturer)

    class Meta(BaseProductCodeForm.Meta):
        model = ProductCode
        fields = BaseProductCodeForm.Meta.fields + ['product_line']


class ProductCodeFromBatchForm(BaseProductCodeForm):
    class Meta(BaseProductCodeForm.Meta):
        model = ProductCode
        # fields = BaseProductCodeForm.Meta.fields + ['batch_number']
        fields = BaseProductCodeForm.Meta.fields


class BatchForm(ModelForm):
    def __init__(self, manufacturer, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = Batch
        exclude = ('product_line',)
