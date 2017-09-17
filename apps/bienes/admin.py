from django.contrib import admin

from apps.bienes.models import (Categoria, Proveedor, Bien, Producto, 
							   Servicio, Pedido, Cliente, Orden, 
							   DetallePedido, DetalleOrdenProducto, Noticia)


class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

class ProveedorAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'email', 'telefono', 'ciudad')

class BienAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'slug', 'categoria')

class ProductoAdmin(admin.ModelAdmin):
	list_display = ('bien', 'stock', 'precio', 'reorden')

class ServicioAdmin(admin.ModelAdmin):
	list_display = ('bien', 'costo_total',)

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('pk', 'usuario', 'proveedor')

class DetallePedidoAdmin(admin.ModelAdmin):
	list_display = ('pedido', 'producto', 'cantidad')

class ClienteAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'apellidos', 'telefono', 'email', 'ciudad')

class OrdenAdmin(admin.ModelAdmin):
	list_display = ('pk', 'usuario', 'cliente', 'ciudad', 'direccion')

class DetalleOrdenProductoAdmin(admin.ModelAdmin):
	list_display = ('orden', 'producto', 'cantidad')

class NoticiaAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'slug', 'resumen', 'usuario', 'fecha_hora')

# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Bien, BienAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido, DetallePedidoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(DetalleOrdenProducto, DetalleOrdenProductoAdmin)
admin.site.register(Noticia, NoticiaAdmin)