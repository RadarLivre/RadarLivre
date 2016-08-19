var maps_marker_clustering = function() {
    
    var _getDistance = function(pos1, pos2, mapHeight, mapZoom) {
        a = _getPixelCoordinate(pos1, mapHeight, mapZoom);
        b = _getPixelCoordinate(pos2, mapHeight, mapZoom);
        return Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
    }
    
    var _getPixelCoordinate = function (pos, mapHeigth, zoom) {
        var latLng = pos;
        var scale = 1 << zoom;

        var worldCoordinate = _project(latLng, mapHeigth);

        var pixelCoordinate = new google.maps.Point(
            Math.floor(worldCoordinate.x * scale),
            Math.floor(worldCoordinate.y * scale));

        return pixelCoordinate;
    }

    var _project = function (latLng, TILE_SIZE) {

        var siny = Math.sin(latLng.lat() * Math.PI / 180);

        // Truncating to 0.9999 effectively limits latitude to 89.189. This is
        // about a third of a tile past the edge of the world tile.
        siny = Math.min(Math.max(siny, -0.9999), 0.9999);

        return new google.maps.Point(
            TILE_SIZE * (0.5 + latLng.lng() / 360),
            TILE_SIZE * (0.5 - Math.log((1 + siny) / (1 - siny)) / (4 * Math.PI)));
    }
    
    return {
        
        doCluster : function(markers, map, mapHeight, mapZoom) {
            
            var _markers = [];
            var index = 0;
            for(k in markers) {
                _markers.push({
                    id: index++, 
                    marker: markers[k], 
                    toHide: false
                });                
            }
            
            for(k in _markers) {
                for(l in _markers) {
                    m1 = _markers[k].marker;
                    m2 = _markers[l].marker;
                    if(_markers[k].id !== _markers[l].id && !_markers[k].toHide) {
                        d = _getDistance(m1.getPosition(), m2.getPosition(), mapHeight, mapZoom)
                        if (d < 50) {
                            _markers[l].toHide = true;
                        }
                    }
                }
            }
            
            for(k in _markers) {
                if(_markers[k].toHide) {
                    _markers[k].marker.setMap(null);
                } else if(!_markers[k].marker.getMap()) {
                    _markers[k].marker.setMap(map);
                }
            }
            
        }, 
        
        doClusterMarker : function(marker, markers, map, mapHeight, mapZoom) {
            
            for(k in markers) {
                m = markers[k];
                d = _getDistance(marker.getPosition(), m.getPosition(), mapHeight, mapZoom)
                if (d < 20) {
                    marker.setMap(null);
                    return ;
                }
            }
                        
        }
        
    };
    
}();