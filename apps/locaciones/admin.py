from django.contrib import admin

from apps.locaciones.models import Pais, Ciudad

class PaisAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class CiudadAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'pais')

# Register your models here.

admin.site.register(Pais, PaisAdmin)
admin.site.register(Ciudad, CiudadAdmin)