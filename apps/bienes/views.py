# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView,
								  DeleteView,)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, cm

from .models import (Noticia, Bien, Producto, Servicio, Orden, DetalleOrdenProducto,
					 Cliente, Pedido, DetallePedido, Proveedor,)
from .forms import (OrdenForm, ClienteForm, DetalleOrdenProductoForm, PedidoForm,
					DetallePedidoForm, ProveedorForm,)

from apps.locaciones.models import Pais

# Create your views here.
def index(request):
	noticias = Noticia.objects.all().order_by('-fecha_hora')[:3]

	return render(request, 'index.html', {'noticias': noticias})

class Index(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(Index, self).get_context_data(**kwargs)
		context['noticias'] = Noticia.objects.all().order_by('-fecha_hora')[:3]

		return context

class UpdateUsuario(UpdateView):
	model = User
	fields = ['first_name', 'last_name', 'email', 'username']
	template_name = 'usuario/usuario_edit.html'
	success_url = reverse_lazy('index')

class ListNoticia(ListView):
	template_name = 'noticia/noticia_list.html'

	def get_queryset(self):
		return Noticia.objects.all().order_by('-fecha_hora')

class DetailNoticia(DetailView):
	model = Noticia
	template_name = 'noticia/noticia_detail.html'

class ListProducto(ListView):
	template_name = 'bien/producto/producto_list.html'

	def get_queryset(self):
		productos = Producto.objects.filter(stock__gt = 0)
		
		return productos

class DetailProducto(DetailView):
	model = Producto
	template_name = 'bien/producto/producto_detail.html'

	def get_context_data(self, **kwargs):
		context = super(DetailProducto, self).get_context_data(**kwargs)
		id_producto = context['object'].pk
		bien = Bien.objects.get(id = id_producto)
		proveedor = context['object'].proveedor
		context['bien'] = bien
		context['proveedor'] = proveedor

		return context

class ListServicio(ListView):
	model = Servicio
	template_name = 'bien/servicio/servicio_list.html'
	context_object_name = 'servicios'

class DetailServicio(DetailView):
	model = Servicio
	template_name = 'bien/servicio/servicio_detail.html'

	def get_context_data(self, **kwargs):
		context = super(DetailServicio, self).get_context_data(**kwargs)
		id_servicio = context['object'].pk
		proveedores = context['object'].proveedores.all()
		context['bien'] = Bien.objects.get(id = id_servicio)
		context['proveedores'] = proveedores

		return context

class ListOrden(ListView):
	model = Orden
	template_name = 'orden/orden_list.html'
	context_object_name = 'ordenes'

class OrdenCreate(CreateView):
	model = Orden
	template_name = 'orden/orden_create.html'
	form_class = OrdenForm

	def get_context_data(self, **kwargs):
		context = super(OrdenCreate, self).get_context_data(**kwargs)
		context['paises'] = Pais.objects.all()
		context['clientes'] = Cliente.objects.all()
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if request.user.is_authenticated:
			if form.is_valid():
				orden = form.save(commit = False)
				orden.usuario = request.user
				orden.save()
				form.save_m2m();
				return HttpResponseRedirect(reverse_lazy('bien:orden_details_create', kwargs={'pk': orden.pk}))

		return self.render_to_response(self.get_context_data(form = form))

class DetalleOrdenProductoCreate(SingleObjectMixin, ListView):
	template_name = 'orden/orden_details_create.html'

	def get_queryset(self):
		object_list = DetalleOrdenProducto.objects.filter(orden__pk = self.object.pk)
		
		return object_list

	def get_context_data(self, **kwargs):
		context = super(DetalleOrdenProductoCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = DetalleOrdenProductoForm()
		if 'object_list' not in context:
			context['object_list'] = self.get_queryset()
		if 'object' not in context:
			context['object'] = self.object

		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset = Orden.objects.all())

		return super(DetalleOrdenProductoCreate, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(queryset = Orden.objects.all())
		self.object_list = self.get_queryset()
		form = DetalleOrdenProductoForm(request.POST)

		if form.is_valid():
			clean_form = form.cleaned_data
			detalle = DetalleOrdenProducto(orden = self.object, producto = clean_form.get('producto'),
										   cantidad = clean_form.get('cantidad'))
			if not self.exists_object_in_queryset(self.object_list, detalle):
				detalle.save()
			else:
				producto = DetalleOrdenProducto.objects.get(orden__pk = self.object.pk, producto = detalle.producto)
				producto.cantidad+=detalle.cantidad
				producto.save()

			p = clean_form.get('producto')
			p.stock=p.stock-detalle.cantidad
			p.save()  
			return redirect('bien:orden_details_create', pk = self.object.pk)
		return self.render_to_response(self.get_context_data(form = form))


	def list_queryset(self, queryset):
		list = []
		for object in queryset:
			list.append(object.producto.pk)

		return list
			

	def exists_object_in_queryset(self, queryset, object):
		estado = False
		if isinstance(object, DetalleOrdenProducto):
			if object.producto.pk in self.list_queryset(queryset):
				estado = True
		return estado

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('bien:orden_details_create', kwargs = {'pk': pk})

def detalle_orden_producto_delete(request, pk):
	template_name = 'orden/orden_details_delete.html'
	detalle = get_object_or_404(DetalleOrdenProducto, id = pk)
	
	if request.method == 'POST':
		producto = detalle.producto
		orden = detalle.orden
		producto.stock+=detalle.cantidad
		producto.save()
		detalle.delete()
		return redirect('bien:orden_details_create', pk = orden.pk)

	return render(request, template_name, {'object': detalle})

class OrdenUpdate(UpdateView):
	model = Orden
	form_class = OrdenForm
	template_name = 'orden/orden_update.html'

	def get_success_url(self):
		pk = self.kwargs['pk']

		return reverse_lazy('bien:orden_details_create', kwargs = {'pk': pk})

class OrdenDelete(DeleteView):
	model = Orden
	template_name = 'orden/orden_delete.html'
	success_url = reverse_lazy('bien:orden_list')

class ClienteCreate(CreateView):
	model = Cliente
	form_class = ClienteForm
	template_name = 'usuario/cliente_create.html'
	success_url = reverse_lazy('bien:orden_create')

	def get_context_data(self, **kwargs):
		context = super(ClienteCreate, self).get_context_data(**kwargs)
		context['paises'] = Pais.objects.all()
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)

		return context

class ListPedido(ListView):
	model = Pedido
	template_name = 'pedido/pedido_list.html'
	context_object_name = 'pedidos'

class PedidoCreate(CreateView):
	model = Pedido
	form_class = PedidoForm
	template_name = 'pedido/pedido_create.html'

	def get_context_data(self, **kwargs):
		context = super(PedidoCreate, self).get_context_data(**kwargs)
		if 'proveedores' not in context:
			context['proveedores'] = Proveedor.objects.filter(pk__in = self.get_list_id_provedores())
		if 'paises' not in context:
			context['paises'] = Pais.objects.all()
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			pedido = form.save(commit = False)
			pedido.usuario = request.user
			pedido.save()
			return HttpResponseRedirect(reverse_lazy('bien:pedido_details_create', kwargs={'pk': pedido.pk}))

		return self.render_to_response(self.get_context_data(form = form))

	def get_list_id_provedores(self):
		list = []
		for producto in Producto.objects.all():
			list.append(producto.proveedor.pk)

		return list

class PedidoUpdate(UpdateView):
	model = Pedido
	form_class = PedidoForm
	template_name = 'pedido/pedido_update.html'

	def get_success_url(self):
		pk = self.kwargs['pk']

		return reverse_lazy('bien:pedido_details_create', kwargs = {'pk': pk})

class PedidoDelete(DeleteView):
	model = Pedido
	template_name = 'pedido/pedido_delete.html'
	success_url = reverse_lazy('bien:pedido_list')

class ProveedorCreate(CreateView):
	model = Proveedor
	form_class = ProveedorForm
	template_name = 'usuario/proveedor_create.html'
	success_url = reverse_lazy('bien:pedido_create')

	def get_context_data(self, **kwargs):
		context = super(ProveedorCreate, self).get_context_data(**kwargs)
		if 'paises' not in context:
			context['paises'] = Pais.objects.all()
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)

		return context

