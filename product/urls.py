from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.create_product_line, name='create_product_line'),
    path('<uuid:uuid>/', views.product_line, name='detail_productline'),
    path('batch/<uuid:uuid>/', views.batch_detail, name='batch_detail'),
    path('generate/batch/<uuid:uuid>/', views.generate_product_codes_for_batch,
         name='generate_product_codes_for_batch'),
    path('generate/<uuid:uuid>/', views.generate_product_codes, name='generate_product_codes_for_line'),
    path('generate/', views.generate_product_codes, name='generate_product_codes'),


]
