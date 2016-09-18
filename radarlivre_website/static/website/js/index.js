MDL_LOADED = false;
MAP_LOADED = false;

ROUTE_PROPAGATION_ENABLED = false;

var DataType = {
    AIRPLANE: "AIRPLANE", 
    AIRPLANE_PROPAGATED: "AIRPLANE_PROPAGATED", 
    ROUTE: "ROUTE", 
    COLLECTOR: "COLLECTOR", 
    AIRPORT: "AIRPORT"
};

var AIRPLANE_ICON_PATH = "M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"
var AIRPORT_ICON_PATH = "M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"
var COLLECTOR_ICON_PATH = "M12 5c-3.87 0-7 3.13-7 7h2c0-2.76 2.24-5 5-5s5 2.24 5 5h2c0-3.87-3.13-7-7-7zm1 9.29c.88-.39 1.5-1.26 1.5-2.29 0-1.38-1.12-2.5-2.5-2.5S9.5 10.62 9.5 12c0 1.02.62 1.9 1.5 2.29v3.3L7.59 21 9 22.41l3-3 3 3L16.41 21 13 17.59v-3.3zM12 1C5.93 1 1 5.93 1 12h2c0-4.97 4.03-9 9-9s9 4.03 9 9h2c0-6.07-4.93-11-11-11z"
var BALLOON_ICON_PATH = "M11,23A2,2 0 0,1 9,21V19H15V21A2,2 0 0,1 13,23H11M12,1C12.71,1 13.39,1.09 14.05,1.26C15.22,2.83 16,5.71 16,9C16,11.28 15.62,13.37 15,16A2,2 0 0,1 13,18H11A2,2 0 0,1 9,16C8.38,13.37 8,11.28 8,9C8,5.71 8.78,2.83 9.95,1.26C10.61,1.09 11.29,1 12,1M20,8C20,11.18 18.15,15.92 15.46,17.21C16.41,15.39 17,11.83 17,9C17,6.17 16.41,3.61 15.46,1.79C18.15,3.08 20,4.82 20,8M4,8C4,4.82 5.85,3.08 8.54,1.79C7.59,3.61 7,6.17 7,9C7,11.83 7.59,15.39 8.54,17.21C5.85,15.92 4,11.18 4,8Z"

componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {
	
    MDL_LOADED = true;
    log("MDL Loaded");
    if(MAP_LOADED)
        initMap();

    var settsDialog = rl_base.doAddDialog({
        button: "#rl-map__dialog-config__trigger",
        dialog: "#rl-map__dialog-config"
    });

    $("#rl-map__dialog-config__close").click(function() {
        settsDialog.close();
    });

    $("#rl-map__switch-enable-propagated-route").change(function() {
        ROUTE_PROPAGATION_ENABLED = $(this).is(":checked");
    });
    
});

