import math
from main import rng
import Practica

class Cirugia(Practica):

    def frecuencia_llegada(self):
        
        # Distribución exponencial negativa con media de 10 horas (600 minutos)
        random_num = rng.uniform(0, 1)
        media_minutos = 10 * 60
        return -media_minutos * math.log(1 - random_num)
    
    def duracion(self):
        # Distribución uniforme entre 1 y 2 horas (en minutos: 60 a 120)
        random_num = rng.uniform(0, 1)
        min_minutos = 80
        max_minutos = 100
        return min_minutos + (max_minutos - min_minutos) * random_num