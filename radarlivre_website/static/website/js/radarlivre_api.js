var radarlivre_api = function() {

	/*
	 * PRIVADO
	 */
	
	var BASE_REMOTE_URL = "http://www.radarlivre.com/api/";
    var BASE_LOCAL_URL = "http://localhost:8000/api/";
	var baseURL = BASE_LOCAL_URL;
	
	var getJSON = function (url, params, callbackSucess, callbackError, callbackFinal) {
        params["format"] = "jsonp";

		$.getJSON( url, params )
		.done(function( data ) {

			callbackSucess(data);

		}).fail(function( jqxhr, textStatus, error ) {

		    callbackError(textStatus + ", " + error);

		}).always(function() {

			callbackFinal();

		});

	}

	/*
	 * PÚBLICO
	 */

	return {

		doInit : function() {

			

		}, 
        
        doGetAirplaneInfos : function(maxUpdateDelay, mapBounds, onReceived, onFailed) {
            mapBounds = mapBounds === null? {}: mapBounds;
            getJSON(baseURL + "airplane_info/?callback=?", {
                max_update_delay: maxUpdateDelay, 
                top: mapBounds.top, 
                bottom: mapBounds.bottom, 
                left: mapBounds.left, 
                right: mapBounds.right
            }, function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        }, 
        
        doGetAirplaneRoute : function(airplane, interval, onReceived, onFailed) {
            getJSON(baseURL + "observation/?callback=?", {
                airplane: airplane, 
                interval: interval
            }, function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        }, 
        
        doGetContribs : function(max_update_delay, onReceived, onFailed) {
            getJSON(baseURL + "contrib/?callback=?", {
                max_update_delay: max_update_delay
            }, function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        }

	};

} ();