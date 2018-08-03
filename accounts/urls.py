from django.urls import path

from accounts import views

app_name='accounts'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('manufacturer/', views.manufacturer, name='manufacturer'),
    path('create_manufacturer/', views.create_manufacturer, name='create_manufacturer'),
]
