import math


class Math:
    """Classe com métodos estáticos para cálculos matemáticos e conversões de unidades aeronáuticas"""

    @staticmethod
    def degrees_to_radians(degrees):
        return float(degrees) * math.pi / 180.0

    @staticmethod
    def radians_to_degrees(rad):
        return float(rad) * 180.0 / math.pi

    @staticmethod
    def normalize(vector2_d):
        return math.sqrt(math.pow(vector2_d[0], 2.0) + math.pow(vector2_d[1], 2.0))

    @staticmethod
    def rotate(vector2_d, theta):
        x = float(vector2_d[0])
        y = float(vector2_d[1])
        theta = Math.degrees_to_radians(theta)
        aux = x * math.cos(theta) - y * math.sin(theta)
        y = x * math.sin(theta) + y * math.cos(theta)
        x = aux
        return x, y

    @staticmethod
    def knots_to_metres(knots):
        return (knots * 1.852) / 3.6


class Util:
    """Classe utilitária para operações comuns no processamento de requisições"""

    @staticmethod
    def parse_param(request, param, default_value):
        """Obtém e converte parâmetro da requisição para float, com fallback para valor padrão"""

        param = request.GET.get(param)

        if param:
            try:
                return float(param)
            except ValueError:
                pass

        return default_value
