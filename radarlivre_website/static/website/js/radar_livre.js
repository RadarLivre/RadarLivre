var MDL_LOADED = false;
var MAP_LOADED = false;

$(function() {

	componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {

		console.log("MDL LOADED!");
		MDL_LOADED = true;

		rl_base.doInit();
			
	});
	
});


var rl_api = function() {

	/*
	 * PRIVADO
	 */
	
	var BASE_REMOTE_URL = "http://www.radarlivre.com/api/";
	var BASE_LOCAL_URL = "http://localhost/api/";
	var BASE_LOCAL_DJANGO_URL = "http://localhost:8000/api/";
	var baseURL = BASE_REMOTE_URL;

	var updatingAirplanes = false;

	var mapReference = null;

	// Referencia ao timer de atualização
	var timerUpdater = null;

	// Valor do intervalo de atualização em milisegundos
	var DEFAULT_UPDATE_INTERVAL_TIME = 5 * 1000;
	var updateIntervalTime = DEFAULT_UPDATE_INTERVAL_TIME;

	// Atual lista de aeronaves
	var airplaneInfos = [];
	var selectedAirplaneInfo = null;
	var lastRoutePosition = null;
	
	function doGetJson(url, params, callbackSucess, callbackError, callbackFinal) {

		$.getJSON( url, params).done(function( data ) {

			callbackSucess(data);

		}).fail(function( jqxhr, textStatus, error ) {

		    callbackError(textStatus + ", " + error);

		}).always(function() {

			callbackFinal();

		});

	}

	function doUpdateAirplaneInfos() {

		if(rl_map.getMap() != null && !updatingAirplanes) {

			console.log("Atualizando aeronaves...");

			updatingAirplanes = false;

			topBound = mapReference.getBounds().getNorthEast().lat();
			bottomBound = mapReference.getBounds().getSouthWest().lat();
			leftBound = mapReference.getBounds().getSouthWest().lng();
			rightBound = mapReference.getBounds().getNorthEast().lng();

			doGetJson(baseURL + "airplane_info/?callback=?", 
				//Parâmetros da url
				{
					format : "jsonp", 
					timestampinterval: 60 * 1000, 
					top: topBound, 
					bottom: bottomBound, 
					left: leftBound, 
					right: rightBound
				},

				// Função de retorno positivo da requisição
				function(data) {
					console.log("Aeronaves atualizadas: " + data.length);
					onAirplaneInfosReceived(data);
				},

				// Função de erro da requisição
				function() {
					console.log("Erro ao atualizar aeronaves!");
				}, 

				// Finalizando a requisição
				function() {
					console.log("Requisição finlizada!");
					updatingAirplanes = false;
				}
			);

		} else {

			console.log("Pulando atualização de aeronaves...");

		}

	}

	function onAirplaneInfosReceived(response) {
		for(var i = 0; i < airplaneInfos.length; i++) {
			var airplaneInfo = airplaneInfos[i];
			if(exists(airplaneInfo, response) == -1) {
				deleteAirplaneInfo(airplaneInfo, i);
				i--;
			}
		}

		for(var i = 0; i < response.length; i++) {
			saveAirplane(response[i]);
		}
	}
	
	function doGetAirplaneRoute() {

		if(map != null && selectedAirplaneInfo != null) {

			console.log("Baixando rota para a aeronave selecionada...");
			
			var lasttimestamp = 0;				

			doGetJson(baseURL + "observation/?callback=?", 
				//Parâmetros da url
				{
					format : "jsonp",  
					airplane: selectedAirplaneInfo.airplane, 
					lasttimestamp: lasttimestamp
					//timestampinterval: 1000000000000
				},

				// Função de retorno positivo da requisição
				function(data) {
					console.log("Rota recebida: " + data.length);
					onAirplaneRouteReceived(data);
				},

				// Função de erro da requisição
				function() {
					console.log("Erro ao baixar rota da aeronave selecionada!");
				}, 

				// Finalizando a requisição
				function() {
					console.log("Requisição finlizada!");
					updatingAirplanes = false;
				}
			);

		} else {

			console.log("Pulando atualizacao da rota...");

		}

	}
	
	function onAirplaneRouteReceived(data) {
		
		if(selectedAirplaneInfo != null && data.length > 0) {
			
			for(var i = 0; i < data.length - 1; i++)
				rl_map.addLine(data[i], data[i + 1]);

			lastRoutePosition = data[data.length - 1];
			
		}
		
	}

	function exists(airplaneInfo, list) {
		var index = -1;
		$(list).each(function(i, el) {
			if(el.airplane == airplaneInfo.airplane) {
				index = i;
				return false;
			}
		});
		return index;
	}

	function saveAirplane(airplaneInfo) {
		index = exists(airplaneInfo, airplaneInfos);
		if(index != -1)
			updateAirplaneInfo(airplaneInfo, index);
		else 
			addAirplaneInfo(airplaneInfo);

		rl_map.updateMarkerFromAirplaneInfo(airplaneInfo);
	}

	function updateAirplaneInfo(airplaneInfo, index) {
		if(airplaneInfos[index].timestamp != airplaneInfo.timestamp) {
			// console.log("Atualizando a aeronave " + airplaneInfo.airplane + "...");
			airplaneInfos[index] = airplaneInfo;
			// update mark...

			if(selectedAirplaneInfo != null && airplaneInfo.airplane == selectedAirplaneInfo.airplane) {
				rl_map.addLine(lastRoutePosition, airplaneInfo);
				lastRoutePosition = airplaneInfo;
			}
		}
	}

	function addAirplaneInfo(airplaneInfo) {
		// console.log("Adicionando a aeronave " + airplaneInfo.airplane + "...");
		airplaneInfos.push(airplaneInfo);
		// create mark...
	}

	function deleteAirplaneInfo(airplaneInfo, index) {
		// console.log("Removendo a aeronave " + airplaneInfo.airplane + "...");
		airplaneInfos.splice(index, 1);

		rl_map.deleteMarker(airplaneInfo);
		
		if(selectedAirplaneInfo != null && selectedAirplaneInfo.airplane == airplaneInfo.airplane)
			rl_map.removeLine();
	}

	/*
	 * PÚBLICO
	 */

	return {

		doInit : function() {

			mapReference = rl_map.getMap();
			
			timerUpdater = setInterval(function() {

				doUpdateAirplaneInfos();

			}, updateIntervalTime);

			rl_map.setOnMarkSelected(function(marker) {
				rl_api.doSelectAirplane(marker.airplaneInfo);
			});
			rl_map.setOnMarkUnselected(function() {
				rl_api.doUnselectAirplane();
			});

		}, 

		doSelectAirplane : function(airplaneInfo) {

			console.log("Selecionando aeronave: " + airplaneInfo.airplane);
			selectedAirplaneInfo = airplaneInfo;			
			doGetAirplaneRoute();			

		}, 

		doUnselectAirplane : function() {

			console.log("Removendo seleção da aeronave: " + airplaneInfo.airplane);
			selectedAirplaneInfo = null;
			selectedAirplaneInfoRoute = null;
			rl_map.removeLine();

		}, 

		getAirplaneInfos : function() {

			return airplaneInfos;

		}

	};

} ();


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
			

			if($(".rl-map").exists()) {
				
				console.log("Init map");
				rl_map.doInit();
				rl_api.doInit();
				
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


var rl_map = function() {

	// Variável que guarda a referência ao objeto GoogleMap
	var map = null;

	// Coleção de marcadores no mapa que caracterizam os aviões
	var markers = [];
	var selectedMark = null;

	var selectedMarkPolyLines = [];

	var infowindow = null;

	var defaultIconColor = "#263238";
	var selectedIconColor = "#A0B";
	var routeColors = []	

	var onMarkSelected = function(marker) {};
	var onMarkUnselected = function(marker) {};

	function doInitColors() {

		var rgbToHex = function(r, g, b) {
		    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
		}

		var r = 255, g = 0, b = 0;

		var initColors1 = function(a, b) {
			routeColors.push(rgbToHex(r, g, b));
			if(b < 255) {
				initColors1(a, b + 1);
			} else if (a > 0) {
				initColors1(a - 1, b);
			}
		}
		
		initColors1(r, g);
		initColors1(g, b);

	}

	function colorFromAltitude(altitude) {

		if(altitude < 0) altitude = 0;

		return routeColors.length * altitude / 100 * 1000;

	}

	function exists(airplaneInfo) {

		for(var i = 0; i < markers.length; i++)
			if(markers[i].airplaneInfo.airplane == airplaneInfo.airplane)
				return i;

		return -1;

	}

	function createIcon(color, angle) {
		return {
		    path: "M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z",
		    fillColor: color,
		    fillOpacity: 1,
		    strokeWeight: 0,
		    scale: 1.0, 
		    rotation: angle, 
		  	origin: new google.maps.Point(0, 0),
		  	anchor: new google.maps.Point(10, 10),
		}
	}

	function doCreateMark (airplaneInfo) {

		icon = createIcon(defaultIconColor, parseInt(airplaneInfo.angle));

		var myLatlng = new google.maps.LatLng(airplaneInfo.latitude, airplaneInfo.longitude);
		var marker = new google.maps.Marker({
		    position: myLatlng,
		    title:"Clique para mais informações", 
		    icon: icon, 

		    // Custon property 
			airplaneInfo: airplaneInfo
		});

		google.maps.event.addListener(marker, 'click', function() {
			unselectMarker();
			selectMarker(marker);
		});

		return marker;

	} 

	function selectMarker(marker) {
		onMarkSelected(marker);
		doShowInfo(marker);
		marker.setIcon(createIcon(selectedIconColor, marker.airplaneInfo.angle));
		selectedMark = marker;
	}

	function unselectMarker() {
		if(selectedMark != null) {
			selectedMark.setIcon(createIcon(defaultIconColor, selectedMark.airplaneInfo.angle));
			selectedMark = null;
			onMarkUnselected();
		}
	}
		
	function addMarker(airplaneInfo) {
		var mark = doCreateMark(airplaneInfo);
		mark.setMap(map);
		markers.push(mark);
	}

	function updateMarker(airplaneInfo, index) {
		var mark = markers[index];
		mark.airplaneInfo = airplaneInfo;
		mark.setPosition(new google.maps.LatLng(airplaneInfo.latitude, airplaneInfo.longitude));
		
		if(selectedMark != null && selectedMark.airplaneInfo.airplane == airplaneInfo.airplane) {
			mark.setIcon(createIcon(selectedIconColor, airplaneInfo.angle));
		} else {
			mark.setIcon(createIcon(defaultIconColor, airplaneInfo.angle));
		}

	}

	function doShowInfo(marker) {

		doCloseInfo();

		airplaneInfo = marker.airplaneInfo;
		
		var windowWidth = $(window).width();

		var timestampToDate = function(t) {
			return DateFormat.format.prettyDate(new Date(t));
		}
		
		if(windowWidth <= 480) {

			var contentWindow = '' + 
				'<ul class="mdl-list">' + 
				'	<li class="">' + 
				'		<span class="">' + 
				'			<span class="mdl-typography--title">' + airplaneInfo.flight + '</span><br/>' + 
				'			<span class="mdl-typography--title">' + airplaneInfo.airline + " - " + airplaneInfo.airlineCountry + '</span><br/>' + 
				'			<span class="mdl-typography--subheading mdl-color-text--grey-700">Atualizado ' + timestampToDate(airplaneInfo.timestamp) + '</span>' + 
				'		</span>' + 
				'	</li>' + 
				'	<div class="rl-horizontal-line mdl-color--grey-300"></div>' + 
				'	<li class="">' + 
				'		<span class="">' + 
				'			<span class="mdl-typography--subheading mdl-color-text--grey-700">latitude</span><br/>' + 
				'			<span>' + airplaneInfo.latitude + '</span>' + 
				'		</span>' + 
				'	</li>' + 
				'	<li class="">' + 
				'		<span class="">' + 
				'			<span class="mdl-typography--subheading mdl-color-text--grey-700">longitude</span><br/>' + 
				'			<span>' + airplaneInfo.longitude + '</span>' + 
				'		</span>' + 
				'	</li>' + 
				'	<li class="">' + 
				'		<span class="">' + 
				'			<span class="mdl-typography--subheading mdl-color-text--grey-700">altitude</span><br/>' + 
				'			<span>' + airplaneInfo.altitude + ' ft / ' + parseFloat(parseInt(airplaneInfo.altitude * 30.48))/100 + ' m' + '</span>' + 
				'		</span>' + 
				'	</li>' + 
				'	<li class="">' + 
				'		<span class="">' + 
				'			<span class="mdl-typography--subheading mdl-color-text--grey-700">velocidade</span><br/>' + 
				'			<span>' + airplaneInfo.horizontalVelocity + ' knots / ' + parseFloat(parseInt(airplaneInfo.horizontalVelocity * 185.2))/100 + ' km/h' + '</span>' + 
				'		</span>' + 
				'	</li>' + 
				'</ul>';
	
			infowindow = new google.maps.InfoWindow({
				content: contentWindow
			});
	
			infowindow.open(map, marker);
			
			google.maps.event.addListener(infowindow, 'closeclick', function() {
				unselectMarker();
			});
			
		} else {
			
			$(".rl-map-drawer").addClass("is-visible");
			
			$(".rl-map-drawer__title").text(airplaneInfo.flight);
			$(".rl-map-drawer__subtitle").text(airplaneInfo.airline + " - " + airplaneInfo.airlineCountry);
			
			$(".rl-map-drawer__date").text("Atualizado " + timestampToDate(airplaneInfo.timestamp));
			$(".rl-map-drawer__lat").text(airplaneInfo.latitude);
			$(".rl-map-drawer__lng").text(airplaneInfo.longitude);
			$(".rl-map-drawer__alt").text(airplaneInfo.altitude + ' ft / ' + parseFloat(parseInt(airplaneInfo.altitude * 30.48))/100 + ' m');
			$(".rl-map-drawer__speed").text(airplaneInfo.horizontalVelocity + ' knots / ' + parseFloat(parseInt(airplaneInfo.horizontalVelocity * 185.2))/100 + ' km/h');
			
			$(".rl-map-drawer__close-button").click(function() {
				
				unselectMarker();
				doCloseInfo();
				
			});
		}

	}

	function doCloseInfo() {

		if(infowindow != null) {
			infowindow.close();
		}
		
		var drawer = $(".rl-map-drawer");
		drawer.removeClass("is-visible");
		
	}

	return {

		doInit : function() {

			// Modificando alguns atributos gráficos 
			var color = $(".mdl-layout-title").css("color");
			$(".rl-header-floating .mdl-layout__drawer-button .material-icons").css('color', color);
 			
			doInitColors();

 			rl_map.doInitMap();

		}, 

		doInitMap : function() {

			try {
				
				google;
				
			} catch (e) {
				
				rl_base.doShowSnackbar("Erro ao carregar mapa!");
								
				return;
				
			}
			
			if(!MAP_LOADED) {

				console.log("MAP LOADED!");
				MAP_LOADED = true;

			}
			
			if(MDL_LOADED && MAP_LOADED) {

				lat = rl_base.getURLParameter("lat");
				lng = rl_base.getURLParameter("lng");
				zoom = rl_base.getURLParameter("zoom");

				if(lat == null) lat = -14.950841; else lat = parseFloat(lat);
				if(lng == null) lng = -52.1189968; else lng = parseFloat(lng);
				if(zoom == null) zoom = 4; else zoom = parseFloat(zoom);

				var styleArray = [
					{
						"featureType": "road",
						"elementType": "geometry.stroke",
						"stylers": [
							{ "visibility": "off" }
						]
					},{
						"featureType": "road",
						"elementType": "geometry.fill",
						"stylers": [
							{ "color": "#90A4AE" }
						]
					}
				]

				map = new google.maps.Map(document.getElementById('map'), {

			    	center: {lat: lat, lng: lng},
			    	zoom: zoom, 
			    	mapTypeControl: false,
				    mapTypeControlOptions: {
				        style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
				        position: google.maps.ControlPosition.LEFT_TOP
				    },
				    zoomControl: true,
				    zoomControlOptions: {
				        position: google.maps.ControlPosition.RIGHT_CENTER
				    },
				    scaleControl: true,
				    streetViewControl: false,
				    fullscreenControl: false, 
				    styles: styleArray

			  	});

				var updateURLFunction = function() {

					var myObject = {
						lat : parseFloat(parseInt(map.getCenter().lat() * 100)/100.0),
						lng : parseFloat(parseInt(map.getCenter().lng() * 100)/100.0),
						zoom : parseFloat(parseInt(map.getZoom() * 100)/100.0)
					};

					var recursiveEncoded = $.param( myObject );
					var url = "?" + recursiveEncoded;
					window.history.pushState("", "", url);

				};

				map.addListener('center_changed', updateURLFunction);

			  	rl_map.doInitMapSearchBox();
			}

		}, 

		doInitMapSearchBox : function() {
			
			map.addListener('click', function() {
				$("#rl-place-searchbox").focusout();
			})

			// Create the search box and link it to the UI element.
			var input = document.getElementById('rl-place-searchbox');
			var searchBox = new google.maps.places.SearchBox(input);
			//map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

			// Bias the SearchBox results towards current map's viewport.
			map.addListener('bounds_changed', function() {
				searchBox.setBounds(map.getBounds());
			});

			var markers = [];
			// Listen for the event fired when the user selects a prediction and retrieve
			// more details for that place.
			searchBox.addListener('places_changed', function() {
				var places = searchBox.getPlaces();

				if (places.length == 0) {
					return;
				}

				// Clear out the old markers.
				markers.forEach(function(marker) {
				marker.setMap(null);
				});
				markers = [];

				// For each place, get the icon, name and location.
				var bounds = new google.maps.LatLngBounds();
				places.forEach(function(place) {
					var icon = {
						url: place.icon,
						size: new google.maps.Size(71, 71),
						origin: new google.maps.Point(0, 0),
						anchor: new google.maps.Point(17, 34),
						scaledSize: new google.maps.Size(25, 25)
					};

					// Create a marker for each place.
					markers.push(new google.maps.Marker({
						map: map,
						icon: icon,
						title: place.name,
						position: place.geometry.location
					}));

					if (place.geometry.viewport) {
						// Only geocodes have viewport.
						bounds.union(place.geometry.viewport);
					} else {
						bounds.extend(place.geometry.location);
					}
				});

				map.fitBounds(bounds);

			});

		}, 

		updateMarkerFromAirplaneInfo : function(airplaneInfo) {

			var index = exists(airplaneInfo);

			if(index == -1) {
				addMarker(airplaneInfo);
			} else {
				updateMarker(airplaneInfo, index);
			}

		}, 

		deleteMarker : function(airplaneInfo) {
			index = exists(airplaneInfo);

			if(index != -1) {
				markers[index].setMap(null);
				markers.splice(index, 1);
			}
		},  

		addLine : function (obs1, obs2) {
			var flightPlanCoordinates = [
				{lat: parseFloat(obs1.latitude), lng: parseFloat(obs1.longitude)},
				{lat: parseFloat(obs2.latitude), lng: parseFloat(obs2.longitude)}
			];
			var flightPath = new google.maps.Polyline({
				path: flightPlanCoordinates,
				geodesic: true,
				strokeColor: colorFromAltitude((obs1.altitude + obs2.altitude)/2),
				strokeOpacity: 1.0,
				strokeWeight: 2
			});

			flightPath.setMap(map);

			selectedMarkPolyLines.push(flightPath);
		}, 

		removeLine : function() {

			for(var i = 0; i < selectedMarkPolyLines.length; i++)
				selectedMarkPolyLines[i].setMap(null);

		}, 

		getMap : function() {
			return map;
		}, 

		setOnMarkSelected : function(callback) {
			onMarkSelected = callback;
		}, 

		setOnMarkUnselected : function(callback) {
			onMarkUnselected = callback;
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





/*
 * POLYFILL
 */

 (function() {

  var supportCustomEvent = window.CustomEvent;
  if (!supportCustomEvent || typeof supportCustomEvent == 'object') {
    supportCustomEvent = function CustomEvent(event, x) {
      x = x || {};
      var ev = document.createEvent('CustomEvent');
      ev.initCustomEvent(event, !!x.bubbles, !!x.cancelable, x.detail || null);
      return ev;
    };
    supportCustomEvent.prototype = window.Event.prototype;
  }

  /**
   * Finds the nearest <dialog> from the passed element.
   *
   * @param {Element} el to search from
   * @return {HTMLDialogElement} dialog found
   */
  function findNearestDialog(el) {
    while (el) {
      if (el.nodeName.toUpperCase() == 'DIALOG') {
        return /** @type {HTMLDialogElement} */ (el);
      }
      el = el.parentElement;
    }
    return null;
  }

  /**
   * Blur the specified element, as long as it's not the HTML body element.
   * This works around an IE9/10 bug - blurring the body causes Windows to
   * blur the whole application.
   *
   * @param {Element} el to blur
   */
  function safeBlur(el) {
    if (el && el.blur && el != document.body) {
      el.blur();
    }
  }

  /**
   * @param {!NodeList} nodeList to search
   * @param {Node} node to find
   * @return {boolean} whether node is inside nodeList
   */
  function inNodeList(nodeList, node) {
    for (var i = 0; i < nodeList.length; ++i) {
      if (nodeList[i] == node) {
        return true;
      }
    }
    return false;
  }

  /**
   * @param {!HTMLDialogElement} dialog to upgrade
   * @constructor
   */
  function dialogPolyfillInfo(dialog) {
    this.dialog_ = dialog;
    this.replacedStyleTop_ = false;
    this.openAsModal_ = false;

    // Set a11y role. Browsers that support dialog implicitly know this already.
    if (!dialog.hasAttribute('role')) {
      dialog.setAttribute('role', 'dialog');
    }

    dialog.show = this.show.bind(this);
    dialog.showModal = this.showModal.bind(this);
    dialog.close = this.close.bind(this);

    if (!('returnValue' in dialog)) {
      dialog.returnValue = '';
    }

    this.maybeHideModal = this.maybeHideModal.bind(this);
    if ('MutationObserver' in window) {
      // IE11+, most other browsers.
      var mo = new MutationObserver(this.maybeHideModal);
      mo.observe(dialog, { attributes: true, attributeFilter: ['open'] });
    } else {
      dialog.addEventListener('DOMAttrModified', this.maybeHideModal);
    }
    // Note that the DOM is observed inside DialogManager while any dialog
    // is being displayed as a modal, to catch modal removal from the DOM.

    Object.defineProperty(dialog, 'open', {
      set: this.setOpen.bind(this),
      get: dialog.hasAttribute.bind(dialog, 'open')
    });

    this.backdrop_ = document.createElement('div');
    this.backdrop_.className = 'backdrop';
    this.backdropClick_ = this.backdropClick_.bind(this);
  }

  dialogPolyfillInfo.prototype = {

    get dialog() {
      return this.dialog_;
    },

    /**
     * Maybe remove this dialog from the modal top layer. This is called when
     * a modal dialog may no longer be tenable, e.g., when the dialog is no
     * longer open or is no longer part of the DOM.
     */
    maybeHideModal: function() {
      if (!this.openAsModal_) { return; }
      if (this.dialog_.hasAttribute('open') &&
          document.body.contains(this.dialog_)) { return; }

      this.openAsModal_ = false;
      this.dialog_.style.zIndex = '';

      // This won't match the native <dialog> exactly because if the user set
      // top on a centered polyfill dialog, that top gets thrown away when the
      // dialog is closed. Not sure it's possible to polyfill this perfectly.
      if (this.replacedStyleTop_) {
        this.dialog_.style.top = '';
        this.replacedStyleTop_ = false;
      }

      // Optimistically clear the modal part of this <dialog>.
      this.backdrop_.removeEventListener('click', this.backdropClick_);
      if (this.backdrop_.parentElement) {
        this.backdrop_.parentElement.removeChild(this.backdrop_);
      }
      dialogPolyfill.dm.removeDialog(this);
    },

    /**
     * @param {boolean} value whether to open or close this dialog
     */
    setOpen: function(value) {
      if (value) {
        this.dialog_.hasAttribute('open') || this.dialog_.setAttribute('open', '');
      } else {
        this.dialog_.removeAttribute('open');
        this.maybeHideModal();  // nb. redundant with MutationObserver
      }
    },

    /**
     * Handles clicks on the fake .backdrop element, redirecting them as if
     * they were on the dialog itself.
     *
     * @param {!Event} e to redirect
     */
    backdropClick_: function(e) {
      var redirectedEvent = document.createEvent('MouseEvents');
      redirectedEvent.initMouseEvent(e.type, e.bubbles, e.cancelable, window,
          e.detail, e.screenX, e.screenY, e.clientX, e.clientY, e.ctrlKey,
          e.altKey, e.shiftKey, e.metaKey, e.button, e.relatedTarget);
      this.dialog_.dispatchEvent(redirectedEvent);
      e.stopPropagation();
    },

    /**
     * Sets the zIndex for the backdrop and dialog.
     *
     * @param {number} backdropZ
     * @param {number} dialogZ
     */
    updateZIndex: function(backdropZ, dialogZ) {
      this.backdrop_.style.zIndex = backdropZ;
      this.dialog_.style.zIndex = dialogZ;
    },

    /**
     * Shows the dialog. This is idempotent and will always succeed.
     */
    show: function() {
      this.setOpen(true);
    },

    /**
     * Show this dialog modally.
     */
    showModal: function() {
      if (this.dialog_.hasAttribute('open')) {
        throw new Error('Failed to execute \'showModal\' on dialog: The element is already open, and therefore cannot be opened modally.');
      }
      if (!document.body.contains(this.dialog_)) {
        throw new Error('Failed to execute \'showModal\' on dialog: The element is not in a Document.');
      }
      if (!dialogPolyfill.dm.pushDialog(this)) {
        throw new Error('Failed to execute \'showModal\' on dialog: There are too many open modal dialogs.');
      }
      this.show();
      this.openAsModal_ = true;

      // Optionally center vertically, relative to the current viewport.
      if (dialogPolyfill.needsCentering(this.dialog_)) {
        dialogPolyfill.reposition(this.dialog_);
        this.replacedStyleTop_ = true;
      } else {
        this.replacedStyleTop_ = false;
      }

      // Insert backdrop.
      this.backdrop_.addEventListener('click', this.backdropClick_);
      this.dialog_.parentNode.insertBefore(this.backdrop_,
          this.dialog_.nextSibling);

      // Find element with `autofocus` attribute or first form control.
      var target = this.dialog_.querySelector('[autofocus]:not([disabled])');
      if (!target) {
        // TODO: technically this is 'any focusable area'
        var opts = ['button', 'input', 'keygen', 'select', 'textarea'];
        var query = opts.map(function(el) {
          return el + ':not([disabled])';
        }).join(', ');
        target = this.dialog_.querySelector(query);
      }
      safeBlur(document.activeElement);
      target && target.focus();
    },

    /**
     * Closes this HTMLDialogElement. This is optional vs clearing the open
     * attribute, however this fires a 'close' event.
     *
     * @param {string=} opt_returnValue to use as the returnValue
     */
    close: function(opt_returnValue) {
      if (!this.dialog_.hasAttribute('open')) {
        throw new Error('Failed to execute \'close\' on dialog: The element does not have an \'open\' attribute, and therefore cannot be closed.');
      }
      this.setOpen(false);

      // Leave returnValue untouched in case it was set directly on the element
      if (opt_returnValue !== undefined) {
        this.dialog_.returnValue = opt_returnValue;
      }

      // Triggering "close" event for any attached listeners on the <dialog>.
      var closeEvent = new supportCustomEvent('close', {
        bubbles: false,
        cancelable: false
      });
      this.dialog_.dispatchEvent(closeEvent);
    }

  };

  var dialogPolyfill = {};

  dialogPolyfill.reposition = function(element) {
    var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
    var topValue = scrollTop + (window.innerHeight - element.offsetHeight) / 2;
    element.style.top = Math.max(scrollTop, topValue) + 'px';
  };

  dialogPolyfill.isInlinePositionSetByStylesheet = function(element) {
    for (var i = 0; i < document.styleSheets.length; ++i) {
      var styleSheet = document.styleSheets[i];
      var cssRules = null;
      // Some browsers throw on cssRules.
      try {
        cssRules = styleSheet.cssRules;
      } catch (e) {}
      if (!cssRules)
        continue;
      for (var j = 0; j < cssRules.length; ++j) {
        var rule = cssRules[j];
        var selectedNodes = null;
        // Ignore errors on invalid selector texts.
        try {
          selectedNodes = document.querySelectorAll(rule.selectorText);
        } catch(e) {}
        if (!selectedNodes || !inNodeList(selectedNodes, element))
          continue;
        var cssTop = rule.style.getPropertyValue('top');
        var cssBottom = rule.style.getPropertyValue('bottom');
        if ((cssTop && cssTop != 'auto') || (cssBottom && cssBottom != 'auto'))
          return true;
      }
    }
    return false;
  };

  dialogPolyfill.needsCentering = function(dialog) {
    var computedStyle = window.getComputedStyle(dialog);
    if (computedStyle.position != 'absolute') {
      return false;
    }

    // We must determine whether the top/bottom specified value is non-auto.  In
    // WebKit/Blink, checking computedStyle.top == 'auto' is sufficient, but
    // Firefox returns the used value. So we do this crazy thing instead: check
    // the inline style and then go through CSS rules.
    if ((dialog.style.top != 'auto' && dialog.style.top != '') ||
        (dialog.style.bottom != 'auto' && dialog.style.bottom != ''))
      return false;
    return !dialogPolyfill.isInlinePositionSetByStylesheet(dialog);
  };

  /**
   * @param {!Element} element to force upgrade
   */
  dialogPolyfill.forceRegisterDialog = function(element) {
    if (element.showModal) {
      console.warn('This browser already supports <dialog>, the polyfill ' +
          'may not work correctly', element);
    }
    if (element.nodeName.toUpperCase() != 'DIALOG') {
      throw new Error('Failed to register dialog: The element is not a dialog.');
    }
    new dialogPolyfillInfo(/** @type {!HTMLDialogElement} */ (element));
  };

  /**
   * @param {!Element} element to upgrade
   */
  dialogPolyfill.registerDialog = function(element) {
    if (element.showModal) {
      console.warn('Can\'t upgrade <dialog>: already supported', element);
    } else {
      dialogPolyfill.forceRegisterDialog(element);
    }
  };

  /**
   * @constructor
   */
  dialogPolyfill.DialogManager = function() {
    /** @type {!Array<!dialogPolyfillInfo>} */
    this.pendingDialogStack = [];

    // The overlay is used to simulate how a modal dialog blocks the document.
    // The blocking dialog is positioned on top of the overlay, and the rest of
    // the dialogs on the pending dialog stack are positioned below it. In the
    // actual implementation, the modal dialog stacking is controlled by the
    // top layer, where z-index has no effect.
    this.overlay = document.createElement('div');
    this.overlay.className = '_dialog_overlay';
    this.overlay.addEventListener('click', function(e) {
      e.stopPropagation();
    });

    this.handleKey_ = this.handleKey_.bind(this);
    this.handleFocus_ = this.handleFocus_.bind(this);
    this.handleRemove_ = this.handleRemove_.bind(this);

    this.zIndexLow_ = 100000;
    this.zIndexHigh_ = 100000 + 150;
  };

  /**
   * @return {Element} the top HTML dialog element, if any
   */
  dialogPolyfill.DialogManager.prototype.topDialogElement = function() {
    if (this.pendingDialogStack.length) {
      var t = this.pendingDialogStack[this.pendingDialogStack.length - 1];
      return t.dialog;
    }
    return null;
  };

  /**
   * Called on the first modal dialog being shown. Adds the overlay and related
   * handlers.
   */
  dialogPolyfill.DialogManager.prototype.blockDocument = function() {
    document.body.appendChild(this.overlay);
    document.body.addEventListener('focus', this.handleFocus_, true);
    document.addEventListener('keydown', this.handleKey_);
    document.addEventListener('DOMNodeRemoved', this.handleRemove_);
  };

  /**
   * Called on the first modal dialog being removed, i.e., when no more modal
   * dialogs are visible.
   */
  dialogPolyfill.DialogManager.prototype.unblockDocument = function() {
    document.body.removeChild(this.overlay);
    document.body.removeEventListener('focus', this.handleFocus_, true);
    document.removeEventListener('keydown', this.handleKey_);
    document.removeEventListener('DOMNodeRemoved', this.handleRemove_);
  };

  dialogPolyfill.DialogManager.prototype.updateStacking = function() {
    var zIndex = this.zIndexLow_;

    for (var i = 0; i < this.pendingDialogStack.length; i++) {
      if (i == this.pendingDialogStack.length - 1) {
        this.overlay.style.zIndex = zIndex++;
      }
      this.pendingDialogStack[i].updateZIndex(zIndex++, zIndex++);
    }
  };

  dialogPolyfill.DialogManager.prototype.handleFocus_ = function(event) {
    var candidate = findNearestDialog(/** @type {Element} */ (event.target));
    if (candidate != this.topDialogElement()) {
      event.preventDefault();
      event.stopPropagation();
      safeBlur(/** @type {Element} */ (event.target));
      // TODO: Focus on the browser chrome (aka document) or the dialog itself
      // depending on the tab direction.
      return false;
    }
  };

  dialogPolyfill.DialogManager.prototype.handleKey_ = function(event) {
    if (event.keyCode == 27) {
      event.preventDefault();
      event.stopPropagation();
      var cancelEvent = new supportCustomEvent('cancel', {
        bubbles: false,
        cancelable: true
      });
      var dialog = this.topDialogElement();
      if (dialog.dispatchEvent(cancelEvent)) {
        dialog.close();
      }
    }
  };

  dialogPolyfill.DialogManager.prototype.handleRemove_ = function(event) {
    if (event.target.nodeName.toUpperCase() != 'DIALOG') { return; }

    var dialog = /** @type {HTMLDialogElement} */ (event.target);
    if (!dialog.open) { return; }

    // Find a dialogPolyfillInfo which matches the removed <dialog>.
    this.pendingDialogStack.some(function(dpi) {
      if (dpi.dialog == dialog) {
        // This call will clear the dialogPolyfillInfo on this DialogManager
        // as a side effect.
        dpi.maybeHideModal();
        return true;
      }
    });
  };

  /**
   * @param {!dialogPolyfillInfo} dpi
   * @return {boolean} whether the dialog was allowed
   */
  dialogPolyfill.DialogManager.prototype.pushDialog = function(dpi) {
    var allowed = (this.zIndexHigh_ - this.zIndexLow_) / 2 - 1;
    if (this.pendingDialogStack.length >= allowed) {
      return false;
    }
    this.pendingDialogStack.push(dpi);
    if (this.pendingDialogStack.length == 1) {
      this.blockDocument();
    }
    this.updateStacking();
    return true;
  };

  /**
   * @param {dialogPolyfillInfo} dpi
   */
  dialogPolyfill.DialogManager.prototype.removeDialog = function(dpi) {
    var index = this.pendingDialogStack.indexOf(dpi);
    if (index == -1) { return; }

    this.pendingDialogStack.splice(index, 1);
    this.updateStacking();
    if (this.pendingDialogStack.length == 0) {
      this.unblockDocument();
    }
  };

  dialogPolyfill.dm = new dialogPolyfill.DialogManager();

  /**
   * Global form 'dialog' method handler. Closes a dialog correctly on submit
   * and possibly sets its return value.
   */
  document.addEventListener('submit', function(ev) {
    var target = ev.target;
    if (!target || !target.hasAttribute('method')) { return; }
    if (target.getAttribute('method').toLowerCase() != 'dialog') { return; }
    ev.preventDefault();

    var dialog = findNearestDialog(/** @type {Element} */ (ev.target));
    if (!dialog) { return; }

    // FIXME: The original event doesn't contain the element used to submit the
    // form (if any). Look in some possible places.
    var returnValue;
    var cands = [document.activeElement, ev.explicitOriginalTarget];
    var els = ['BUTTON', 'INPUT'];
    cands.some(function(cand) {
      if (cand && cand.form == ev.target && els.indexOf(cand.nodeName.toUpperCase()) != -1) {
        returnValue = cand.value;
        return true;
      }
    });
    dialog.close(returnValue);
  }, true);

  dialogPolyfill['forceRegisterDialog'] = dialogPolyfill.forceRegisterDialog;
  dialogPolyfill['registerDialog'] = dialogPolyfill.registerDialog;

  if (typeof module === 'object' && typeof module['exports'] === 'object') {
    // CommonJS support
    module['exports'] = dialogPolyfill;
  } else if (typeof define === 'function' && 'amd' in define) {
    // AMD support
    define(function() { return dialogPolyfill; });
  } else {
    // all others
    window['dialogPolyfill'] = dialogPolyfill;
  }
})();
