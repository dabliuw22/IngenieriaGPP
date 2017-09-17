$(document).ready(function(){
	$("#id_pais").on('change', busqueda);
	function busqueda() {
		var id = $(this).val();
		$.ajax({
			data: {'id': id},
			url: '/pais/busqueda/ciudad/',
			type: 'GET',
			dataType: 'json',
			success: function(data){
				var html = '';
				var html2 = '';
				if(data.length > 0) {
					html = '<div class="form-group"><label>Ciudad</label>';
					html += '<select id="id_ciudad" name="ciudad" class="form-control">'
							+ '<option value="">---------</option>';
					for(var i = 0; i < data.length; i++) {
						html += '<option value="'+data[i].pk+'">'+data[i].fields.nombre+'</option>';
					}
					html += '</select></div>';
					html2 = '<div class="form-group"><label>Direccion</label><input id="id_direccion" name="direccion" type="text" class="form-control" placeholder="Direcci&oacute;n" maxlength="250"></div>';
				}
				$('#ciudades').html(html);
				$('#direccion').html(html2);
			}
		});
	}

	$('#id_pais_cliente').on('change', busquedaCiudades);
	function busquedaCiudades() {
		var id =$(this).val();
		$.ajax({
			data: {'id': id},
			url: '/pais/busqueda/ciudad/',
			type: 'GET',
			dataType: 'json',
			success: function(data){
				var html = '';
				if(data.length > 0) {
					html = '<div class="form-group"><label>Ciudad</label>';
					html += '<select id="id_ciudad" name="ciudad" class="form-control">'
							+ '<option value="">---------</option>';
					for(var i = 0; i < data.length; i++) {
						html += '<option value="'+data[i].pk+'">'+data[i].fields.nombre+'</option>';
					}
					html += '</select></div>';
				}
				$('#ciudades_cliente').html(html);
			}
		});
	}

	$('#id_pais_proveedor').on('change', buscarCiudadesP);
	function buscarCiudadesP() {
		var id = $(this).val();
		console.log(id);
		$.ajax({
			data: {'id': id},
			type: 'GET',
			url: '/pais/busqueda/ciudad/',
			dataType: 'json',
			success: function(data) {
				var html = '';
				if(data.length > 0) {
					html = '<div class="form-group"><label>Ciudad</label>';
					html += '<select id="id_ciudad" name="ciudad" class="form-control">'
							+ '<option value="">---------</option>';
					for(var i = 0; i < data.length; i++) {
						html += '<option value="'+data[i].pk+'">'+data[i].fields.nombre+'</option>';	
					}
					html += '</select></div>';
				}
				$('#ciudades_proveedor').html(html);
			}
		});
	}
});