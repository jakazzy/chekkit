from django import template

from product.models import ProductLine, Batch

register = template.Library()
@register.filter
def product_lines(request):
    return ProductLine.objects.filter(manufacturer__profile__user=request.user)

@register.filter
def batch_numbers(request):
    return Batch.objects.filter(location__manufacturer=request.user.profile.manufacturer)

