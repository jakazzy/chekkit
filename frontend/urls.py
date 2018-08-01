from django.urls import path
from . import views

app_name= 'frontend'
urlpatterns = [
    path('', views.overview, name='overview'),
    path('activity/', views.activity, name='activity'),
    path('analytics/', views.analytics, name='analytics'),
]
