import math
from RNG import rng

class Cirugia:
    def __init__(self, media_llegada, duracion_min, duracion_max):
        self.media = media_llegada
        self.duracion_min = duracion_min
        self.duracion_max = duracion_max
        self.estado = None
        self.random_num_frecuencia = rng.uniform(0, 1)
        self.random_num_duracion = rng.uniform(0, 1)
        self.llegada = -self.media * math.log(1 - self.random_num_frecuencia)
        self.duracion_var = self.duracion_min + (self.duracion_max - self.duracion_min) * self.random_num_duracion

    def frecuencia_llegada(self, tiempo):
        self.random_num_frecuencia = rng.uniform(0, 1)
        self.llegada = -self.media * math.log(1 - self.random_num_frecuencia) + tiempo

    def duracion(self):
        self.random_num_duracion = rng.uniform(0, 1)
        self.duracion_var = self.duracion_min + (self.duracion_max - self.duracion_min) * self.random_num_duracion

    def set_estado(self, estado):
        try:
            if estado in ('creacion', 'llevandose a cabo', 'cola prioritaria', 'destruccion'):
                self.estado = estado
            else:
                raise TypeError("El estado debe ser creacion, llevandose a cabo, cola prioritaria o destruccion")
        except TypeError as e:
            print("Error ", e)

    def get_estado(self):
        return self.estado
