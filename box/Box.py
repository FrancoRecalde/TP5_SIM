

class box:
    
    def __init__(self):
        self.estado: str = ""
        
    def set_libre(self):
        self.estado = "libre"
    
    def set_ocupado(self):
        self.estado = "ocupado" 
        
    def set_sanitizando(self):
        self.estado = "sanitizando"
    