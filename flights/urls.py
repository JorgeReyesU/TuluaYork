from django.urls import path, include
from . import views
from .views import flights

urlpatterns = [
    path('', views.flights, name="flights"),
]