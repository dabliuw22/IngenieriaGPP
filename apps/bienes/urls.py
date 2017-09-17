from django.conf.urls import url
from django.contrib.auth.views import password_change
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from .views import (UpdateUsuario, ListNoticia, DetailNoticia, ListProducto, DetailProducto, ListServicio,
					DetailServicio, ListOrden, OrdenCreate, OrdenUpdate, OrdenDelete, ClienteCreate, 
					DetalleOrdenProductoCreate, detalle_orden_producto_delete, ListPedido, PedidoCreate, 
					PedidoUpdate, PedidoDelete, ProveedorCreate, DetallePedidoCreate, detalle_pedido_delete,
					send_factura, factura_imprimir,)


urlpatterns = [
	url(r'^usuario/editar/(?P<pk>\d+)$', login_required(UpdateUsuario.as_view()), name = 'usuario_update'),
	url(r'^usuario/editar/password/$', password_change, {'template_name': 'usuario/password/edit_password.html', 'post_change_redirect': reverse_lazy('index')}, name = 'update_password'),
	url(r'^noticia/lista$', ListNoticia.as_view(), name='noticia_list'),
	url(r'^noticia/(?P<slug>[-\w]+)-(?P<pk>\d+)$', DetailNoticia.as_view(), name='noticia_detail'),
	url(r'^producto/lista$', ListProducto.as_view(), name='producto_list'),
	url(r'^producto/(?P<slug>[-\w]+)-(?P<pk>\d+)$', DetailProducto.as_view(), name='producto_detail'),
	url(r'^servicio/lista$', ListServicio.as_view(), name='servicio_list'),
	url(r'^servicio/(?P<slug>[-\w]+)-(?P<pk>[\d]+)$', DetailServicio.as_view(), name='servicio_detail'),
	url(r'^orden/lista$', login_required(ListOrden.as_view()), name='orden_list'),
	url(r'^orden/nueva$', login_required(OrdenCreate.as_view()), name='orden_create'),
	url(r'^orden/edit/(?P<pk>\d+)$', login_required(OrdenUpdate.as_view()), name='orden_update'),
	url(r'^orden/eliminar/(?P<pk>\d+)$', login_required(OrdenDelete.as_view()), name='orden_delete'),
	url(r'^orden/cargar/(?P<pk>\d+)$', login_required(DetalleOrdenProductoCreate.as_view()), name='orden_details_create'),
	url(r'^orden/detalle/eliminar/(?P<pk>\d+)$', detalle_orden_producto_delete, name="orden_details_delete"),
	url(r'^pedido/lista$', login_required(ListPedido.as_view()), name='pedido_list'),
	url(r'^pedido/nuevo$', login_required(PedidoCreate.as_view()), name='pedido_create'),
	url(r'^pedido/edit/(?P<pk>\d+)$', login_required(PedidoUpdate.as_view()), name='pedido_update'),
	url(r'^pedido/eliminar/(?P<pk>\d+)$', login_required(PedidoDelete.as_view()), name='pedido_delete'),
	url(r'^pedido/cargar/(?P<pk>\d+)$', login_required(DetallePedidoCreate.as_view()), name='pedido_details_create'),
	url(r'^pedido/detalle/eliminar/(?P<pk>\d+)$', detalle_pedido_delete, name='pedido_details_delete'),
	url(r'^cliente/nuevo$', login_required(ClienteCreate.as_view()), name='cliente_create'),
	url(r'^proveedor/nuevo$', login_required(ProveedorCreate.as_view()), name='proveedor_create'),
	url(r'^orden/send/factura/(?P<pk>\d+)', send_factura, name='orden_factura_send'),
	url(r'^orden/factura/(?P<pk>\d+)$', factura_imprimir, name='orden_factura_imprimir'),
]