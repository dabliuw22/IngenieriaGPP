from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone

from apps.locaciones.models import Ciudad

# Create your models here.

class Categoria(models.Model):
	nombre = models.CharField(max_length = 100)

	def __str__(self):
		return '{}'.format(self.nombre)

class Proveedor(models.Model):
	nombre = models.CharField(max_length = 250)
	email = models.EmailField(max_length = 250)
	telefono = models.CharField(max_length = 15)
	ciudad = models.ForeignKey(Ciudad, on_delete = models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

class Bien(models.Model):
	nombre = models.CharField(max_length = 250)
	descripcion = models.TextField()
	imagen = models.ImageField(upload_to = 'img_bienes', null = True, blank = True)
	slug = models.SlugField(max_length = 250, editable = False)
	categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.nombre)
		super(Bien, self).save(*args, **kwargs)

class Producto(models.Model):
	bien = models.OneToOneField(Bien, on_delete = models.CASCADE, primary_key = True)
	stock = models.IntegerField(default = 0)
	precio = models.DecimalField(max_digits = 20, decimal_places = 2)
	reorden = models.IntegerField(default = 0)
	proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)

	def __str__(self):
		return '{}'.format(self.bien)

class Servicio(models.Model):
	bien = models.OneToOneField(Bien, on_delete = models.CASCADE, primary_key = True)
	costo = models.DecimalField(max_digits = 20, decimal_places = 2)
	extra = models.DecimalField(max_digits = 20, decimal_places = 2, default = 0)
	costo_total = models.DecimalField(max_digits = 20, decimal_places = 2, editable = False)
	video = models.CharField(max_length = 500, null = True, blank = True)
	proveedores = models.ManyToManyField(Proveedor, blank = True)

	def __str__(self):
		return '{}'.format(self.bien)

	def save(self, *args, **kwargs):
		self.costo_total = (self.costo+self.extra)
		super(Servicio, self).save(*args, **kwargs)

	def get_valor(self):
		return self.costo+self.extra

class Pedido(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)
	fecha = models.DateTimeField()
	ciudad = models.ForeignKey(Ciudad)
	direccion = models.CharField(max_length = 250)
	productos = models.ManyToManyField(Producto, blank = True, 
									   through = 'DetallePedido')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return 'Pedido: {} - Proveedor: {}'.format(self.pk, self.proveedor)

	def save(self, *args, **kwargs):
		self.fecha = timezone.now()
		super(Pedido, self).save(*args, **kwargs)

class DetallePedido(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete = models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
	cantidad = models.IntegerField()

	def get_valor(self):
		return self.producto.precio*self.cantidad

class Cliente(models.Model):
	nombre = models.CharField(max_length = 30)
	apellidos = models.CharField(max_length = 50)
	telefono = models.CharField(max_length = 15)
	email = models.EmailField()
	ciudad = models.ForeignKey(Ciudad, on_delete = models.CASCADE)

	def __str__(self):
		return '{}{}{}'.format(self.nombre, ' ', self.apellidos)

class Orden(models.Model):
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	fecha = models.DateTimeField()
	ciudad = models.ForeignKey(Ciudad)
	direccion = models.CharField(max_length = 250)
	servicios = models.ManyToManyField(Servicio, blank = True, related_name = 'ordenes_servicio')
	productos = models.ManyToManyField(Producto, blank = True, 
									   through = 'DetalleOrdenProducto', related_name = 'ordenes_producto')

	class Meta:
		ordering = ['-fecha']

	def __str__(self):
		return 'Orden: {} - Cliente: {}'.format(self.pk, self.cliente)

	def save(self, *args, **kwargs):
		self.fecha = timezone.now()
		super(Orden, self).save(*args, **kwargs)

class DetalleOrdenProducto(models.Model):
	orden = models.ForeignKey(Orden, on_delete = models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
	cantidad = models.IntegerField(default = 1)

	def get_valor(self):
		return self.producto.precio*self.cantidad


class Noticia(models.Model):
	titulo = models.CharField(max_length = 250)
	resumen = models.CharField(max_length = 250)
	contenido = models.TextField()
	fecha_hora = models.DateTimeField(auto_now_add = True, editable = False)
	foto = models.ImageField(upload_to = 'img_noticia', blank = True)
	slug = models.SlugField(max_length = 250, editable = False)
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.titulo)
		super(Noticia, self).save(*args, **kwargs)