function initMap() {

    MAP_LOADED = true;

    if(!MDL_LOADED) return;
    log("MAP Loaded");

    var routeColors = [];
    initColors(routeColors);
    
    var updateAirports = true;
    
    var getAirplanes = function() {
        radarlivre_updater.doBeginConnection(DataType.AIRPLANE,
            function(connId) {
                // log("Begin get airplanes...");
                var map = maps_api.getMap();
                radarlivre_api.doGetAirplaneInfos(
                    {
                        top: map.getBounds().getNorthEast().lat(), 
                        bottom: map.getBounds().getSouthWest().lat(), 
                        left: map.getBounds().getSouthWest().lng(), 
                        right: map.getBounds().getNorthEast().lng(), 
                        map_height: $("#map").height(), 
                        map_zoom: map.getZoom(), 
                        min_airplane_distance: 50
                    }, 
                    function(data) {
                        radarlivre_updater.doEndConnection(connId, DataType.AIRPLANE, data);
                    }, 
                    function(error) {
                        radarlivre_updater.doCancelConnection(connId, DataType.AIRPLANE);
                        log("Get airplanes error: " + error);
                    }
                );
            }
        );
    }
    
    var getAirplanesPropagated = function(flight) {
        radarlivre_updater.doBeginConnection(DataType.AIRPLANE_PROPAGATED + "_" + flight,
            function(connId) {
                // log("Begin get airplane propagation to " + flight);
                radarlivre_api.doGetFlightPropagation(
                    {
                        flight: flight, 
                        propagation_count: 12,
                        propagation_interval: 5000
                    }, 
                    function(data) {
                        radarlivre_updater.doEndConnection(connId, DataType.AIRPLANE_PROPAGATED + "_" + flight, data);
                    }, 
                    function(error) {
                        radarlivre_updater.doCancelConnection(connId, DataType.AIRPLANE_PROPAGATED + "_" + flight);
                        log("Get airplanes propagated error: " + error);
                    }
                );
            }
        );
    }
    
    var getAirports = function() {
        radarlivre_updater.doBeginConnection(DataType.AIRPORT,
           function(connId) {
                var map = maps_api.getMap();
                var mapsBounds = {
                    top: map.getBounds().getNorthEast().lat(), 
                    bottom: map.getBounds().getSouthWest().lat(), 
                    left: map.getBounds().getSouthWest().lng(), 
                    right: map.getBounds().getNorthEast().lng()
                };
                var zoom = map.getZoom();
                // log("Begin get airports: " + zoom);
                radarlivre_api.doGetAirports(
                    zoom, mapsBounds, 
                    function(data) {
                        radarlivre_updater.doEndConnection(connId, DataType.AIRPORT, data);
                    }, 
                    function(error) {
                        radarlivre_updater.doCancelConnection(connId, DataType.AIRPORT);
                        log("Get airport error: " + error);
                    }
                );
            }
        );
        
    }
    
    var getCollectors = function() {
        radarlivre_updater.doBeginConnection(DataType.COLLECTOR,
            function(connId) {
                // log("Begin get contribs...");
                radarlivre_api.doGetCollectors(
                    null,
                    function(data) {
                        radarlivre_updater.doEndConnection(connId, DataType.COLLECTOR, data);
                    }, 
                    function(error) {
                        radarlivre_updater.doCancelConnection(connId, DataType.COLLECTOR);
                        log("Get contrib error: " + error);
                    }
                );
            }
        );        
    }
    
    var getRoute = function() {
        var marker = maps_api.getSelectedMarker();
        if(marker && marker.dataType === DataType.AIRPLANE) {
            radarlivre_updater.doBeginConnection(DataType.ROUTE,
                function(connId) {
                    // log("Begin get route to: " + marker.id);
                    radarlivre_api.doGetAirplaneRoute(
                        marker.id, 
                        null, 
                        function(data) {
                            radarlivre_updater.doEndConnection(connId, DataType.ROUTE, data);
                        }, 
                        function(error) {
                            radarlivre_updater.doCancelConnection(connId, DataType.ROUTE);
                            log("Get route error: " + error);
                        }
                    );
                }
            );
        }
    }
    
    radarlivre_updater.doSetOnObjectCreatedListener(function(objects, connectionType, conn) {
        //if(objects.length > 0)
        //    log(objects.length + " " + connectionType + " objects created in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                
                maps_api.doSetMarker({
                    id: o.flight.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPLANE_ICON_PATH, "#FFEB3B", parseInt(o.groundTrackHeading), 10, 10, 1, 1)
                });

                if(ROUTE_PROPAGATION_ENABLED)
                    getAirplanesPropagated(o.flight.id);
                
            }
            
            // maps_api.doClusterizeMarkers();
        } else if(connectionType.startsWith(DataType.AIRPLANE_PROPAGATED)) {
            for(o of objects) {    
                
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPLANE_ICON_PATH, "#FFEB3B", parseInt(o.groundTrackHeading), 10, 10, .5, 1)
                });
            }
            
        } else if(connectionType == DataType.COLLECTOR) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(COLLECTOR_ICON_PATH, "#00f", o.angle, 10, 10, .9, 0)
                });
            }
        } else if(connectionType == DataType.ROUTE) {
            if(objects.length > 0) {
                marker = maps_api.getSelectedMarker();
                
                if(marker && marker.id == objects[0].flight) {
                    for(var i = 0; i < objects.length - 1; i++) {
                        var o1 = objects[i];
                        var o2 = objects[i + 1];
                        maps_api.doSetPolyLine(marker, {
                            id: o1.timestamp, 
                            path: [
                                {lat: parseFloat(o1.latitude), lng: parseFloat(o1.longitude)}, 
                                {lat: parseFloat(o2.latitude), lng: parseFloat(o2.longitude)}
                            ], 
                            color: "#000"
                        })
                    }
                }
            }
        } else if(connectionType == DataType.AIRPORT) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPORT_ICON_PATH, "#555", 0, 10, 10, .7, 0)
                });
            }
        }
    });
    
    radarlivre_updater.doSetOnObjectUpdatedListener(function(objects, connectionType, conn) {
        //if(objects.length > 0)
            //log(objects.length + " " + connectionType + " objects updated in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        showInfoTo(maps_api.getSelectedMarker());
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.flight.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPLANE_ICON_PATH, "#FFEB3B", parseInt(o.groundTrackHeading), 10, 10, 1, 1)
                });
                
                if(ROUTE_PROPAGATION_ENABLED)
                    getAirplanesPropagated(o.flight.id);
            }
        } else if(connectionType.startsWith(DataType.AIRPLANE_PROPAGATED)) {
            
            for(o of objects) {    
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPLANE_ICON_PATH, "#FFEB3B", parseInt(o.groundTrackHeading), 10, 10, .5, 1)
                });
            }
            
        } else if(connectionType == DataType.COLLECTOR) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(COLLECTOR_ICON_PATH, "#00f", o.angle, 10, 10, .9, 0)
                });
            }
        } else if(connectionType == DataType.ROUTE) {
            if(objects.length > 0) {
                marker = maps_api.getSelectedMarker();
                
                if(marker && marker.id == objects[0].flight) {
                    for(var i = 0; i < objects.length - 1; i++) {
                        var o1 = objects[i];
                        var o2 = objects[i + 1];
                        maps_api.doSetPolyLine(marker, {
                            id: o1.timestamp, 
                            path: [
                                {lat: parseFloat(o1.latitude), lng: parseFloat(o1.longitude)}, 
                                {lat: parseFloat(o2.latitude), lng: parseFloat(o2.longitude)}
                            ], 
                            color: "#000"
                        })
                    }
                }
            }
        } else if(connectionType == DataType.AIRPORT) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon(AIRPORT_ICON_PATH, "#555", 0, 10, 10, .7, 0)
                });
            }
        }
    });
    
    radarlivre_updater.doSetOnObjectRemovedListener(function(objects, connectionType, conn) {
        //if(objects.length > 0)
        //    log(objects.length + " " + connectionType + " objects removed in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.flight.id, connectionType) );
                
                for(k in maps_api.getMarkers()) {
                    if(k.startsWith(DataType.AIRPLANE_PROPAGATED)) {
                        toRemove = maps_api.getMarkers()[k].filter(function(marker) {
                            return marker.data.flight === o.flight.id;
                        });
                        for(k in toRemove)
                            maps_api.doRemoveMarker(toRemove[k]);
                    }
                }
                
            }
        } else if(connectionType.startsWith(DataType.AIRPLANE_PROPAGATED)) {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.id, connectionType) );
            }
        } else if(connectionType == DataType.AIRPORT) {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.id, connectionType) );
            }
        } else {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.id, connectionType) );
            }
        }
    });
    
    maps_api.doSetOnMarkerSelectListener(function(marker) {
        showInfoTo(marker);
        getRoute();
    });

    maps_api.doSetOnMarkerUnselectListener(function(marker) {
        hideInfo(marker);
        maps_api.doRemovePolyLine(marker);
    });

    maps_api.doSetOnInfoWindowCloseListener(function(marker) {
        hideInfo(marker);
        maps_api.doRemovePolyLine(marker);
        maps_api.doUnselectMarker();
    });
    
    maps_api.doSetOnMapZoomChangeListener(function() {
        updateAirports = true;
    });
    
    maps_api.doSetOnMapBoundsChangeListener(function() {
        updateAirports = true;
    });

    maps_api.doInit("#map", 0.001, 0.001, 7, function() {
        getAirplanes();
        getAirports();
        getCollectors();    
        setInterval(getAirplanes, 5000);
        setInterval(getRoute, 5000);
        setInterval(getCollectors, 5000);
        setInterval(function() {
            if(updateAirports) {
                updateAirports = false;
                getAirports();
            }
        }, 1000);
    });

    maps_api.doInitMapSearchBox("#rl-place-searchbox");
    
    radarlivre_updater.doInit();

}

