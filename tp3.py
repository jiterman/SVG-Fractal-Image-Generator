import sys
from cola_pila import Cola, Pila, _Nodo
from tortuga import Tortuga
from math import radians

OPERACIONES_VALIDAS = 'FGfg+-|[]'
MENSAJE_AYUDA = 'Verificar que el archivo con la descripción del Sistema-L esté en formato sl, la cantidad de iteraciones sea un número natural y el archivo a escribir tenga el formato svg, en ese orden.'
MENSAJE_ABRIR_ARCHIVO = 'No se pudo cargar el archivo con la descripción del Sistema-L, verifique que no se encuentre abierto y que esté en la ruta correspondiente, y vuelva a intentar.'
MENSAJE_PROCESAR_ERROR = 'Verifique el ángulo, axioma o las reglas ingresados en el archivo de descripción del Sistema-L.\n* Ángulo: debe ser un número perteneciente al conjunto de los reales.\n* Axioma: puede contener cualquier caracter menos espacios.\n* Reglas: cada línea debe ser un par de operaciones dividido por un espacio. Ej.: F FF'
sys.argv.pop(0) #Elimina el nombre del archivo de la lista de comandos ingresados por el usuario

def main ():
    """Función principal del programa."""
    if not es_ingreso_valido():
        print(MENSAJE_AYUDA)
        return
    try:
        angulo, axioma, reglas = procesar_archivo()
    except (PermissionError, IOError, FileNotFoundError):
        print(MENSAJE_ABRIR_ARCHIVO)
        return
    except ValueError:
        print(MENSAJE_PROCESAR_ERROR)
        return
    traduccion = procesar_reglas(axioma, reglas)
    cola_dibujo, bordes = procesar_traduccion(traduccion, angulo)
    dibujar_svg(cola_dibujo, bordes)
    
def procesar_archivo ():
    """Abre el archivo sl pasado por comando, interpreta la información en el, asignando su información a variables
    que luego devuelve en caso de que esté todo correcto y si no eleva un ValueError."""
    with open (sys.argv[0]) as archivo_sl:
        angulo = archivo_sl.readline().rstrip('\n')
        axioma = archivo_sl.readline().rstrip('\n')
        reglas = {}
        if not son_angulo_axioma_validos (angulo, axioma):
            raise ValueError
        for linea in archivo_sl:
            linea = linea.rstrip('\n')
            predecesor, sucesor = linea.split(' ')
            reglas[predecesor] = sucesor
    return round(float(angulo) % 360, 1), axioma, reglas

def procesar_reglas (axioma, reglas):
    """Recibe el axioma y las reglas del sistema-l y según la cantidad de iteraciones que pidió el usuario devuelve
    una traducción filtrada """
    traduccion = axioma
    for _ in range(int(sys.argv[1])):
        actual = ''
        for e in traduccion:
            actual += reglas.get(e, e)
        traduccion = actual
    return filtrar_traduccion(traduccion)

def filtrar_traduccion (traduccion):
    '''Recibe una cadena y devuelve otra cadena que contiene los
    caracteres validos ya establecidos de la primera.'''
    filtrado = ''
    for e in traduccion:
        if e in OPERACIONES_VALIDAS:
            filtrado += e
    return filtrado

def son_angulo_axioma_validos (angulo, axioma):
    """Revisa que lo recibido sea un ángulo (indifrente de si es flotante o no)
    y que el axioma sea uno solo."""
    return (angulo.replace(".", "", 1).isdigit() and not ' ' in axioma)
    
def es_ingreso_valido ():
    """Chequea el ingreso del usuario. Revisa que reciba tres comandos, que el primero y
    el tercero sean de los formatos correspondientes, y la cantidad de iteraciones sea un
    número natural."""
    return (len(sys.argv) == 3 and sys.argv[0][-3:] == '.sl' and sys.argv[1].isdigit() and sys.argv[2][-4:] == '.svg')

def procesar_traduccion (traduccion, angulo):
    """Recibe la traducción (de las reglas y el axioma) y el angulo, dependiendo el caracter en la traducción la operación
    que realiza, devuelve la cola de dibujo y los extremos del mismo. """
    cola_dibujo, pila_tortugas = Cola(), Pila()
    pila_tortugas.apilar(Tortuga(radians(angulo)))
    bordes = [0, 0, 0, 0] #Almacena x mín, x máx, y mín, y máx. 
    for e in traduccion:
        tortuga_actual = pila_tortugas.ver_tope()
        if e in 'FGfg':
            x_ant, y_ant = tortuga_actual.x, tortuga_actual.y
            tortuga_actual.avanzar()
            x_act, y_act = pila_tortugas.ver_tope().x, pila_tortugas.ver_tope().y
            if e in 'FG':
                cola_dibujo.encolar((x_ant, y_ant, x_act, y_act))
            chequear_bordes_coordenadas(bordes, x_act, y_act)
        if e == '+': pila_tortugas.ver_tope().girar_der()
        if e == '-':
            pila_tortugas.ver_tope().girar_izq()
        if e == '|':
            pila_tortugas.ver_tope().cambiar_sentido()
        if e == '[':
            pila_tortugas.apilar(tortuga_actual.apilar_tortuga())
        if e == ']':
            pila_tortugas.desapilar()
    return cola_dibujo, bordes

def chequear_bordes_coordenadas (bordes, x, y):
    """"""
    bordes[0] = min(bordes[0], x)
    bordes[1] = min(bordes[1], y)
    bordes[2] = max(bordes[2], x)
    bordes[3] = max(bordes[3], y)        

def dibujar_svg (cola_dibujo, bordes):
    """Recibe la cola de dibujos y los bordes, con estos crea y escribe el archivo svg con el nombre pedido por comando."""
    ancho = bordes[2] - bordes[0]
    alto = bordes[3] - bordes[1]
    with open (sys.argv[2], 'w') as archivo_dibujo:
        archivo_dibujo.write(f'<svg viewBox="{bordes[0] - 5} {bordes[1] - alto * 0.1} {ancho + 5} {alto + alto * 0.2}" xmlns="http://www.w3.org/2000/svg">')
        while not cola_dibujo.esta_vacia():
            coordenadas = cola_dibujo.desencolar()
            archivo_dibujo.write(f'\n\t<line x1="{coordenadas[0]}" y1="{coordenadas[1]}" x2="{coordenadas[2]}" y2="{coordenadas[3]}" stroke-width="1" stroke="black" />')
        archivo_dibujo.write('\n</svg>')
    
main()