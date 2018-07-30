from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Manufacturer
from product.models import ProductLine


# Create your views here.
def overview(request):
    if request.user.is_authenticated:
        product_lines = ProductLine.objects.filter(manufacturer__profile__user=request.user)
        context = {
            'product_lines': product_lines
        }
        return render(request, 'frontend/overview.html', context)
    else:
        return render(request, 'frontend/landing.html', {})