function createIcon(path, color, angle, offsetX, offsetY, scale, strokeWeight) {
    return {
        path: path,
        fillColor: color,
        fillOpacity: 1,
        strokeWeight: strokeWeight,
        strokeColor: "#FF5722", 
        scale: scale? scale: 1, 
        rotation: angle, 
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(offsetX, offsetY),
    }
}

var timestampToDate = function(t) {
    return DateFormat.format.prettyDate(new Date(t));
}

function showInfoTo(object) {
    if(object) {
        var dataType = object.dataType;
        var marker = object;
        var data = object.data;

        var clearAirportType = function(text) {
            switch(text) {
                case "small_airport":
                    return "Aeroporto de pequeno porte";
                case "medium_airport":
                    return "Aeroporto de médio porte";
                case "large_airport":
                    return "Aeroporto de grande porte";
                case "seaplane_base":
                    return "Base de hidroaviões";
                case "heliport":
                    return "Heliporto";
                case "balloonport":
                    return "Aeroporto de balões";
                case "closed":
                    return "Aeroporto fechado";
                default:
                    return text;
            }
        }
        
        var clear = function(text) {
            return text? text: "--";
        }

        var formateNumber = function(n) {
            return parseFloat(parseInt(n*100))/100;
        }

        if(dataType == DataType.AIRPLANE) {  
            var info = data;
            $(".rl-map-drawer").addClass("is-visible");

            $(".rl-map-drawer__title").text(clear(info.flight.code));
            $(".rl-map-drawer__subtitle").text(clear(info.airline? info.airline.name: "") + " - " + clear(info.airline? info.airline.country: ""));

            $(".rl-map-drawer__date").text("Atualizado " + clear(timestampToDate(info.timestamp)));
            $(".rl-map-drawer__lat").text(clear(formateNumber(info.latitude)));
            $(".rl-map-drawer__lng").text(clear(formateNumber(info.longitude)));
            $(".rl-map-drawer__alt").text(clear(formateNumber(info.altitude)) + ' ft / ' + clear(parseFloat(parseInt(info.altitude * 30.48))/100) + ' m');
            $(".rl-map-drawer__speed").text(clear(formateNumber(info.horizontalVelocity)) + ' knots / ' + clear(parseFloat(parseInt(info.horizontalVelocity * 185.2))/100) + ' km/h');
        } else if(dataType == DataType.COLLECTOR) {  
            maps_api.doShowMarkerInfo(
                marker,
                "<span>" +
                	"<strong>Usuário " + clear(data.user.first_name) + " " + clear(data.user.last_name) + "</strong>" +
    			"</span><br>" +
    			"<span>" +
    				"Enviou informações " + timestampToDate(data.timestampData) +
				"</span>"
            );
        } else if(dataType == DataType.AIRPORT) {  
            maps_api.doShowMarkerInfo(
                marker,
                "<span>" +
                	clearAirportType(clear(data.type)) + "<br>" + clear(data.name) + " - <strong>" + clear(data.code) + "</strong>" +
    			"</span><br>" +
    			"<span>" +
    				clear(data.city) + ", " + clear(data.state) + "<br>" + clear(data.country) + 
				"</span>"
            );
        }

        $(".rl-map-drawer__close-button").click(function() {

            maps_api.doUnselectMarker();
            hideInfo();

        });
    }
}

function hideInfo(marker) {
    $(".rl-map-drawer").removeClass("is-visible");
    maps_api.doHideMarkerInfo(marker);
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
