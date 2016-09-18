import math

class Math():

    @staticmethod
    def degreesToRadians(degrees):
        return float(degrees) * math.pi / 180.0

    @staticmethod
    def radiansToDegrees(rad):
        return float(rad) * 180.0 / math.pi

    @staticmethod
    def normalize(vector2D):
        return math.sqrt(math.pow(vector2D[0], 2.0) + math.pow(vector2D[1], 2.0));

    @staticmethod
    def rotate(vector2D, theta):
        x = float(vector2D[0])
        y = float(vector2D[1])
        theta = Math.degreesToRadians(theta)
        aux = x * math.cos(theta) - y * math.sin(theta)
        y = x * math.sin(theta) + y * math.cos(theta)
        x = aux
        return (x, y)

    @staticmethod
    def knotsToMetres(knots):
        return (knots * 1.852) / 3.6


class Util():

    @staticmethod
    def parseParam(request, param, defaultValue):
        param = request.GET.get(param)

        if param:
            try:
                return float(param)
            except:
                pass

        return defaultValue