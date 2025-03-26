import dearpygui.dearpygui as dpg
import sympy as sp
from Funciones import Polinomica, Trigonometrica
import re

def convertir_a_numero(valor):
    """Convierte expresiones con pi en valores numéricos."""
    try:
        return float(sp.N(sp.sympify(valor.replace("π", "pi"))))
    except:
        return float(valor) if valor.replace('.', '', 1).isdigit() else 0

def formatear_expresion(expresion):
    """Formatea la expresión eliminando '.0' en enteros y aplicando superíndices."""
    
    # Quitar los '.0' de números enteros
    expresion = re.sub(r'(\d+)\.0([^0-9])', r'\1\2', expresion)
    
    # Reemplazar exponentes
    expresion = (expresion
                 .replace("x^2", "x²")
                 .replace("x^3", "x³")
                 .replace("x^1", "x")
                 .replace("x^0", ""))

    # Eliminar coeficientes "1" SOLO cuando preceden a una variable
    expresion = re.sub(r'\b1([a-zA-Z\(])', r'\1', expresion)

    return expresion

def actualizar_funcion():
    """Actualiza la visualización de la función según los coeficientes ingresados."""
    tipo_funcion = dpg.get_value("tipo_funcion")

    if tipo_funcion == "Polinómica":
        coeficientes = [float(dpg.get_value(f"coef_{i}") or 0) for i in range(6)]
        funcion = Polinomica(coeficientes)
        dpg.configure_item("grupo_polinomica", show=True)
        dpg.configure_item("grupo_trigonometrica", show=False)

    else:
        valores = [convertir_a_numero(dpg.get_value(f"param_{param}") or "0") for param in "ABCDEF"]
        funcion = Trigonometrica(*valores)
        
        dpg.configure_item("grupo_polinomica", show=False)
        dpg.configure_item("grupo_trigonometrica", show=True)

    funcion_str = str(funcion)
    dpg.set_value("funcion_display", formatear_expresion(funcion_str))

def interfaz():
    dpg.create_context()

    with dpg.window(label="Solucionador de ecuaciones", width=700, height=400):
        dpg.add_text("Seleccione el tipo de función:")
        dpg.add_combo(["Polinómica", "Trigonométrica"], default_value="Polinómica", tag="tipo_funcion", callback=actualizar_funcion)

        with dpg.group(tag="grupo_polinomica", show=True):
            dpg.add_text("Función polinómica:")
            with dpg.group(horizontal=True):
                for i in range(6):
                    dpg.add_input_text(tag=f"coef_{i}", width=50, default_value="0", callback=actualizar_funcion)
                    if i < 5:  # Agregar "+" en todos los términos excepto el último
                        dpg.add_text(f"x^{i} +" if i > 1 else "x +" if i == 1 else "+")
                    else:
                        dpg.add_text(f"x^{i}" if i > 1 else "x" if i == 1 else "")


        with dpg.group(tag="grupo_trigonometrica", show=False):
            dpg.add_text("Función trigonométrica:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="param_A", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text("sin(")
                dpg.add_input_text(tag="param_B", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text("x + ")
                dpg.add_input_text(tag="param_C", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text(") + ")
                dpg.add_input_text(tag="param_D", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text("cos(")
                dpg.add_input_text(tag="param_E", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text("x + ")
                dpg.add_input_text(tag="param_F", width=50, default_value="1", callback=actualizar_funcion)
                dpg.add_text(")")

        dpg.add_text("Seleccione el método numérico:")
        dpg.add_combo(["Bisección", "Newton", "Secante", "Regla Falsa"], default_value="Bisección", tag="metodo_numerico")

        dpg.add_text("Función seleccionada:", wrap=500)
        dpg.add_text("", tag="funcion_display", wrap=500)

    dpg.create_viewport(title="Solucionador de ecuaciones", width=700, height=400)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    interfaz()
