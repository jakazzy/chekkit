from django.shortcuts import render

from accounts.forms import ManufacturerForm


def profile(request):
    return render(request, 'account/profile.html')


def manufacturer(request):
    return render(request, 'account/manufacturer.html')


def create_manufacturer(request):
    if request.method == 'POST':
        create_manufacturer_form = ManufacturerForm(request.POST)
    else:
        create_manufacturer_form = ManufacturerForm()

    return render(request, 'account/create_manufacturer.html', {'create_manufacturer_form': create_manufacturer_form})
