from main import rng

class Sanitario:
    
    def __init__(self, s_min, s_max, a, b, h):
        self.s_min = s_min
        self.s_max = s_max
        self.a = a  # valor que antes era 3
        self.b = b  # valor que antes era 0.05
        self.h = h

        
    def runge_kutta(self, S_objetivo):
        def f(t, s):
            return self.a * t + self.b * s**2

        t = 0
        s = 0
        h = self.h

        while s < S_objetivo:
            k1 = h * f(t, s)
            k2 = h * f(t + h / 2, s + k1 / 2)
            k3 = h * f(t + h / 2, s + k2 / 2)
            k4 = h * f(t + h, s + k3)
            s += (k1 + 2 * k2 + 2 * k3 + k4) / 6
            t += h

        return t * 10