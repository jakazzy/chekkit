from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import ManufacturerForm, ProfileForm
from accounts.models import Location
from product.models import ProductLine, CodeCollection


# Create your views here.
def overview(request):
    if request.user.is_authenticated:
        if not request.user.profile.activated:
            if request.method == 'POST':
                create_manufacturer_form = ManufacturerForm(request.POST)
                profile_form = ProfileForm(request.POST)
                if create_manufacturer_form.is_valid() and profile_form.is_valid():
                    manufacturer = create_manufacturer_form.save()
                    position = profile_form.cleaned_data['position']
                    profile = request.user.profile
                    profile.manufacturer = manufacturer
                    profile.activated = True
                    profile.position = position
                    Location.objects.create(name=manufacturer.address, manufacturer=manufacturer)
                    profile.save()
                return redirect(reverse('frontend:overview'))
            else:
                create_manufacturer_form = ManufacturerForm()
                profile_form = ProfileForm(initial={})
            return render(request, 'frontend/overview.html',
                          {'create_manufacturer_form': create_manufacturer_form, 'profile_form': profile_form})
        else:
            product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user)
            context = {
                'product_lines': product_lines,
                'overview': True
            }
            return render(request, 'frontend/overview.html', context)
    else:
        return render(request, 'frontend/landing.html', {})


def activity(request):
    context = {
        'activity': True
    }
    return render(request, 'frontend/activity.html', context)


def analytics(request):
    context = {
        'analytics': True
    }
    return render(request, 'frontend/analytics.html', context)


def collections(request):
    collection_object = CodeCollection.objects.filter(manufacturer=request.user.profile.manufacturer)
    context = {
        'collection_object': collection_object,
        'collections': True
    }
    return render(request, 'frontend/collections.html', context)
