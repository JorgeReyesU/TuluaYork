from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class usuario(models.Model):
    max_vuelos = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
