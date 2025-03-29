import dearpygui.dearpygui as dpg
import sympy as sp
from Funciones import Polinomica, Trigonometrica
import re
import matplotlib.pyplot as plt
from Secante import Secante 


##-------------------------------------------------------------------------------------------
#-----------------------------
## TRANSFORMAR EXPRESIONES

def convertir_a_numero(valor):
    """Convierte expresiones con pi en valores numéricos."""
    try:
        return float(sp.N(sp.sympify(valor.replace("π", "pi"))))
    except:
        return float(valor) if valor.replace('.', '', 1).isdigit() else 0
#_____________________________________________________________________________
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
#_____________________________________________________________________________
def obtener_funcion():
    """Obtiene la función seleccionada con sus parámetros. Transofrma la func a una expresión analítica"""
    tipo_funcion = dpg.get_value("tipo_funcion")
    if tipo_funcion == "Polinómica":
        coeficientes = [convertir_a_numero(dpg.get_value(f"coef_{i}") or "0") for i in range(6)]

        return Polinomica(coeficientes)
    else:
        valores = [convertir_a_numero(dpg.get_value(f"param_{param}") or "0") for param in "ABCDEF"]
        return Trigonometrica(*valores)



##-------------------------------------------------------------------------------------------
#-----------------------------
## MUESTRA LA FUNCIÓN EN LA VENTANA
def actualizar_funcion():
    """Actualiza la visualización de la función según los coeficientes ingresados."""
    tipo_funcion = dpg.get_value("tipo_funcion")

    if tipo_funcion == "Polinómica":
        coeficientes = [convertir_a_numero(dpg.get_value(f"coef_{i}") or "0") for i in range(6)]
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


##-------------------------------------------------------------------------------------------
#-----------------------------
##CONFIG DE LA GRÁFICA
def graficar_error(iteraciones_values, iteraciones_error):
    """Genera la gráfica del error en función de las iteraciones"""
    plt.style.use("dark_background")
    
    plt.figure(figsize=(8, 5))
    plt.plot(iteraciones_values, iteraciones_error, label='Error relativo', color='cyan', marker='o')

    plt.axhline(0, color='white', linewidth=1)
    plt.axvline(0, color='white', linewidth=1)
    plt.legend()
    plt.title('Error en función de las Iteraciones')
    plt.xlabel('Iteraciones')
    plt.ylabel('Error (%)')
    plt.grid(True, linestyle='--', linewidth=0.3)
    plt.show()


## RESUELVE LA EC. SEGÚN EL MÉTODO ESCOGIDO USANDO LAS CLASES DE LOS MÉTODOS
def res():
    """Obtiene los datos y los envía a la clase correspondiente para obtener la raíz"""
    funcion = obtener_funcion()
    metodo = dpg.get_value("metodo_numerico")

    if metodo == "Bisección":
        x0 = convertir_a_numero(dpg.get_value("biseccion_x0"))
        criterio = dpg.get_value("criterio_paro")
        
        if criterio == "Número de iteraciones":
            limite = int(dpg.get_value("input_iteraciones"))
        else:
            limite = float(dpg.get_value("input_error"))
        #Mandar llamar al método y pasar valores
        
    if metodo == "Newton":
        x0 = convertir_a_numero(dpg.get_value("newton_x0"))
        criterio = dpg.get_value("criterio_paro")
        
        if criterio == "Número de iteraciones":
            limite = int(dpg.get_value("input_iteraciones"))
        else:
            limite = float(dpg.get_value("input_error"))
        #Mandar llamar al método y pasar valores
    
    if metodo == "Secante":
        x0 = convertir_a_numero(dpg.get_value("secante_x0"))
        x1 = convertir_a_numero(dpg.get_value("secante_x1"))
        criterio = dpg.get_value("criterio_paro")
        
        if criterio == "Número de iteraciones":
            limite = int(dpg.get_value("input_iteraciones"))
            limite_e = None  # Para evitar valores basura
        else:
            limite_e = float(dpg.get_value("input_error"))
            limite = None  # Para evitar valores basura
        print(f"Criterio: {criterio}, Límite: {limite_e}")
        print(f"Criterio recibido: '{criterio}'")
        solucionador = Secante(funcion, x0, x1, criterio, limite, limite_e)
        raiz, iteraciones, error = solucionador.resolver()

        dpg.set_value("resultado_texto", f"Raíz encontrada en el intervalo: {raiz} con error de {error:.5f}% \nNúmero de iteraciones: {iteraciones}" if raiz is not None else "No se encontró raíz")
        graficar_error(solucionador.iteraciones_values, solucionador.iteraciones_error)

##-------------------------------------------------------------------------------------------
#-----------------------------
## CONFIG DE VENTANA 

def interfaz():
    dpg.create_context()
    #Combo para escoger func
    with dpg.window(label="Solucionador de ecuaciones", width=700, height=400):
        dpg.add_text("Seleccione el tipo de función:")
        dpg.add_combo(["Polinómica", "Trigonométrica"], default_value="Polinómica", tag="tipo_funcion", callback=actualizar_funcion)

