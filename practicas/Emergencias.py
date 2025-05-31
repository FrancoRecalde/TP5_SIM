from main import rng
import Practica

class Emergencias(Practica):

    def frecuencia_llegada(self):
        # Distribución uniforme entre 5 y 10 horas (en minutos: 300 a 600)
        random_num = rng.uniform(0, 1)
        min_minutos = 6 * 60
        max_minutos = 10 * 60
        return min_minutos + (max_minutos - min_minutos) * random_num
    
    
    def duracion(self):
        # Distribución uniforme entre 1 y 2 horas (en minutos: 60 a 120)
        random_num = rng.uniform(0, 1)
        min_minutos = 70
        max_minutos = 130
        return min_minutos + (max_minutos - min_minutos) * random_num