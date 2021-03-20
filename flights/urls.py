from django.urls import path, include
from . import views
from .views import flights, findflights

urlpatterns = [
    path('', flights, name="flights"),
    path('findflights/<ciudad1_name>/<ciudad2_name>', findflights),
]