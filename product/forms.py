from django.forms import ModelForm

from .models import ProductLine, Product


class ProductLineForm(ModelForm):
    class Meta:
        model = ProductLine
        fields = ['product_name', 'description', ]


class ProductForm(ModelForm):
    def __init__(self, manufacturer=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if manufacturer:
            self.fields['product_line'].queryset = ProductLine.objects.filter(manufacturer=manufacturer)

    class Meta:
        model = Product
        exclude = ['product_code']
