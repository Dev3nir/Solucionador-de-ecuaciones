class Newton:
    def __init__(self, funcion, x0, criterio, limite, limite_e):
        self.funcion = funcion
        self.x0 = x0
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
            f_x0 = self.funcion.evaluar(self.x0)
            df_x0 = self.funcion.derivar(self.x0)

            print(f"Iteración {iteraciones}: x0={self.x0}, f(x0)={f_x0}, f'(x0)={df_x0}")

            if df_x0 == 0:
                print("Derivada se anuló. El método de Newton no puede continuar.")
                return None

            x1 = self.x0 - f_x0 / df_x0
            f_x1 = self.funcion.evaluar(x1)

            # Calcular error
            error = abs((x1 - self.x0) / x1) * 100 if x1 != 0 else float('inf')

            print(f"x1={x1}, f(x1)={f_x1}, error={error:.5f} %")

            # Guardar error e iteraciones
            self.iteraciones_error.append(error)
            self.iteraciones_values.append(iteraciones)

            # Condición de paro según criterio seleccionado
            if self.criterio.lower() in ["error", "error porcentual"] and error <= self.limite_e:
                print(f"Se alcanzó el error tolerado: {error:.5f} %")
                raiz = x1
                break
            elif self.criterio == "Número de iteraciones" and iteraciones >= self.limite:
                print(f"Se alcanzó el número máximo de iteraciones: {iteraciones}")
                raiz = x1
                break
            elif abs(f_x1) < 1e-6:  # Si la función es suficientemente pequeña
                print(f"Raíz encontrada en x1={x1}, f(x1)={f_x1}")
                raiz = x1
                break

            # Actualizar valores para la siguiente iteración
            self.x0 = x1
            iteraciones += 1

        if raiz is not None:
            print(f"Raíz encontrada o aproximada: {raiz}")
            return raiz, iteraciones, error
        else:
            print("No se encontró una raíz dentro de los parámetros especificados.")
            return None
