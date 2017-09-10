
$(function() 
{
	$("#add-restaurant-form").on('submit', function() {
		name = $("#id_name").val()
		city = $("#id_city").val()
		address = $("#id_address").val()
		cuisine = $("#id_cuisine").val()
		borough = $("#id_borough").val()
		image = $("#id_image").val()
        
        var error = false;

		if(name == "")
		{
			$("#error_name").show()
			$("#id_name").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		if(city == "")
		{
			$("#error_city").show()
			$("#id_city").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		if(address == "")
		{
			$("#error_address").show()
			$("#id_address").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		if(borough == "")
		{
			$("#error_borough").show()
			$("#id_borough").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		if(cuisine == "")
		{
			$("#error_cuisine").show()
			$("#id_cuisine").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		if($("#checkbox-image").is(':checked'))
		{
			$("#id_image_default").val("yes")
		}
		else
		{
			$("#id_image_default").val("no")
		}
		if(!$("#checkbox-image").is(':checked') && image == "")
		{
			$("#error_image").show()
			$("#id_image").css({ boxShadow: "0px 0px 3px 2px firebrick" })
            error = true
		}
		return !error;
	});
	
	$("#id_name").click(function() {
		$("#error_name").hide();
		$("#id_name").css({ boxShadow: "" })
	});
	$("#id_city").click(function() {
		$("#error_city").hide();
		$("#id_city").css({ boxShadow: "" })
	});
	$("#id_address").click(function() {
		$("#error_address").hide();
		$("#id_address").css({ boxShadow: "" })
	});
	$("#id_cuisine").click(function() {
		$("#error_cuisine").hide();
		$("#id_cuisine").css({ boxShadow: "" })
	});
	$("#id_borough").click(function() {
		$("#error_borough").hide();
		$("#id_borough").css({ boxShadow: "" })
	});
	$("#id_image").click(function() {
		$("#error_image").hide();
		$("#id_image").css({ boxShadow: "" })
	});
	
	
    $( "#id_city" ).autocomplete
    ({
		source: function (request, response) 
		{
			city = request.term
			city = city.replace(/á/gi,"a");
			city = city.replace(/é/gi,"e");
			city = city.replace(/í/gi,"i");
			city = city.replace(/ó/gi,"o");
			city = city.replace(/ú/gi,"u");
			city = city.replace(/ñ/gi,"n");
			city = city.replace(/\s+/g, '-');
			$.getJSON("/cities/"+city, function (data) 
			{
				response(data);
			});
		},
		minLength: 3,
		select: function (event, ui) {
 			var selectedObj = ui.item;
			$("#id_city").val(selectedObj.value);
			return false;
		}
	});
	$("#id_city").autocomplete("option", "delay", 300);


	function parseURL(url)
	{
		var data = url;
		data = data.toLowerCase();
		// error con algunos caracteres / º
		data = data.replace(/c\//g, "calle ");
		data = data.replace(/nº/g, "");
		data = data.replace(/,/g, "");
		data = data.replace(/á/gi,"a");
		data = data.replace(/é/gi,"e");
		data = data.replace(/í/gi,"i");
		data = data.replace(/ó/gi,"o");
		data = data.replace(/ú/gi,"u");
		data = data.replace(/ñ/gi,"n");
		data = data.replace(/\s+/g, '-');
		return data;
	}
	
	
	$( "#resolve_address" ).click
    (
		function () 
		{
			$("#error_address").hide();
			$("#id_address").css({ boxShadow: "" })
			if($("#id_name").val() == "" && $("#id_city").val() == "")
			{
				$("#address_notfound").show();
				$("#add-address").text("Añadir dirección manualmente");
				$("#add-address").show();
			}
			else
			{
				$("#resolve_address").html("Buscando");
				$("#resolve_address").addClass("loading");
				$("#img-restaurant").attr("src","../static/images/loading_preview.gif");
				$("#img-restaurant").show();
				$("#address_notfound").hide();
				name = $("#id_name").val()
				name = name+" "+$("#id_city").val()
				//name = name.replace(/\s+/g,"+")
				//name = name.replace(/,/g,"+")
				name = name.replace(/á/gi,"a");
				name = name.replace(/é/gi,"e");
				name = name.replace(/í/gi,"i");
				name = name.replace(/ó/gi,"o");
				name = name.replace(/ú/gi,"u");
				name = name.replace(/ñ/gi,"n");
				name = name.replace(/\s+/g, '-');
;				$.getJSON("/address/"+name, function (data) 
				{
					$("#resolve_address").html("Buscar dirección");
					$("#resolve_address").removeClass("loading");
					if(data === "error")
					{
						$("#address_notfound").show();
						$("#add-address").text("Añadir dirección manualmente");
						$("#add-address").show();
						$("#img-restaurant").hide();
					}
					else
					{
						$("#id_address").val(data)
						$("#add-address").text("Modificar dirección");
						$("#add-address").show();
						$("#img-restaurant").attr("src","/find/image/"+parseURL(data));
					}
				});
			}
		}
	);
	
	$("#add-address").click
	(
		function ()
		{
			$("#id_address").prop('readonly', false);
			$("#address_notfound").hide();
			$("#add-address").hide();
		}
	);
	
	$("#checkbox-image").change(function() {
		if(this.checked) {
			$("#id_image").prop('disabled', true);
			var data = $("#id_address").val();
			if(data != "") {
				$("#img-restaurant").attr("src","/find/image/"+parseURL(data));
				$("#img-restaurant").show();
			}
		}
		else
		{
			$("#id_image").prop('disabled', false);
			readURL($("#id_image"));
		}
	});

	function readURL(input) {

	    if (input.files && input.files[0]) {
	        var reader = new FileReader();

	        reader.onload = function (e) {
	            $('#img-restaurant').attr('src', e.target.result);
	        }

	        reader.readAsDataURL(input.files[0]);
	    }
	}

	$("#id_image").change(function(){
	    readURL(this);
	});
});
