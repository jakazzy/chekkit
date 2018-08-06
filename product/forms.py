from django.forms import ModelForm

from accounts.models import Location
from .models import ProductLine, ProductCode, Batch, CodeCollection


class ProductLineForm(ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product_name', 'description']


class CodeCollectionForm(ModelForm):
    class Meta:
        model = CodeCollection
        fields = ('quantity',)


class ProductCodeForm(ModelForm):
    def __init__(self, manufacturer=None, *args, **kwargs):
        super(ProductCodeForm, self).__init__(*args, **kwargs)
        if manufacturer:
            self.fields['product_line'].queryset = ProductLine.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = ProductCode
        fields = ['product_line']


class ProductCodeFromBatchForm(ModelForm):
    def __init__(self, manufacturer=None, *args, **kwargs):
        super(ProductCodeFromBatchForm, self).__init__(*args, **kwargs)
        if manufacturer:
            self.fields['product_line'].queryset = ProductLine.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = ProductCode
        fields = ['batch_number']


class BatchForm(ModelForm):
    def __init__(self, manufacturer, *args, **kwargs):
        super(BatchForm, self).__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = Batch
        exclude = ('product_line',)
