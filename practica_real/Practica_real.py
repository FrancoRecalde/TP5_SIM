from TP2_SIM.practicas import Practica
from TP2_SIM.services import num_id
class Practica_real:
    
    def __init__(self) -> None:
        self.tipo: Practica = None
        self.id: int = num_id.Contador().siguiente()
        estado: str = ""
        
    def set_llevandose_a_cabo(self):
        self.estado = "llevandose_a_cabo"
        
    def set_cola(self):
        self.estado = "cola"
    
    def cola_prioritaria(self):
        self.estado = "cola_prioritaria"
        
        