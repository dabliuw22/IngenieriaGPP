from django import forms

from .models import Orden, DetalleOrdenProducto, Cliente, Producto, Pedido, DetallePedido, Proveedor
from apps.locaciones.models import Pais, Ciudad

class ClienteForm(forms.ModelForm):

	class Meta:
		model = Cliente

		fields = (
			'nombre',
			'apellidos',
			'telefono',
			'email',
			'ciudad',
		)

		labels = {
			'nombre': 'Nombre',
			'apellidos': 'Apellidos',
			'telefono': 'Telefono',
			'email': 'E-mail',
			'ciudad': 'Ciudad',	
		}

	def clean_email(self):
		email_form = self.cleaned_data['email']
		if Cliente.objects.filter(email = email_form).exists():
			self.add_error('email', 'E-mail existente, intente con otro')

		return email_form

class OrdenForm(forms.ModelForm):
	class Meta:
		model = Orden

		fields = (
			'cliente',
			'ciudad',
			'direccion',
			'servicios',
		)

class DetalleOrdenProductoForm(forms.Form):
	producto = forms.ModelChoiceField(queryset = Producto.objects.filter(stock__gt = 0))
	cantidad = forms.IntegerField(initial = 1)

	def clean_cantidad(self):
		cantidad_form = self.cleaned_data['cantidad']
		producto_form = self.cleaned_data['producto']
		if producto_form.stock < cantidad_form:
			self.add_error('cantidad', 'Cantidad invalida, excede el stock')
		if cantidad_form < 0:
			self.add_error('cantidad', 'Cantidad invalida')

		return cantidad_form

class PedidoForm(forms.ModelForm):

	class Meta:
		model = Pedido

		fields = [
			'proveedor',
			'ciudad',
			'direccion',
		]

class DetallePedidoForm(forms.ModelForm):
	class Meta:
		model = DetallePedido

		fields = (
			'producto',
			'cantidad',
		)

	def clean_cantidad(self):
		cantidad_form = self.cleaned_data['cantidad']
		if cantidad_form <= 0:
			self.add_error('cantidad', 'Cantidad invalida')

		return cantidad_form

class ProveedorForm(forms.ModelForm):

	class Meta:
		model = Proveedor

		fields = [
			'nombre',
			'email',
			'telefono',
			'ciudad',
		]