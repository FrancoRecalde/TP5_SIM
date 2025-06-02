

class Box:
    
    def __init__(self):
        self.libre: bool = False
        self.ocupado: bool = False
        self.sanitizando: bool = False
        
    def set_libre(self):
        self.libre = True
        self.ocupado = False
        self.sanitizando = False
    
    def set_ocupado(self):
        self.ocupado = True
        self.libre = False
        
    def set_sanitizando(self):
        self.sanitizando = True
        self.ocupado = False
        self.libre = False
        
    def estado(self) -> str:
        if self.libre:
            return "Libre"
        elif self.ocupado:
            return "Ocupado"
        elif self.sanitizando:
            return "Sanitizando"
        else:
            return "Estado desconocido"
    