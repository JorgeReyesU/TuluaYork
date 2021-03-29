from django.conf import settings
from django.db import models

# Create your models here.

class vacuna(models.Model):
    nombre = models.CharField(max_length=20)
    periodicidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class impuesto(models.Model):
    nombre = models.CharField(max_length=40)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre


class ciudad(models.Model):
    nombre = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    visa = models.BooleanField()

    def __str__(self):
        return self.nombre

class interface_vacuna(models.Model):
    vacuna = models.ForeignKey(vacuna, on_delete=models.CASCADE)
    destino = models.ForeignKey(ciudad, on_delete=models.CASCADE)

class interface_impuesto(models.Model):
    impuesto = models.ForeignKey(impuesto, on_delete=models.CASCADE)
    destino = models.ForeignKey(ciudad, on_delete=models.CASCADE)

class vuelo(models.Model):
    nombre = models.CharField(max_length=20)
    origen = models.ForeignKey(ciudad, related_name='origen', on_delete=models.CASCADE)
    destino = models.ForeignKey(ciudad, related_name='destino', on_delete=models.CASCADE)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    fecha_llegada = models.DateField()
    hora_llegada = models.TimeField()
    costo = models.IntegerField()
    estado = models.BooleanField(default=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class escala(models.Model):
    vuelo = models.ForeignKey(vuelo, on_delete=models.CASCADE)
    destino = models.ForeignKey(ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.destino.nombre

class reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vuelo = models.ForeignKey(vuelo, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=20)
    cc = models.CharField(max_length=12)

    def __str__(self):
        return self.vuelo.nombre
