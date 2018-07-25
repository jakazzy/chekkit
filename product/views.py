from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.detail import DetailView

from account.models import Manufacturer
from product.models import ProductLine
from .forms import ProductLineForm, ProductForm


# Create your views here.
def add_productlines(request):
    if request.method == 'POST':
        form = ProductLineForm(request.POST)
        if form.is_valid:
            # new_form= form.cleaned_data
            form.save()

            return HttpResponseRedirect('/')
    else:
        form = ProductLineForm()
    return render(request, 'product/add_productline.html', {'form': form})


class ProductLineView(DetailView):
    model = ProductLine
    template_name = 'product/product_line_detail.html'
    content_object_name = 'productline'


def generate_product_codes(request, uuid=None):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid:
            # new_form= form.cleaned_data
            form.save()

            return HttpResponseRedirect('/')
    else:
        current_user_manufacturer = request.user.profile.manufacturer
        if uuid:
            product_line = ProductLine.objects.get(uuid=uuid)
            form = ProductForm(current_user_manufacturer, initial={'product_line': product_line})
        else:
            form = ProductForm(current_user_manufacturer)
        return render(request, 'product/generate_product_codes.html', {'form': form, 'manufacturer': current_user_manufacturer})
