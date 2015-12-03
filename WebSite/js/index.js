// Handle the framework load event
componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {
	doInitMap();  		
	doInitInterface();  
    doInitWebSocket();	
    doInitGetAirplaneLoop();	
});


// Protocol to talk with service
var REQUEST_GET_AIRPLANES = "GET_AIRPLANES";
var REQUEST_GET_AIRPORTS = "GET_AIRPORTS";
var REQUEST_GET_ROUTE = "GET_ROUTE";
var REQUEST_SEARCH = "SEARCH";
var RESPONSE_REQUEST_GET_AIRPLANES = "GET_AIRPLANES_RESPONSE";
var RESPONSE_REQUEST_GET_AIRPORTS = "GET_AIRPORTS_RESPONSE";
var RESPONSE_REQUEST_GET_ROUTE = "GET_ROUTE_RESPONSE";
var RESPONSE_REQUEST_SEARCH = "SEARCH_RESPONSE";


// Interval to update airplane list
var DEF_INTERVAL_UPDATE_AIRPLANES = 3000;


// This variable contains a google.maps.Map object
map = null;


// This is the current route object
currentRoutePolyLine = []
currentHex = ""


// Url of the server
// var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";
var wsUri = "ws://www.radarlivre.com:9999/Radar-Livre/websocket";
var webSocket;


// User to controll popups
var hasShow = false;


// List of current airplanes markers
var airplaneMarkers = [];

function getParam(param) {
	var url = window.location.search.substring(1);

	var vars = url.split('&');
	for (var i=0; i<vars.length; i++) {
	    var pair = vars[i].split("=");
	    if (pair[0] == param) {
	    	return pair[1];
	    }
	}

	return null;
} 

// Initializing google maps view

function doInitMap() {

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
				{ "color": md_blue_grey_300 }
			]
		}
	]

	lat = getParam("lat");
	lng = getParam("lng");
	zoom = getParam("zoom");

	if(lat == null) lat = -14.950841; else lat = parseFloat(lat);
	if(lng == null) lng = -52.1189968; else lng = parseFloat(lng);
	if(zoom == null) zoom = 4; else zoom = parseFloat(zoom);

	map = new google.maps.Map(document.getElementById('map-canvas'), {
		center: {lat: lat, lng: lng},
		streetViewControl: false,
		zoom: zoom, 
		styles: styleArray, 
		mapTypeControl: true,
	    mapTypeControlOptions: {
	    	style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
	    	position: google.maps.ControlPosition.TOP_RIGHT,
	    	mapTypeIds: [
	        	google.maps.MapTypeId.ROADMAP,
	        	google.maps.MapTypeId.TERRAIN
	    	]
	    }, 
	    zoomControl: true,
	    zoomControlOptions: {
	        position: google.maps.ControlPosition.RIGHT_CENTER
	    },
	    scaleControl: true, 
	    overviewMapControl: true
	});	

	map.addListener('click', function() {
	    doRemoveCurrentRoute();
	    doHideAirplaneInfo();
	})

	map.addListener('center_changed', function() {
		var lat = parseFloat(parseInt(map.getCenter().lat() * 100)/100.0);
		var lng = parseFloat(parseInt(map.getCenter().lng() * 100)/100.0);
		var zoom = parseFloat(parseInt(map.getZoom() * 100)/100.0);

		window.history.pushState("", "", "?lat=" + lat + "&lng=" + lng + "&zoom=" + zoom);
	})

}

