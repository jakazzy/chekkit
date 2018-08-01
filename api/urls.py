from django.urls import path

from ussdapp.views import check_it

app_name='api'
urlpatterns = [
    path('', check_it, name='check_it'),
]
