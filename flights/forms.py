from django.forms import ModelForm
from .models import vuelo, reserva

class vueloForm(ModelForm):
    class Meta:
        model = vuelo
        #fields = ['customer', 'product']
        fields = '__all__'

class reservaForm(ModelForm):
    class Meta:
        model = reserva
        fields = ['nombre', 'cc']
