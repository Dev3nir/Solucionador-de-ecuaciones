import numpy as np

class Polinomica:
    def __init__(self, coeficientes):
        """
        coeficientes: lista de coeficientes en orden ascendente de grado.
        Ejemplo: [a0, a1, a2, a3, a4, a5] representa a0 + a1*x + a2*x^2 + ...
        """
        self.coeficientes = coeficientes
    
    def evaluar(self, x):
        """Evalúa la función en un punto x."""
        return sum(c * (x ** i) for i, c in enumerate(self.coeficientes))
    
    def __str__(self):
        """Devuelve una representación bonita de la función."""
        terminos = [f"{c}x^{i}" if i > 0 else str(c) for i, c in enumerate(self.coeficientes) if c != 0]
        return " + ".join(terminos).replace("x^1", "x")

class Trigonometrica:
    def __init__(self, A, B, C, D, E, F):
        """
        Representa la función g(x) = A sin(Bx + C) + D cos(Ex + F)
        """
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F
    
    def evaluar(self, x):
        """Evalúa la función en un punto x."""
        return self.A * np.sin(self.B * x + self.C) + self.D * np.cos(self.E * x + self.F)
    
    def __str__(self):
        """Devuelve una representación bonita de la función."""
        return f"{self.A}sin({self.B}x + {self.C}) + {self.D}cos({self.E}x + {self.F})"
