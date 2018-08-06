from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from product.models import ProductLine, ProductCode, Batch
from .forms import ProductLineForm, ProductCodeForm, BatchForm, ProductCodeFromBatchForm, CodeCollectionForm


# Create your views here.
@login_required()
def create_product_line(request):
    next = request.GET.get('next', '/')
    if request.method == 'POST':
        create_product_line_form = ProductLineForm(request.POST)
        if create_product_line_form.is_valid():
            product_line = create_product_line_form.save(commit=False)
            product_line.manufacturer = request.user.profile.manufacturer
            product_line.save()
            next = request.POST.get('next')
            if next != '/':
                return redirect(next + str(product_line.uuid) + '/')
            else:
                return redirect(reverse('product:detail_productline', args=(product_line.uuid,)))
    else:
        create_product_line_form = ProductLineForm()
    return render(request, 'product/create_product_line.html',
                  {'create_product_line_form': create_product_line_form, 'next': next})




def product_line(request, uuid):
    product_line_object = ProductLine.objects.get(uuid=uuid)
    product_codes = ProductCode.objects.filter(product_line=product_line_object).order_by('created')
    paginator = Paginator(product_codes, 20)

    page = request.GET.get('page')
    product_codes = paginator.get_page(page)
    return render(request, 'product/product_line_detail.html',
                  {'product_line_object': product_line_object, 'product_codes': product_codes})


def batch_detail(request, uuid):
    batch = Batch.objects.get(uuid=uuid)
    product_codes = ProductCode.objects.filter(batch_number__uuid=uuid)
    paginator = Paginator(product_codes, 20)

    page = request.GET.get('page')
    product_codes = paginator.get_page(page)
    return render(request, 'batch/batch_detail.html', {'product_codes': product_codes, 'batch_object': batch})


@login_required()
def generate_product_codes(request, uuid=None):
    current_user_manufacturer = request.user.profile.manufacturer
    if request.method == 'POST':
        collection_form = CodeCollectionForm(request.POST)
        product_form = ProductCodeForm(current_user_manufacturer, request.POST)
        batch_form = BatchForm(current_user_manufacturer, request.POST)
        print('product: ', product_form.is_valid())
        print('batch: ', batch_form.is_valid())
        if product_form.is_valid() and collection_form.is_valid() and batch_form.is_valid():
            collection = collection_form.save(commit=False)
            product = product_form.save(commit=False)
            batch = batch_form.save(commit=False)

            collection.manufacturer = product.product_line.manufacturer
            collection.save()

            batch.product_line = product.product_line
            batch.save()

            for c_time in range(0, collection.quantity):
                ProductCode.objects.create(batch_number=batch, product_line=product.product_line, collection=collection)

            return redirect(reverse('product:detail_productline', args=(product.product_line.uuid,)))
        return redirect('/')
    else:
        batch_form = BatchForm(current_user_manufacturer)
        collection_form = CodeCollectionForm()
        if uuid:
            product_line = ProductLine.objects.get(uuid=uuid)
            product_form = ProductCodeForm(current_user_manufacturer, initial={'product_line': product_line})
        else:
            product_form = ProductCodeForm(current_user_manufacturer)
        return render(request, 'product/generate_product_codes.html',
                      {'product_form': product_form, 'batch_form': batch_form,
                       'manufacturer': current_user_manufacturer, 'collection_form': collection_form})


@login_required()
def generate_product_codes_for_batch(request, uuid):
    batch = Batch.objects.get(uuid=uuid)
    if request.method == 'POST':
        product_form = ProductCodeFromBatchForm(request.POST)
        if product_form.is_valid():

            product = product_form.save(commit=False)

            quantity = product_form.cleaned_data['quantity']

            for c_time in range(0, quantity):
                ProductCode.objects.create(batch_number=batch, generated_by=request.user,
                                           product_line=batch.product_line)

            return redirect(reverse('product:batch_detail', args=(batch.uuid,)))
    else:
        product_form = ProductCodeFromBatchForm(initial={'batch_number': batch})
        return render(request, 'product/generate_product_codes.html',
                      {'product_form': product_form,
                       'manufacturer': request.user.profile.manufacturer})


def product_code(request, uuid, id):
    product_code_object = ProductCode.objects.get(id=id, product_line__uuid=uuid)
    return render(request, 'product/product_code.html', {'product_code_object': product_code_object})
