from django.contrib import admin
from .models import PerfilUsuario, Mascota, Asignatura, SesionEstudio, RegistroAnimo, Tarjeta, Especialidad, Psicologo, Logro, ObtencionLogro

# Register your models here.

admin.site.register(PerfilUsuario)
admin.site.register(Mascota)
admin.site.register(Asignatura)
admin.site.register(SesionEstudio)
admin.site.register(RegistroAnimo)
admin.site.register(Tarjeta)
admin.site.register(Especialidad)
admin.site.register(Psicologo)
admin.site.register(Logro)
admin.site.register(ObtencionLogro)