#_____________________________________________________________________________
        #Config función polinómica
        with dpg.group(tag="grupo_polinomica", show=True):
            dpg.add_text("Función polinómica:")
            with dpg.group(horizontal=True):
                for i in range(6):
                    dpg.add_input_text(tag=f"coef_{i}", width=50, default_value="0", callback=actualizar_funcion)
                    if i < 5: 
                        dpg.add_text(f"x^{i} +" if i > 1 else "x +" if i == 1 else "+")
                    else:
                        dpg.add_text(f"x^{i}" if i > 1 else "x" if i == 1 else "")
#_____________________________________________________________________________
        #Config función trigonométrica
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
#_____________________________________________________________________________
        
        ### INSUMOS PARA CADA MÉTODO
        def actualizar_inputs_metodo():
            """Muestra u oculta los inputs necesarios según el método seleccionado."""
            metodo = dpg.get_value("metodo_numerico")
            
            if metodo == "Bisección":
                dpg.configure_item("grupo_biseccion", show=True)
            else:
                dpg.configure_item("grupo_biseccion", show=False)
            
            if metodo == "Newton":
                dpg.configure_item("grupo_Newton", show=True)
            else:
                dpg.configure_item("grupo_Newton", show=False)
            
            if metodo == "Secante":
                dpg.configure_item("grupo_secante", show=True)
            else:
                dpg.configure_item("grupo_secante", show=False)

        #Mostrar campos según el criterio
        def actualizar_inputs_criterio():
            """Muestra el input adecuado según el criterio de paro seleccionado."""
            criterio = dpg.get_value("criterio_paro")

            if criterio == "Número de iteraciones":
                dpg.configure_item("input_iteraciones", show=True)
                dpg.configure_item("input_error", show=False)
            else:
                dpg.configure_item("input_iteraciones", show=False)
                dpg.configure_item("input_error", show=True)
#_____________________________________________________________________________
        
        #Selección de método con un combo
        dpg.add_text("Seleccione el método numérico:")
        dpg.add_combo(["Bisección", "Newton", "Secante", "Regla Falsa"], default_value="Bisección",
                    tag="metodo_numerico", callback=actualizar_inputs_metodo)

        # Grupo para Bisección
        with dpg.group(tag="grupo_biseccion", show=False):
            dpg.add_text("Ingrese el intervalo")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="biseccion_x0", width=80, default_value="-")
                dpg.add_text(", ")
                dpg.add_input_text(tag="biseccion_x1", width=80, default_value="+")

        # Grupo para Newton
        with dpg.group(tag="grupo_Newton", show=False):
            dpg.add_text("Ingrese el punto inicial")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="newton_x0", width=80, default_value="0")

        # Grupo para Secante
        with dpg.group(tag="grupo_secante", show=False):
            dpg.add_text("Ingrese los dos puntos iniciales:")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="secante_x0", width=80, default_value="0")
                dpg.add_text(", ")
                dpg.add_input_text(tag="secante_x1", width=80, default_value="1")

        # Grupo para Regla Falsa
        with dpg.group(tag="grupo_regla_falsa", show=False):
            dpg.add_text("Ingrese el intervalo")
            with dpg.group(horizontal=True):
                dpg.add_input_text(tag="reglafalsa_x0", width=80, default_value="-")
                dpg.add_text(", ")
                dpg.add_input_text(tag="reglafalsa_x1", width=80, default_value="+")
#_____________________________________________________________________________
        ##ESCOGER CRITERIO DE PARO
        dpg.add_text("Seleccione el criterio de paro:")
        dpg.add_combo(["Número de iteraciones", "Error porcentual"], default_value="Número de iteraciones",
                        tag="criterio_paro", callback=actualizar_inputs_criterio)

        dpg.add_input_int(tag="input_iteraciones", label="Iteraciones", default_value=10, min_value=1)
        dpg.add_input_float(tag="input_error", label="Error porcentual", default_value=0.01, min_value=0.0001, show=False)
#_____________________________________________________________________________
       
        ##ESPACIO DONDE SE MUESTRA LA FUNC
        dpg.add_text("Función seleccionada:", wrap=500)
        dpg.add_text("", tag="funcion_display", wrap=500)
#_____________________________________________________________________________
        ###BOTONES
    
        #Tema para los botones
        with dpg.theme() as tema_btn:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (12,84,132), category=dpg.mvThemeCat_Core) 
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (9, 66, 105), category=dpg.mvThemeCat_Core)  
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (7, 53, 84), category=dpg.mvThemeCat_Core)  
            
        #Botón para resolver
        res_btn = dpg.add_button(label="Resolver", callback=res)
        dpg.bind_item_theme(res_btn, tema_btn)
        dpg.add_text("", tag="resultado_texto")

#_____________________________________________________________________________
#_____________________________________________________________________________
    dpg.create_viewport(title="Solucionador de ecuaciones", width=700, height=450)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    interfaz()
