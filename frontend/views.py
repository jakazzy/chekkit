from django.shortcuts import render

from product.models import ProductLine


# Create your views here.
def overview(request):
    if request.user.is_authenticated:
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
