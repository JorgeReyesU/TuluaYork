from django.contrib import admin
from flights.models import reserva, escala, vuelo, ciudad, impuesto, vacuna

admin.site.register(reserva)
admin.site.register(escala)
admin.site.register(vuelo)
admin.site.register(ciudad)
admin.site.register(impuesto)
admin.site.register(vacuna)
