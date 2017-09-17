from django.conf.urls import url

from .views import BusquedaAjaxView

urlpatterns = [
	url(r'^pais/busqueda/ciudad/$', BusquedaAjaxView.as_view(), name = 'ajax_busqueda'),
]