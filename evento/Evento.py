

class Evento:
    def __init__(self, tiempo: float, tipo: str, practica=None, descripcion: str = ""):
        self.tiempo = tiempo
        self.tipo = tipo
        self.practica = practica  # instancia de Cirugia, Clinica o Emergencia
        self.descripcion = descripcion or tipo

    def __lt__(self, other):
        """Para poder ordenar eventos por tiempo"""
        return self.tiempo < other.tiempo

    def __repr__(self):
        return f"Evento({self.tiempo:.2f}, {self.tipo})"


    def set_tiempo(self, tiempo: float):
        """Actualiza el tiempo del evento"""
        self.tiempo = self.practica.llegada