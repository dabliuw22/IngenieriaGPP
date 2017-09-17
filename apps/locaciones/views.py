from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Pais, Ciudad

# Create your views here.

class BusquedaAjaxView(TemplateView):
	
	def get(self, request, *args, **kwargs):
		id_pais = request.GET['id']
		ciudades = Ciudad.objects.filter(pais__id = id_pais)
		data = serializers.serialize('json', ciudades, fields = ('pk', 'nombre'))

		return HttpResponse(data, content_type = 'applications/json')