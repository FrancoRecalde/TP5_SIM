import math
from main import rng

class Cirugia():
    def __init__(self):
        super().__init__()
        self.llegada = 0
        self.duracion_var = 0   
        
        self.random_num_frecuencia = 0
        self.random_num_duracion = 0
        self.frecuencia_llegada(tiempo=0)
        self.duracion()
    def frecuencia_llegada(self, tiempo: float):
        
        # Distribución exponencial negativa con media de 10 horas (600 minutos)
        self.random_num_frecuencia = rng.uniform(0, 1)

        media_minutos = 10 * 60
        self.llegada = -media_minutos * math.log(1 - self.random_num_frecuencia) +  tiempo
    
        
        
        
    def duracion(self):
        # Distribución uniforme entre 1 y 2 horas (en minutos: 60 a 120)
        self.random_num_duracion = rng.uniform(0, 1)
        
        min_minutos = 80
        max_minutos = 100
        
        self.duracion_var = (min_minutos + (max_minutos - min_minutos) * self.random_num_duracion)