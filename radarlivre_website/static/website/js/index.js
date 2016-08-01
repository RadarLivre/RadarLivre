MDL_LOADED = false;
MAP_LOADED = false;

componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {
	
    MDL_LOADED = true;
    console.info("MDL Loaded");
    if(MAP_LOADED)
        initMap();

});

function initMap() {
    
    MAP_LOADED = true;
    
    if(!MDL_LOADED) return;
    console.info("MAP Loaded");
    
    var selectedMark = null;
    var routeColors = [];
    initColors(routeColors);
    
    var getAirplanes = function() {
        var map = maps_api.getMap();
        radarlivre_api.doGetAirplaneInfos(
            1000000000000,
            {
                top: map.getBounds().getNorthEast().lat(), 
                bottom: map.getBounds().getSouthWest().lat(), 
                left: map.getBounds().getSouthWest().lng(), 
                right: map.getBounds().getNorthEast().lng()
            }, 
            function(data) {
                console.log("Aviões recebidos: " + data.length);
                for(k in data) {
                    a = data[k];
                    maps_api.doSetMarker({
                        id: a.airplane, 
                        data: { dataType: "airplane", data: a}, 
                        position: new google.maps.LatLng(a.latitude, a.longitude), 
                        icon: createIcon(
                            "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z", 
                            "#263238", a.angle, 10, 10
                        )
                    });
                }
            }, 
            function() {}
        );
    }
    
    var getRoute = function(marker) {
        radarlivre_api.doGetAirplaneRoute(
            marker.id, 0, 
            function(data) {
                console.log("Recebida rota para: " + marker.id + ", length: " + data.length);
                for(var i = 0; i < data.length; i++)
                    if(i < data.length - 1)
                        maps_api.doSetPolyLine(
                            marker,
                            {
                                id: data[i].timestamp, 
                                path: [
                                    {lat: parseFloat(data[i].latitude), lng: parseFloat(data[i].longitude)}, 
                                    {lat: parseFloat(data[i+1].latitude), lng: parseFloat(data[i+1].longitude)}
                                ], 
                                color: colorFromAltitude(data[i].altitude, routeColors)
                            }
                        )
            }, 
            function() {}
        );
    }

    var getContrib = function() {
        radarlivre_api.doGetContribs(
            100000000000000, 
            function(data) {
                console.log("Contribuintes recebidos: " + data.length);
                data.map(function(c) {
                    maps_api.doSetMarker({
                        id: c.ip,
                        data: { dataType: "contrib", data: c }, 
                        dataType: "contrib", 
                        position: new google.maps.LatLng(c.latitude, c.longitude), 
                        icon: createIcon(
                            "M12 5c-3.87 0-7 3.13-7 7h2c0-2.76 2.24-5 5-5s5 2.24 5 5h2c0-3.87-3.13-7-7-7zm1 9.29c.88-.39 1.5-1.26 1.5-2.29 0-1.38-1.12-2.5-2.5-2.5S9.5 10.62 9.5 12c0 1.02.62 1.9 1.5 2.29v3.3L7.59 21 9 22.41l3-3 3 3L16.41 21 13 17.59v-3.3zM12 1C5.93 1 1 5.93 1 12h2c0-4.97 4.03-9 9-9s9 4.03 9 9h2c0-6.07-4.93-11-11-11z", 
                            "#3F51B5", 0, 10, 10
                        )
                    });
                    return c;
                });
            }, 
            function() { }
        );
    }

    
    var update = function() {
        var map = maps_api.getMap();
        if(map.getBounds()) {
            console.log("Updating...");
            getContrib();
            getAirplanes();
            if(selectedMark) {
                if(selectedMark.data.dataType === "airplane")
                    getRoute(selectedMark);
                showInfoTo(selectedMark);
            }
        }
    }
    
    maps_api.doSetOnMarkerSelectListener(function(marker) {
        selectedMark = marker;
        if(marker.data.dataType === "airplane") {
            getRoute(marker);
        }
        console.log("Selecionando: " + marker.id);
        showInfoTo(marker);
    });

    maps_api.doSetOnMarkerUnselectListener(function(marker) {
        selectedMark = null;
        console.log("Deselecionando: " + (marker===null? " - ": marker.id));
        if(marker) {
            maps_api.doRemovePolyLine(marker);
            maps_api.doHideMarkerInfo(marker);
        }
        hideInfo();
    });
    
    maps_api.doSetOnInfoWindowCloseListener(function(marker) {
        selectedMark = null;
        console.log("Deselecionando: " + (marker===null? " - ": marker.id));
        if(marker) {
            maps_api.doRemovePolyLine(marker);
        }
        hideInfo();
    });
    
    // maps_api.doInit("#map");
    maps_api.doInit("#map", -5.4047339, -39.2927587, 7, function() {
        update();
        setInterval(update, 5000);
    });

}

function createIcon(path, color, angle, offsetX, offsetY) {
    return {
        path: path,
        fillColor: color,
        fillOpacity: 1,
        strokeWeight: 0,
        scale: 1.0, 
        rotation: angle, 
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(offsetX, offsetY),
    }
}

var timestampToDate = function(t) {
    return DateFormat.format.prettyDate(new Date(t));
}

function showInfoTo(marker) {

    var clear = function(text) {
        return text? text: "--";
    }

    if(marker.data.dataType == "airplane") {  
        var info = marker.data.data;
        $(".rl-map-drawer").addClass("is-visible");
        
        $(".rl-map-drawer__title").text(clear(info.flight));
        $(".rl-map-drawer__subtitle").text(clear(info.airline) + " - " + clear(info.airlineCountry));
        
        $(".rl-map-drawer__date").text("Atualizado " + clear(timestampToDate(info.timestamp)));
        $(".rl-map-drawer__lat").text(clear(info.latitude));
        $(".rl-map-drawer__lng").text(clear(info.longitude));
        $(".rl-map-drawer__alt").text(clear(info.altitude) + ' ft / ' + clear(parseFloat(parseInt(info.altitude * 30.48))/100) + ' m');
        $(".rl-map-drawer__speed").text(clear(info.horizontalVelocity) + ' knots / ' + clear(parseFloat(parseInt(info.horizontalVelocity * 185.2))/100) + ' km/h');
    } else if(marker.data.dataType == "contrib") {  
        maps_api.doShowMarkerInfo(
            marker,
            "<span><strong>Coletor: " + marker.data.data.ip + "</strong></span><br><span>Enviou informações " + timestampToDate(marker.data.data.timestamp) + "</span>"
        );
    }

    $(".rl-map-drawer__close-button").click(function() {
        
        maps_api.doUnselectMerker();
        hideInfo();
        
    });
}

function hideInfo() {
    $(".rl-map-drawer").removeClass("is-visible");
}

function colorFromAltitude(altitude, routeColors) {

    if(altitude < 0) altitude = 0;

    var color = routeColors[parseInt(routeColors.length * altitude / (100 * 1000))];
    return color;

}

function initColors(routeColors) {

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