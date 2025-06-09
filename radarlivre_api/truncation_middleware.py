import json


class RequestTruncationMiddleware:
    """Middleware para truncar casas decimais de campos específicos em requisições POST

    Objetivo: Prevenir erros de precisão excessiva em campos numéricos críticos
    Campos afetados: latitude, longitude, groundTrackHeading e horizontalVelocity"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            try:
                if not request.body:
                    return self.get_response(request)
                    
                try:
                    json_data = json.loads(request.body)
                except json.JSONDecodeError:
                    return self.get_response(request)

                if not isinstance(json_data, list) or not json_data or not isinstance(json_data[0], dict):
                    return self.get_response(request)

                required_fields = ["latitude", "longitude", "groundTrackHeading", "horizontalVelocity"]
                if not all(field in json_data[0] for field in required_fields):
                    return self.get_response(request)

                latitude, decimal_latitude = str(json_data[0]["latitude"]).split(".")
                longitude, decimal_longitude = str(json_data[0]["longitude"]).split(".")
                ground_tracking, decimal_ground_tracking = str(
                    json_data[0]["groundTrackHeading"]
                ).split(".")
                h_velocity, decimal_h_velocity = str(
                    json_data[0]["horizontalVelocity"]
                ).split(".")

                if len(decimal_latitude) > 10:
                    new_latitude = f"{latitude}.{decimal_latitude[:10]}"
                    json_data[0].update({"latitude": float(new_latitude)})

                if len(decimal_longitude) > 10:
                    new_longitude = f"{longitude}.{decimal_longitude[:10]}"
                    json_data[0].update({"longitude": float(new_longitude)})

                if len(decimal_ground_tracking) > 10:
                    new_ground_tracking = (
                        f"{ground_tracking}.{decimal_ground_tracking[:10]}"
                    )
                    json_data[0].update(
                        {"groundTrackHeading": float(new_ground_tracking)}
                    )

                if len(decimal_h_velocity) > 10:
                    new_h_velocity = f"{h_velocity}.{decimal_h_velocity[:10]}"
                    json_data[0].update({"horizontalVelocity": float(new_h_velocity)})

                request._body = bytes(json.dumps(json_data), encoding="utf-8")
            except Exception:
                return self.get_response(request)

        response = self.get_response(request)
        return response
