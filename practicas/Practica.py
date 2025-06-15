from abc import ABC, abstractmethod



class Practica:
    
    @abstractmethod
    def frecuencia_llegada(self):
        pass
    
    @abstractmethod
    def duracion(self):
        pass

    @abstractmethod
    def set_estado(self):
        pass
