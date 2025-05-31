from main import rng

class Sanitario:

    def calcular_tiempo(self) -> float:
        """
        Calcula el tiempo necesario para alcanzar un valor de S entre 1 y 3 
        """
        random_num = rng.uniform(0, 1)
        s_objetivo = 1 + random_num * (3-1)  # S entre 1 y 3
        return self.runge_kutta(s_objetivo)
        
        
    def runge_kutta(self, S_objetivo, h=0.1) -> float:
        """
        Integra dS/dt = 3t + 0.05 * S^2 desde S=0 hasta alcanzar S_objetivo.
        Devuelve el valor de t * 10 cuando se alcanza o supera S_objetivo.
        """
        def f(t, s):
            return 3 * t + 0.05 * s**2

        t = 0
        s = 0

        while s < S_objetivo:
            k1 = h * f(t, s)
            k2 = h * f(t + h / 2, s + k1 / 2)
            k3 = h * f(t + h / 2, s + k2 / 2)
            k4 = h * f(t + h, s + k3)
            s += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            t += h

        return round(t * 10, 2)