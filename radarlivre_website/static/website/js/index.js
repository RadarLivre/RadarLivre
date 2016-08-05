MDL_LOADED = false;
MAP_LOADED = false;

var DataType = {
    AIRPLANE: "AIRPLANE", 
    ROUTE: "ROUTE", 
    CONTRIB: "CONTRIB"
};

componentHandler.registerUpgradedCallback("MaterialLayout", function(elem) {
	
    MDL_LOADED = true;
    log("MDL Loaded");
    if(MAP_LOADED)
        initMap();
    
});

function initMap() {

    MAP_LOADED = true;

    if(!MDL_LOADED) return;
    log("MAP Loaded");

    var routeColors = [];
    initColors(routeColors);
    
    var getAirplanes = function() {
        if(radarlivre_updater.doBeginConnection(DataType.AIRPLANE)) {
            // log("Begin get airplanes...");
            var map = maps_api.getMap();
            var mapsBounds = {
                top: map.getBounds().getNorthEast().lat(), 
                bottom: map.getBounds().getSouthWest().lat(), 
                left: map.getBounds().getSouthWest().lng(), 
                right: map.getBounds().getNorthEast().lng()
            };
            radarlivre_api.doGetAirplaneInfos(
                null, mapsBounds, 
                function(data) {
                    radarlivre_updater.doEndConnection(DataType.AIRPLANE, data, "airplane");
                }, 
                function(error) {
                    radarlivre_updater.doCancelConnection(DataType.AIRPLANE);
                    log("Get airplanes error: " + error);
                }
            );
        } else {
            log("Can't get airplanes. Request already sended!");
        }
        
    }
    
    var getContrib = function() {
        if(radarlivre_updater.doBeginConnection(DataType.CONTRIB)) {
            // log("Begin get contribs...");
            radarlivre_api.doGetContribs(
                null, 
                function(data) {
                    radarlivre_updater.doEndConnection(DataType.CONTRIB, data);
                }, 
                function(error) {
                    radarlivre_updater.doCancelConnection(DataType.CONTRIB);
                    log("Get contrib error: " + error);
                }
            );
        } else {
            log("Can't get contrib. Request already sended!");
        }
        
    }
    
    var getRoute = function() {
        var marker = maps_api.getSelectedMarker();
        if(marker && marker.dataType === DataType.AIRPLANE) {
            if(radarlivre_updater.doBeginConnection(DataType.ROUTE)) {
                // log("Begin get route to: " + marker.id);
                radarlivre_api.doGetAirplaneRoute(
                    marker.id, 
                    null, 
                    function(data) {
                        radarlivre_updater.doEndConnection(DataType.ROUTE, data);
                    }, 
                    function(error) {
                        radarlivre_updater.doCancelConnection(DataType.ROUTE);
                        log("Get route error: " + error);
                    }
                );
                
            } else {
                log("Can't get route. Request already sended!");
            }
        }
    }
    
    
    var update = function() {
        log("Updating...");
        
        getAirplanes();
        getContrib();
        getRoute();
    }
    
    radarlivre_updater.doSetOnObjectCreatedListener(function(objects, connectionType, conn) {
        //log(objects.length + " " + connectionType + " objects created in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.airplane, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon("M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z", "#000", o.angle, 10, 10)
                });
            }
        } else if(connectionType == DataType.CONTRIB) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon("M12 5c-3.87 0-7 3.13-7 7h2c0-2.76 2.24-5 5-5s5 2.24 5 5h2c0-3.87-3.13-7-7-7zm1 9.29c.88-.39 1.5-1.26 1.5-2.29 0-1.38-1.12-2.5-2.5-2.5S9.5 10.62 9.5 12c0 1.02.62 1.9 1.5 2.29v3.3L7.59 21 9 22.41l3-3 3 3L16.41 21 13 17.59v-3.3zM12 1C5.93 1 1 5.93 1 12h2c0-4.97 4.03-9 9-9s9 4.03 9 9h2c0-6.07-4.93-11-11-11z", "#00f", o.angle, 10, 10)
                });
            }
        } else if(connectionType == DataType.ROUTE) {
            if(objects.length > 0) {
                marker = maps_api.getSelectedMarker();
                
                if(marker && marker.id == objects[0].airplane) {
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
        }
    });
    
    radarlivre_updater.doSetOnObjectUpdatedListener(function(objects, connectionType, conn) {
        //log(objects.length + " " + connectionType + " objects updated in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        showInfoTo(maps_api.getSelectedMarker());
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.airplane, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon("M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z", "#000", o.angle, 10, 10)
                });
            }
        } else if(connectionType == DataType.CONTRIB) {
            for(o of objects) {
                maps_api.doSetMarker({
                    id: o.id, 
                    dataType: connectionType, 
                    data: o, 
                    position: new google.maps.LatLng(o.latitude, o.longitude), 
                    icon: createIcon("M12 5c-3.87 0-7 3.13-7 7h2c0-2.76 2.24-5 5-5s5 2.24 5 5h2c0-3.87-3.13-7-7-7zm1 9.29c.88-.39 1.5-1.26 1.5-2.29 0-1.38-1.12-2.5-2.5-2.5S9.5 10.62 9.5 12c0 1.02.62 1.9 1.5 2.29v3.3L7.59 21 9 22.41l3-3 3 3L16.41 21 13 17.59v-3.3zM12 1C5.93 1 1 5.93 1 12h2c0-4.97 4.03-9 9-9s9 4.03 9 9h2c0-6.07-4.93-11-11-11z", "#00f", o.angle, 10, 10)
                });
            }
        } else if(connectionType == DataType.ROUTE) {
            if(objects.length > 0) {
                marker = maps_api.getSelectedMarker();
                
                if(marker && marker.id == objects[0].airplane) {
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
        }
    });
    
    radarlivre_updater.doSetOnObjectRemovedListener(function(objects, connectionType, conn) {
        //log(objects.length + " " + connectionType + " objects removed in a delay of " + (conn.responseTimestamp - conn.requestTimestamp) + " milliseconds");
        
        if(connectionType == DataType.AIRPLANE) {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.airplane) );
            }
        } else {
            for(o of objects) {
                maps_api.doRemoveMarker( maps_api.getMarker(o.id) );
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
    });

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

function showInfoTo(object) {
    if(object) {
        var dataType = object.dataType;
        var marker = object;
        var data = object.data;

        var clear = function(text) {
            return text? text: "--";
        }

        if(dataType == DataType.AIRPLANE) {  
            var info = data;
            $(".rl-map-drawer").addClass("is-visible");

            $(".rl-map-drawer__title").text(clear(info.flight));
            $(".rl-map-drawer__subtitle").text(clear(info.airline) + " - " + clear(info.airlineCountry));

            $(".rl-map-drawer__date").text("Atualizado " + clear(timestampToDate(info.timestamp)));
            $(".rl-map-drawer__lat").text(clear(info.latitude));
            $(".rl-map-drawer__lng").text(clear(info.longitude));
            $(".rl-map-drawer__alt").text(clear(info.altitude) + ' ft / ' + clear(parseFloat(parseInt(info.altitude * 30.48))/100) + ' m');
            $(".rl-map-drawer__speed").text(clear(info.horizontalVelocity) + ' knots / ' + clear(parseFloat(parseInt(info.horizontalVelocity * 185.2))/100) + ' km/h');
        } else if(dataType == DataType.CONTRIB) {  
            maps_api.doShowMarkerInfo(
                marker,
                "<span><strong>Coletor: " + data.ip + "</strong></span><br><span>Enviou informações " + timestampToDate(data.timestamp) + "</span>"
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
