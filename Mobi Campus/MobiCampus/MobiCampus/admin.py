from django.contrib import admin
from .models import Usuario, Motorista, Administrador, Carona, CaronaHist

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Motorista)
admin.site.register(Administrador)
admin.site.register(Carona)
admin.site.register(CaronaHist)
