var radarlivre_api = function() {

	/*
	 * PRIVADO
	 */

	var BASE_REMOTE_URL = "http://www.radarlivre.com/api/";
    	var BASE_LOCAL_URL = "http://localhost:8000/api/";
	var baseURL = BASE_REMOTE_URL;

	var getJSON = function (url, params, callbackSucess, callbackError, callbackFinal) {
        params["format"] = "jsonp";

        try {
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
        } catch(error) {
            callbackError(error);
        }

	}

	/*
	 * PÚBLICO
	 */

	return {

		doInit : function() {



		},

        doGetAirplaneInfos : function(params, onReceived, onFailed) {
            getJSON(baseURL + "flight_info/", params,
            function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        },

        doGetFlightPropagation : function(params, onReceived, onFailed) {
            getJSON(baseURL + "flight_propagated_trajectory/", params
            , function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        },

        doGetAirports : function(zoom, mapBounds, onReceived, onFailed) {
            mapBounds = mapBounds === null? {}: mapBounds;
            getJSON(baseURL + "airport/", {
                zoom: zoom,
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

        doGetAirplaneRoute : function(flight, interval, onReceived, onFailed) {
            getJSON(baseURL + "observation/", {
                flight: flight,
                interval: interval
            }, function(data) {
                onReceived(data);
            }, function(error) {
                onFailed(error);
            }, function() {

            });
        },

        doGetCollectors : function(max_update_delay, onReceived, onFailed) {
            getJSON(baseURL + "collector/", {
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
