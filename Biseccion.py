class Biseccion:
    def __init__(self, funcion, x0, x1, criterio, limite, limite_e):
        self.funcion = funcion
        self.x0 = x0
        self.x1 = x1
        self.criterio = criterio
        self.limite = limite
        self.limite_e = limite_e
        self.iteraciones_error = []  # Lista para almacenar error en cada iteración
        self.iteraciones_values = []  # Lista para almacenar iteraciones

    def resolver(self):
        iteraciones = 0
        error = float('inf')
        raiz = None

        while True:
            c = (self.x0 + self.x1) / 2
            f_c = self.funcion.evaluar(c)
            f_x0 = self.funcion.evaluar(self.x0)
            f_x1 = self.funcion.evaluar(self.x1)

            print(f"Iteración {iteraciones}: x0={self.x0}, x1={self.x1}, c={c}, f(x0)={f_x0}, f(x1)={f_x1}, f(c)={f_c}")

            # Calcular error (diferencia relativa entre intervalos)
            error = abs((self.x1 - self.x0) / c) * 100 if c != 0 else float('inf')

            print(f"Error actual: {error:.5f} %")

            # Guardar error e iteración
            self.iteraciones_error.append(error)
            self.iteraciones_values.append(iteraciones)

            # Condiciones de parada
            if self.criterio.lower() in ["error", "error porcentual"] and error <= self.limite_e:
                print(f"Se alcanzó el error tolerado: {error:.5f} %")
                raiz = c
                break
            elif self.criterio == "Número de iteraciones" and iteraciones >= self.limite:
                print(f"Se alcanzó el número máximo de iteraciones: {iteraciones}")
                raiz = c
                break
            elif abs(f_c) < 1e-6:  # Raíz encontrada con tolerancia
                print(f"Raíz encontrada en c={c}, f(c)={f_c}")
                raiz = c
                break

            # Actualizar intervalo
            if f_x0 * f_c < 0:
                self.x1 = c
            else:
                self.x0 = c

            iteraciones += 1

        print(f"Raíz encontrada o aproximada: {raiz}") if raiz else print("No se encontró una raíz dentro del intervalo.")
        return raiz, iteraciones, error
