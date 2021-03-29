from django.urls import path, include
from . import views
from .views import flights, findflights, gvuelos, createflight, updateflight, cancelflight, greservas, cancelreserve, reserveflight

urlpatterns = [
    path('', flights, name="flights"),
    path('findflights/<ciudad1_name>/<ciudad2_name>', findflights, name="findflights"),
    path('gvuelos', gvuelos, name="gvuelos"),
    path('createflight', createflight, name="create_vuelo"),
    path('updateflight/<int:vuelo_id>', updateflight, name="update_vuelo"),
    path('reserveflight/<int:user_id>/<int:vuelo_id>', reserveflight, name="reserve_vuelo"),
    path('cancelflight/<int:vuelo_id>', cancelflight, name='cancel_vuelo'),
    path('greservas/<int:user_id>', greservas, name='greservas'),
    path('cancelreserve/<int:reserva_id>', cancelreserve, name='cancelreserve'),
]