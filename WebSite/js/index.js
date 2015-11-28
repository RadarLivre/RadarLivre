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


// Url of the server
//var wsUri = "ws://" + document.location.host + ":9999/Radar-Livre/websocket";
var wsUri = "ws://www.radarlivre.com:9999/Radar-Livre/websocket";
var webSocket;


// User to controll popups
var hasShow = false;


// List of current airplanes markers
var airplaneMarkers = [];


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

	map = new google.maps.Map(document.getElementById('map-canvas'), {
		center: {lat: -4.850440, lng: -39.572829},
		streetViewControl: false,
		zoom: 7, 
		styles: styleArray, 
		mapTypeControl: true,
	    mapTypeControlOptions: {
	    	style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
	    	position: google.maps.ControlPosition.RIGHT_TOP,
	    	mapTypeIds: [
	        	google.maps.MapTypeId.ROADMAP,
	        	google.maps.MapTypeId.TERRAIN
	    	]
	    }, 
	    zoomControl: true,
	    zoomControlOptions: {
	        position: google.maps.ControlPosition.RIGHT_CENTER
	    },
	    scaleControl: true

	});	


}

function doInitInterface() {
	// ...
}

// The point contais the params: lat, lon and alt
function doMakeRoute(points) {
	smoothTheWay(
		points,
		function(smoothPoints){
			for(var i = 0; i < smoothPoints.length - 1; i++) {
				var p1 = smoothPoints[i];
				var p2 = smoothPoints[i + 1];
				var currentPoints = [
					{lat: p1.lat, lng: p1.lng}, 
					{lat: p2.lat, lng: p2.lng} 
				];
			  	var flightPath = new google.maps.Polyline({
				    path: currentPoints,
				    geodesic: true,
				    strokeColor: getColorFromAlt(p1.alt),
				    strokeOpacity: 1.0,
				    strokeWeight: 2
			  	});

				flightPath.setMap(map);
				currentRoutePolyLine.push(flightPath);
			}

		}, 
		10.0
	);
	console.log("Route done");
}

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
		showError("A conexão com o servidor foi perdida!", 5000, function() {});
		hasShow = true;
	}
}

function onWebSocketMessage(event) {
	var data = event.data;

	if(data.search(RESPONSE_REQUEST_GET_AIRPLANES) != -1) {
		data = data.replace(RESPONSE_REQUEST_GET_AIRPLANES + ":", "");
		if(data != "None") {
			airplanes = JSON.parse(data);
			onAirplanesReceived(airplanes);
		}
	} else if (data.search(RESPONSE_REQUEST_GET_ROUTE) != -1) {
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

function doShowLoading() {
	document.getElementById("loading-view").style.display = 'block';
}

function doHideLoading() {
	document.getElementById("loading-view").style.display = 'none';
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
	    map: map, 

	    // Custon property
	    hex: airplaneInfo.hex, 
		icao: airplaneInfo.icao, 
		lat: airplaneInfo.latitude, 
		lon: airplaneInfo.longitude,  
		alt: airplaneInfo.altitude, 
		climb: airplaneInfo.altitude, 
		head: airplaneInfo.head, 
		velocity: airplaneInfo.velocidadegnd, 
		utf: airplaneInfo.utf
	});

	google.maps.event.addListener(marker, 'click', function() {
		doShowRouteTo(marker);
	});

	return marker;
}

function doInitGetAirplaneLoop() {
	setInterval(doUpdateAirpoits, DEF_INTERVAL_UPDATE_AIRPLANES);
}

function doUpdateAirpoits() {
	console.log("send: " + REQUEST_GET_AIRPLANES);
	webSocket.send(REQUEST_GET_AIRPLANES);
}

function onAirplanesReceived(airplanes) {
	console.log("Updating airplanes: " + airplanes.length);
	var exists = function(air) {
		for(i = 0; i < airplaneMarkers.length; i++)
			if(airplaneMarkers[i].hex == air.hex)
				return i;
		return -1;
	}	
	for(i = 0; i < airplanes.length; i++) {
		air = airplanes[i];
		var index = exists(air);

		if(index != -1) {
			var marker = airplaneMarkers[index];
			marker.setPosition(new google.maps.LatLng(air.latitude, air.longitude))
		} else {
			var marker = doCreateMarker(air);
			marker.setMap(map);
			airplaneMarkers.push(marker);
		}
	}
}

function doShowRouteTo(marker) {
	webSocket.send(REQUEST_GET_ROUTE + "(" + marker.hex + ")");
}

function onRouteReceived(mapPoints) {
	points = [];
	for(key in mapPoints) {
		mapPoint = mapPoints[key];
		points.push({
			lat: mapPoint.latitude, lng: mapPoint.longitude, alt: mapPoint.altitude
		});
	}

	doMakeRoute(points);
}