function doInitInterface() {
	// Create the search box and link it to the UI element.
	var input = document.getElementById('pac-input');
	var inputContent = document.getElementById('search-box-container');
	var searchBox = new google.maps.places.SearchBox(input);
	map.controls[google.maps.ControlPosition.TOP_RIGHT].push(inputContent);

	// Bias the SearchBox results towards current map's viewport.
	map.addListener('bounds_changed', function() {
		searchBox.setBounds(map.getBounds());
	});

	var markers = [];
	// Listen for the event fired when the user selects a prediction and retrieve
	// more details for that place.
	searchBox.addListener('places_changed', function() {
		var places = searchBox.getPlaces();

		// Clear out the old markers.
		markers.forEach(function(marker) {
			marker.setMap(null);
		});

		markers = [];

		if (places.length == 0) {
			return;
		}

		// For each place, get the icon, name and location.
		var bounds = new google.maps.LatLngBounds();
		places.forEach(function(place) {
			// Create a marker for each place.
			markers.push(new google.maps.Marker({
				map: map,
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
}



// Initializing the web socket object

function doInitWebSocket() {
	try{
		webSocket = new WebSocket(wsUri);
		webSocket.onopen = function(event) { onWebSocketOpen(event); };
		webSocket.onclose = function(event) { onWebSocketClose(event); };
		webSocket.onerror = function(event) { onWebSocketError(event) };
		webSocket.onmessage = function(event) { onWebSocketMessage(event); };
	}
	catch(err){
		onWebSocketError(err);
	}	
}

function onWebSocketOpen(event) {
	console.log("WebSocket openned!");

	doHideLoading();
	hasShow = false;
}

function onWebSocketClose(event) {
	console.log("WebSocket closed!");

	doShowLoading();
	doReconectWebSocket();
}

function onWebSocketError(event) {
	console.log("WebSocket error!");

	doShowLoading();
	if(!hasShow) {
		showError("Sem conexão com o servidor!", 5000, function() {});
		hasShow = true;
	}
}

function onWebSocketMessage(event) {
	var data = event.data;

	if(data.search(RESPONSE_REQUEST_GET_AIRPLANES) != -1) {
		console.log("Receive airplanes: " + data);
		data = data.replace(RESPONSE_REQUEST_GET_AIRPLANES + ":", "");
		if(data != "None") {
			airplanes = JSON.parse(data);
			onAirplanesReceived(airplanes);
		}
	} else if (data.search(RESPONSE_REQUEST_GET_ROUTE) != -1) {
		console.log("Receive route: " + data);
		data = data.replace(RESPONSE_REQUEST_GET_ROUTE + ":", "");
		if(data != "None") {
			mapPoints = JSON.parse(data);
			onRouteReceived(mapPoints);
		}
	}
}

function doReconectWebSocket() {
	setTimeout(function() {
		doInitWebSocket();
	}, 3000);
}



// Handling updates

function doInitGetAirplaneLoop() {
	setInterval(doUpdateAirplains, DEF_INTERVAL_UPDATE_AIRPLANES);
}

function doUpdateAirplains() {
	console.log("send: " + REQUEST_GET_AIRPLANES);
	webSocket.send(REQUEST_GET_AIRPLANES);

	if(currentHex != "")
		doShowRouteTo(currentHex);
}

function onAirplanesReceived(airplanes) {
	console.log("Updating airplanes: " + airplanes.length);
	var exists = function(air, list) {
		for(var a = 0; a < list.length; a++)
			if(list[a].hex == air.hex)
				return a;
		return -1;
	}

	for(var b = 0; b < airplanes.length; b++) {
		air = airplanes[b];
		var index = exists(air, airplaneMarkers);

		if(index != -1) {
			var marker = airplaneMarkers[index];
			marker.setPosition(new google.maps.LatLng(air.latitude, air.longitude))
		} else {
			var marker = doCreateMarker(air);
			marker.setMap(map);
			airplaneMarkers.push(marker);
		}
	}

	for(var c = 0; c < airplaneMarkers.length; c++) {
		var airplane = airplaneMarkers[c];
		var index = exists(airplane, airplanes);
		if(index == -1) {
			airplane.setMap(null);
			airplaneMarkers.splice(index, 1);
			if(airplane.hex == currentHex)
				doRemoveCurrentRoute();

			c--;
		}
	}

}

function doShowRouteTo(hex) {
	currentHex = hex;
	console.log("send: " + REQUEST_GET_ROUTE + "(" + hex + ")");
	webSocket.send(REQUEST_GET_ROUTE + "(" + hex + ")");
}

function onRouteReceived(mapPoints) {
	if(currentHex != ""
		&& mapPoints.length > 0
		&& mapPoints[0].hex == currentHex) {
		
		points = [];
		for(key in mapPoints) {
			mapPoint = mapPoints[key];
			points.push({
				lat: mapPoint.latitude, lng: mapPoint.longitude, alt: mapPoint.altitude
			});
		}

		doMakeRoute(points);

	}
}



// Handling interface events

function doShowLoading() {
	document.getElementById("loading-view").style.display = 'block';
}

function doHideLoading() {
	document.getElementById("loading-view").style.display = 'none';
}

function doShowAirplaneInfo(airplaneInfo) {
	drawer = document.getElementById("drawer-info");
	if(!drawer.classList.contains("is-visible")) {
		drawer.classList.add("is-visible");
		drawer.classList.add("drawer");
	}

	airLineData = identifyAirLineInformations(airplaneInfo.id);

	if(airLineData != null) {

		flightId = document.getElementById("label-flight-id");
		flightId.innerHTML = airLineData.idVoo + "/" + airplaneInfo.id;

		airline = document.getElementById("label-airline");
		airline.innerHTML = airLineData.airline + " - " + airLineData.country;

	} else {

		flightId = document.getElementById("label-flight-id");
		flightId.innerHTML = "Sem identificação";

	}
	
	lat = document.getElementById("label-lat");
	lat.innerHTML = airplaneInfo.latitude;
	
	lng = document.getElementById("label-lng");
	lng.innerHTML = airplaneInfo.longitude;
	
	alt = document.getElementById("label-alt");
	alt.innerHTML = airplaneInfo.altitude + " ft <br/> " + parseFloat(parseInt(airplaneInfo.altitude * 30.48))/100 + " m";
	
	spe = document.getElementById("label-spe");
	spe.innerHTML = airplaneInfo.velocidadegnd + " knots <br/> " + parseFloat(parseInt(airplaneInfo.velocidadegnd * 185.2))/100 + " km/h";
}

function doHideAirplaneInfo() {
	drawer = document.getElementById("drawer-info");
	if(drawer.classList.contains("is-visible")) {
		drawer.classList.remove("is-visible");
		drawer.classList.remove("drawer");
	}
}

function doMakeRoute(points) {
	smoothTheWay(
		points,
		function(smoothPoints){
			for(var i = 0; i < smoothPoints.length - 1; i++) {
				var p1 = smoothPoints[i];
				var p2 = smoothPoints[i + 1];

				if(!existsPoly(p1)) {
					var currentPoints = [
						{lat: p1.lat, lng: p1.lng}, 
						{lat: p2.lat, lng: p2.lng} 
					];
				  	var flightPath = new google.maps.Polyline({
					    path: currentPoints,
					    geodesic: true,
					    strokeColor: getColorFromAlt(p1.alt),
					    strokeOpacity: 1.0,
					    strokeWeight: 2, 
					    custonId: "" + p1.lat + ":" + p2.lat
				  	});

					flightPath.setMap(map);
					currentRoutePolyLine.push(flightPath);
				}
			}

		}, 
		3.0
	);
	console.log("Route done");
}

function existsPoly(p1) {
	for(var i = 0; i < currentRoutePolyLine.length; i++) {
		line = currentRoutePolyLine[i]
		var custonId = "" + p1.lat + ":" + p1.lng;
		if(line.custonId == custonId)
			return true;
	}
	return false;
}

function doRemoveCurrentRoute() {
	currentHex = "";
	for(var i = 0; i < currentRoutePolyLine.length; i++) {
		currentRoutePolyLine[i].setMap(null);
	}

	currentRoutePolyLine = [];
}

function doCreateMarker(airplaneInfo) {

	var icon = {
	    path: "M21,16V14L13,9V3.5A1.5,1.5 0 0,0 11.5,2A1.5,1.5 0 0,0 10,3.5V9L2,14V16L10,13.5V19L8,20.5V22L11.5,21L15,22V20.5L13,19V13.5L21,16Z",
	    fillColor: md_indigo_900,
	    fillOpacity: 1,
	    strokeWeight: 0,
	    scale: 1.0, 
	    rotation: parseInt(airplaneInfo.head), 
	  	origin: new google.maps.Point(0, 0),
	  	anchor: new google.maps.Point(10, 10),
	}

	var myLatlng = new google.maps.LatLng(airplaneInfo.latitude, airplaneInfo.longitude);
	var marker = new google.maps.Marker({
	    position: myLatlng,
	    title:"Clique para mais informações", 
	    icon: icon, 

	    // Custon property
	    hex: airplaneInfo.hex, 
		icao: airplaneInfo.icao, 
		lat: airplaneInfo.latitude, 
		lon: airplaneInfo.longitude,  
		alt: airplaneInfo.altitude, 
		climb: airplaneInfo.altitude, 
		head: airplaneInfo.head, 
		velocity: airplaneInfo.velocidadegnd, 
		utf: airplaneInfo.utf, 
		timestamp: airplaneInfo.timestamp
	});

	google.maps.event.addListener(marker, 'click', function() {
		doRemoveCurrentRoute();
		doShowRouteTo(marker.hex);
		doShowAirplaneInfo(airplaneInfo);
		map.panTo(marker.getPosition());
	});

	return marker;
}
