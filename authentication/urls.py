from django.urls import path
from .views import ViewRegister, getout, acceder, perfil

urlpatterns = [
    path('', ViewRegister.as_view(), name="registration"),
    path('acceder/', acceder, name='acceder'),
    path('salir/', getout, name='getout'),
    path('perfil/<int:user_id>', perfil),
]