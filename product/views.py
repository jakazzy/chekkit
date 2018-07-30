from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.detail import DetailView

from product.models import ProductLine, ProductCode
from .forms import ProductLineForm, ProductCodeForm, BatchForm


# Create your views here.
@login_required()
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


def product_line(request, uuid):
    pl = ProductLine.objects.get(uuid=uuid)
    products = ProductCode.objects.filter(product_line=pl)
    return render(request, 'product/product_line_detail.html', {'pl': pl, 'products': products})


@login_required()
def generate_product_codes(request, uuid=None):
    current_user_manufacturer = request.user.profile.manufacturer
    if request.method == 'POST':
        product_form = ProductCodeForm(current_user_manufacturer, request.POST)
        batch_form = BatchForm(current_user_manufacturer, request.POST)
        if product_form.is_valid and batch_form.is_valid:

            batch = batch_form.save(commit=False)
            batch.save()
            product = product_form.save(commit=False)

            product.batch_number = batch
            product.generated_by = request.user
            product.save()
            return redirect(reverse('product:detail_productline', args=(product.product_line.uuid, )))
    else:
        batch_form = BatchForm(current_user_manufacturer)
        if uuid:
            product_line = ProductLine.objects.get(uuid=uuid)
            product_form = ProductCodeForm(current_user_manufacturer, initial={'product_line': product_line})
        else:
            product_form = ProductCodeForm(current_user_manufacturer)
        return render(request, 'product/generate_product_codes.html',
                      {'product_form': product_form, 'batch_form': batch_form,
                       'manufacturer': current_user_manufacturer})


def view_product_codes(request):
    return render(request, 'product/view_product_codes.html')
