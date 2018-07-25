from django.shortcuts import render

from product.models import ProductLine


# Create your views here.

def overview(request):
    product_lines = ProductLine.objects.filter(manufacturer=request.user.profile.manufacturer)
    context = {
        'product_lines': product_lines
    }
    return render(request, 'frontend/overview.html', context)
