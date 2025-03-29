class Secante:
    def __init__(self, funcion, x0, x1, criterio, limite, limite_e):
        self.funcion = funcion
        self.x0 = x0
        self.x1 = x1
        self.criterio = criterio
        self.limite = limite
        self.limite_e = limite_e
        self.iteraciones_error = []  #Lista para almacenar error en cada iter
        self.iteraciones_values = []  #Lista para almacenar iteraciones

    def resolver(self):
        iteraciones = 0
        error = float('inf')
        raiz = None

        while True:
            f_x0 = self.funcion.evaluar(self.x0)
            f_x1 = self.funcion.evaluar(self.x1)

            print(f"Iteración {iteraciones}: x0={self.x0}, f(x0)={f_x0}, x1={self.x1}, f(x1)={f_x1}")

            if f_x1 - f_x0 == 0:
                print("División por cero detectada, saliendo...")
                return None

            x2 = self.x1 - f_x1 * (self.x1 - self.x0) / (f_x1 - f_x0)
            f_x2 = self.funcion.evaluar(x2)

            # Calcular error
            error = abs((x2 - self.x1) / x2) * 100 if x2 != 0 else float('inf')

            print(f"x2={x2}, f(x2)={f_x2}, error={error:.5f} %")

            # Guardar el error y la iteración
            self.iteraciones_error.append(error)
            self.iteraciones_values.append(iteraciones)

            # Condición de paro según criterio seleccionado
            if self.criterio.lower() in ["error", "error porcentual"] and error <= self.limite_e:
                print(f"Se alcanzó el error tolerado: {error:.5f} %")
                raiz = x2
                break
            elif self.criterio == "Número de iteraciones" and iteraciones >= self.limite:
                print(f"Se alcanzó el número máximo de iteraciones: {iteraciones}")
                raiz = x2
                break
            elif abs(f_x2) < 1e-6:  # Si la función es suficientemente pequeña
                print(f"Raíz encontrada en x2={x2}, f(x2)={f_x2}")
                raiz = x2
                break

            # Actualizar valores para la siguiente iteración
            self.x0, self.x1 = self.x1, x2
            iteraciones += 1

        if raiz is not None:
            print(f"Raíz encontrada o aproximada: {raiz}")
            return raiz, iteraciones, error 
        else:
            print("No se encontró una raíz dentro de los parámetros especificados.")
            return None
