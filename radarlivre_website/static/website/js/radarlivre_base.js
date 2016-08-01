$(function() {

	componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {

		rl_base.doInit();
			
	});
	
});

var rl_base = function() {

	return {

		doInit : function() {

			jQuery.fn.exists = function() {

				return this.length > 0;

			}

			if($(".rl-parallax-background").exists()) {
				
				console.log("Init parallax-background");
				rl_parallax_background.doInit();
				
			}

			// Mostrando componentes após as configurações iniciais
			$(".rl-foreground").fadeOut('slow');

		}, 

		getURLParameter : function (sParam) {

		    var sPageURL = window.location.search.substring(1);
		    var sURLVariables = sPageURL.split('&');
		    
		    for (var i = 0; i < sURLVariables.length; i++) {

		        var sParameterName = sURLVariables[i].split('=');
		        
		        if (sParameterName[0] == sParam) {

		            return sParameterName[1];

		        }

		    }

		    return null;

		}, 
		
		doShowSnackbar : function(message, timeout) {
						
			if(message !== undefined && message !== null && MDL_LOADED) {
				
				'use strict'
				
				timeout = timeout === undefined || timeout === null? 2000: timeout;
				var snackbar = document.querySelector("#rl-snackbar");
				snackbar.MaterialSnackbar.showSnackbar({
					
					message: message, 
					timeout: timeout
					
				});
				
				console.log(message);
				
			}
			
		}

	};

} ();

var rl_parallax_background = function() {

	// Guarda o último valor da cor de background
	// Necessário porque alguns navegadores substituem o rgba(0, 0, 0, 0) por transparent
	var lastRGBA = "rgba(0, 0, 0, 0)";

	// Altura da imagem de background
	var headerImageHeight = 0.0;

	// Função que calcula a altura da imagem de background
	var headerHeightFunction = function () {

		// A altura da imagem é calculada com base na largura, estabelecendo
		// um aspecto de 16:9
		headerImageHeight = $(window).width() * 9.0 / 16.0 * 0.6;

	}

	// Função que deixa o header transparente ou não com base na rolagem da página
	var scrollFunction = function () {
		
	    var scroll = $(".rl-main").scrollTop();

	    $(".rl-header-image__background").css('background-position', '0px ' + (-scroll * 0.5) + "px");

	    var opacity = scroll > headerImageHeight * 0.5?
	    	((scroll - headerImageHeight*0.8) / (headerImageHeight * 0.2)):
	    	0;

	    if(opacity > 1) 
	    	opacity = 1;

	    var rawRgb = $(".rl-header").css("background-color");

	    if(rawRgb == "transparent")
	    	rawRgb = lastRGBA;

	    rgb = rawRgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);

	    if(rgb == null) {

	    	rgb = rawRgb.substring(rawRgb.indexOf('(') + 1, rawRgb.lastIndexOf(')')).split(/,\s*/);
	    	var rgba = "rgba(" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + ", " + opacity + ")";
	    	$(".rl-header").css("backgroundColor", rgba);
	    	lastRGBA = rgba;

	    } else {

	    	var rgba = "rgba(" + rgb[1] + ", " + rgb[2] + ", " + rgb[3] + ", " + opacity + ")";
	    	$(".rl-header").css("backgroundColor", rgba);
	    	lastRGBA = rgba;

	    }

	    if(opacity < 1)
	    	$(".rl-header").css("box-shadow", "none");
	    else
			$(".rl-header").css({ boxShadow : "0 2px 2px 0 rgba(0,0,0,.14),0 3px 1px -2px rgba(0,0,0,.2),0 1px 5px 0 rgba(0,0,0,.12)" });

	    if($(".rl-header__fab").exists()) {
	    	if(opacity >= 1) {
	    		console.log("To 1");
	    		$(".rl-header__fab").fadeIn();
	    	} else {
	    		console.log("To 0");
	    		$(".rl-header__fab").fadeOut();
	    	}
	    }

	};


	return {

		doInit : function() {

			headerHeightFunction();
			scrollFunction();

			// Iniciando stellar, plugin para paralaxe na imagem de fundo
			$(".rl-main").scroll(scrollFunction);

			// Setando altura apropriada para o frame de referencia 
			$(".rl-header-image__frame").height( headerImageHeight );
			$(window).resize(function() {
				headerHeightFunction();
				scrollFunction();
				$(".rl-header-image__frame").height( headerImageHeight );
			});

			$(".rl-main").animate({
		        scrollTop: headerImageHeight * 0.8
		    }, 800);

		}

	};

} ();



