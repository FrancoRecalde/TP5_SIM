class Contador:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Contador, cls).__new__(cls)
            cls._instance._valor = 0
        return cls._instance

    def siguiente(self):
        self._valor += 1
        return self._valor
