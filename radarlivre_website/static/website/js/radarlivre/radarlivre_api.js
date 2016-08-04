var radarlivre_api = function() {

	/*
	 * PRIVADO
	 */
	
	var BASE_REMOTE_URL = "http://www.radarlivre.com/api/";
    var BASE_LOCAL_URL = "http://localhost:8000/api/";
	var baseURL = BASE_REMOTE_URL;
	
	var getJSON = function (url, params, callbackSucess, callbackError, callbackFinal) {
        params["format"] = "jsonp";
        
        $.jsonp({
            url: url,
            callbackParameter: "callback", 
            data: params, 
            success: function( data ) {

                callbackSucess(data);

            }, 
            error: function( d, error ) {

                callbackError(error);

            }
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
            getJSON(baseURL + "airplane_info/", {
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
            getJSON(baseURL + "observation/", {
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
            getJSON(baseURL + "contrib/", {
                max_update_delay: max_update_delay
            }, function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        }, 
        
        jsonpCallBack : function(data) {
            log("Jsonp recebido");
        }

	};

} ();