class DetallePedidoCreate(SingleObjectMixin, ListView):
	template_name = 'pedido/pedido_details_create.html'

	def get_queryset(self):
		object_list = DetallePedido.objects.filter(pedido__pk = self.object.pk)

		return object_list

	def get_context_data(self, **kwargs):
		context = super(DetallePedidoCreate, self).get_context_data(**kwargs)
		if 'productos' not in context:
			context['productos'] = Producto.objects.filter(proveedor = self.object.proveedor)
		if 'object' not in context:
			context['object'] = self.object
		if 'object_list' not in context:
			context['object_list'] = self.get_queryset()
		if 'form' not in context:
			context['form'] = DetallePedidoForm()

		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object(queryset = Pedido.objects.all())

		return super(DetallePedidoCreate, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object(queryset = Pedido.objects.all())
		self.object_list = self.get_queryset()
		form = DetallePedidoForm(request.POST)

		if form.is_valid():
			clean_form = form.cleaned_data
			detalle = DetallePedido(pedido = self.object, producto = clean_form.get('producto'),
									cantidad = clean_form.get('cantidad'))
			if not self.exists_object_in_queryset(self.object_list, detalle):
				detalle.save()
			else:
				producto = DetallePedido.objects.get(pedido = self.object, producto = detalle.producto)
				producto.cantidad+=detalle.cantidad
				producto.save()
			p = clean_form.get('producto')
			p.stock += detalle.cantidad 
			p.save()

			return redirect('bien:pedido_details_create', pk = self.object.pk)
		return self.render_to_response(self.get_context_data(form = form))

	def list_queryset(self, queryset):
		list = []
		for object in queryset:
			if isinstance(object, DetallePedido):
				list.append(object.producto.pk)
		return list
			
	def exists_object_in_queryset(self, queryset, object):
		estado = False
		if isinstance(object, DetallePedido):
			if object.producto.pk in self.list_queryset(queryset):
				estado = True
		return estado 

def detalle_pedido_delete(request, pk):
	template_name = 'pedido/pedido_details_delete.html'
	detalle = get_object_or_404(DetallePedido, id = pk)
	
	if request.method == 'POST':
		producto = detalle.producto
		pedido = detalle.pedido
		producto.stock=producto.stock-detalle.cantidad
		producto.save()
		detalle.delete()
		return redirect('bien:pedido_details_create', pk = pedido.pk)

	return render(request, template_name, {'object': detalle})

######### PDF #########

def get_total(orden):
	total = None
	if isinstance(orden, Orden):
		detalle_productos = DetalleOrdenProducto.objects.filter(orden__pk = orden.pk)
		servicios = orden.servicios.all()
		total = 0
		for detalle in detalle_productos:
			total+=detalle.get_valor()
		for servicio in servicios:
			total=total+(servicio.costo+servicio.extra)

	return total

def send_factura(request, pk):
	orden = get_object_or_404(Orden, id = pk)

	pdf = get_pdf(orden)
	nombre_pdf = 'factura-orden'+str(orden.pk)+'.pdf'
	asunto = 'Factura Orden de Compra '+str(orden.pk)+' - Ingeniería GPP'
	email_to = [orden.cliente.email]
	contenido = '<p>Sr(a) '+orden.cliente.nombre+' '+orden.cliente.apellidos+',</p>'
	contenido+='<p>Adjuntamos factura de orden de compra.</p>'
	contenido+='<p><b>Ingenier&iacute;a GPP</b></p><p>Ingenier&iacute;a, Gesti&oacute;n de Proyectos y Productos </p>' 
	mensaje = EmailMessage(asunto, contenido, to = email_to)
	mensaje.attach(nombre_pdf, pdf, 'application/pdf')
	mensaje.content_subtype = 'html'
	mensaje.send()

	return render(request, 'orden/orden_envio_factura.html')

def factura_imprimir(request, pk):

	orden = get_object_or_404(Orden, id = pk)
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'attachment; filename=factura-orden'+pk+'.pdf'

	pdf = get_pdf(orden)

	response.write(pdf)

	return response

def get_pdf(orden):
	buffer = BytesIO()
	c = canvas.Canvas(buffer, pagesize = A4)
	fecha = str(orden.fecha.day)+'/'+str(orden.fecha.month)+'/'+str(orden.fecha.year)
	
	#Header
	c.setLineWidth(.3)
	#Titulo
	c.setFont('Helvetica', 22)
	c.drawString(30, 750, 'Ingenieria GPP')
	#Subtitulo
	c.setFont('Helvetica', 12)
	c.drawString(30, 735, 'Factura de Compra')
	#Fecha
	c.setFont('Helvetica-Bold', 15)
	c.drawString(480, 750, fecha)
	#Línea
	c.line(460, 747, 560, 747)
	#end Header

	detalle_productos = orden.detalleordenproducto_set.all()
	servicios = orden.servicios.all()
	h1 = 690
	h2 = h1
	h3 = h2
	h4 = h3

	#Table Detalle Orden Productos
	#Styles
	styles = getSampleStyleSheet()
	styleBH = styles['Normal']
	styleBH.alignment = TA_CENTER
	styleBH.fontsize = 10
	#end Styles
	tabla_orden = []
	#Encabezado Tabla 
	encabezado_tabla = [
		Paragraph('''Detalle''', styleBH), Paragraph('''Valor''', styleBH)
	]
	tabla_orden.append(encabezado_tabla)
	lista = [
		{'detalle': 'Cliente', 'valor': orden.cliente},
		{'detalle': 'Pais', 'valor': orden.ciudad.pais},
		{'detalle': 'Ciudad', 'valor': orden.ciudad},
		{'detalle': 'Direccion', 'valor': orden.direccion},
	]

	for i in lista:
		o = [i['detalle'], i['valor']]
		tabla_orden.append(o)
		h1-=18

	#end Encabezado Tabla
	h2 = h1-28 #10 de distancia entre tabla y 18 del encabezado
	h3 = h2
	h4 = h3
	width, height = A4
	table1 = Table(tabla_orden, colWidths=[7*cm, 12*cm])
	table1.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), 
							   ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
	table1.wrapOn(c, width, height)
	table1.drawOn(c, 30, h1)
	#end Table Detalle Orden Productos

	if detalle_productos:
		#Table Detalle Orden Productos
		#Styles
		styles = getSampleStyleSheet()
		styleBH = styles['Normal']
		styleBH.alignment = TA_CENTER
		styleBH.fontsize = 10
		#end Styles
		tabla_productos = []
		#Encabezado Tabla 
		encabezado_tabla = [
			Paragraph('''Producto''', styleBH), Paragraph('''Unidades''', styleBH), 
			Paragraph('''Precio''', styleBH), Paragraph('''Valor''', styleBH)
		]
		tabla_productos.append(encabezado_tabla)
		#end Encabezado Tabla
		#Cuerpo Tabla
		for detalle in detalle_productos:
			p = [
				detalle.producto.bien, 
				str(detalle.cantidad), 
				str(detalle.producto.precio), 
				str(detalle.get_valor())
			]
			tabla_productos.append(p)
			h2-=18
		#end Cuerpo Tabla
		h3 = h2-28 #10 de distancia entre tabla y 18 del encabezado
		h4 = h3
		width, height = A4
		table2 = Table(tabla_productos, colWidths=[10*cm, 3*cm, 3*cm, 3*cm])
		table2.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), 
								   ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
		table2.wrapOn(c, width, height)
		table2.drawOn(c, 30, h2)
	#end Table Detalle Orden Productos

	if servicios:
		#Table Servicios
		#Styles
		styles = getSampleStyleSheet()
		styleBH = styles['Normal']
		styleBH.alignment = TA_CENTER
		styleBH.fontsize = 10
		#end Styles
		tabla_servicios = []
		#Encabezado Tabla
		encabezado_tabla = [
			Paragraph('''Servicio/Proyecto''', styleBH), Paragraph('''Costo''', styleBH), 
			Paragraph('''Extra''', styleBH), Paragraph('''Valor''', styleBH)
		]
		tabla_servicios.append(encabezado_tabla)
		#end Encabezado Tabla
		#Cuerpo Tabla
		for servicio in servicios:
			s = [
				servicio.bien,
				str(servicio.costo),
				str(servicio.extra),
				str(servicio.get_valor())
			]
			tabla_servicios.append(s)
			h3-=18
		h4 =h3-28
		width, height = A4
		table3 = Table(tabla_servicios, colWidths=[10*cm, 3*cm, 3*cm, 3*cm])
		table3.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), 
								   ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
		table3.wrapOn(c, width, height)
		table3.drawOn(c, 30, h3)
		#end Table Servicios
	total = get_total(orden)
	if total:
		if total > 0:
			#Table Servicios
			#Styles
			styles = getSampleStyleSheet()
			styleBH = styles['Normal']
			styleBH.alignment = TA_CENTER
			styleBH.fontsize = 10
			#end Styles
			tabla_total = []
			#Encabezado Tabla
			encabezado_tabla = [
				Paragraph('''Total''', styleBH), str(total)
			]
			tabla_total.append(encabezado_tabla)
			width, height = A4
			table4 = Table(tabla_total, colWidths=[16*cm, 3*cm])
			table4.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), 
									   ('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))
			table4.wrapOn(c, width, height)
			table4.drawOn(c, 30, h4)

	c.showPage()
	c.save()
	pdf = buffer.getvalue()
	buffer.close()
	
	return pdf
