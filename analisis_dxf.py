# analisis_dxf.py

import ezdxf
from math import sqrt, pi

def calcular_area_polilinea(polilinea):
    """Calcula el área de una polilínea cerrada."""
    if not polilinea.is_closed:
        print("La polilínea no está cerrada, no se puede calcular el área.")
        return 0

    area = 0
    puntos = polilinea.get_points()
    n = len(puntos)
    
    for i in range(n):
        x1, y1 = puntos[i][:2]  # Coordenadas (x1, y1)
        x2, y2 = puntos[(i + 1) % n][:2]  # Coordenadas del siguiente punto (x2, y2)
        area += (x1 * y2 - x2 * y1)
    
    area = abs(area) / 2
    return area

def calcular_perimetro_polilinea(polilinea):
    """Calcula el perímetro de una polilínea cerrada."""
    if not polilinea.is_closed:
        print("La polilínea no está cerrada, no se puede calcular el perímetro.")
        return 0

    perimetro = 0
    puntos = polilinea.get_points()
    n = len(puntos)

    for i in range(n):
        x1, y1 = puntos[i][:2]  # Coordenadas (x1, y1)
        x2, y2 = puntos[(i + 1) % n][:2]  # Coordenadas del siguiente punto (x2, y2)
        distancia = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        perimetro += distancia
    
    return perimetro

def calcular_dimensiones_polilinea(polilinea):
    """Calcula el ancho y el alto de una polilínea cerrada."""
    puntos = polilinea.get_points()
    x_min = min(punto[0] for punto in puntos)
    x_max = max(punto[0] for punto in puntos)
    y_min = min(punto[1] for punto in puntos)
    y_max = max(punto[1] for punto in puntos)
    
    ancho = x_max - x_min
    alto = y_max - y_min
    
    return ancho, alto

def detectar_polilineas_abiertas(msp):
    """Detecta y lanza una advertencia si hay polilíneas abiertas."""
    polilineas_abiertas = []
    for polilinea in msp.query('LWPOLYLINE'):
        if not polilinea.is_closed:
            polilineas_abiertas.append(polilinea)
    
    if polilineas_abiertas:
        print(f"¡Advertencia! Se encontraron {len(polilineas_abiertas)} polilíneas abiertas.")
    else:
        print("No se encontraron polilíneas abiertas.")

def punto_dentro_polilinea(punto, polilinea_externa):
    """Verifica si un punto está dentro de una polilínea cerrada."""
    puntos_externa = polilinea_externa.get_points()
    n = len(puntos_externa)
    x, y = punto
    dentro = False

    # Algoritmo del rayo para determinar si el punto está dentro del polígono
    for i in range(n):
        x1, y1 = puntos_externa[i][:2]
        x2, y2 = puntos_externa[(i + 1) % n][:2]
        if y1 == y2:
            continue  # Evitar división por cero
        if ((y1 > y) != (y2 > y)):
            x_intersect = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < x_intersect:
                dentro = not dentro

    return dentro

def validar_figuras(polilinea_externa, polilineas_internas, circulos_internos):
    """Valida si las figuras internas están contenidas dentro de la polilínea externa."""
    # Validar que las polilíneas internas están dentro de la polilínea externa
    for polilinea in polilineas_internas:
        puntos_interna = polilinea.get_points()
        for punto in puntos_interna:
            if not punto_dentro_polilinea(punto[:2], polilinea_externa):
                print("¡Advertencia! Hay polilíneas que se salen de la polilínea externa.")
                return False

    # Validar que los círculos internos están dentro de la polilínea externa
    for circulo in circulos_internos:
        centro = circulo.dxf.center
        x_centro = centro[0]
        y_centro = centro[1]
        # Verificar si el centro del círculo está dentro de la polilínea externa
        if not punto_dentro_polilinea((x_centro, y_centro), polilinea_externa):
            print("¡Advertencia! Hay círculos cuyo centro se sale de la polilínea externa.")
            return False
        # Opcional: Verificar si el círculo completo está dentro de la polilínea externa
        # Esto puede requerir una verificación más detallada

    return True

def calcular_area_circulo(circulo):
    """Calcula el área de un círculo."""
    radio = circulo.dxf.radius
    area = pi * radio ** 2
    return area

def calcular_perimetro_circulo(circulo):
    """Calcula la circunferencia de un círculo."""
    radio = circulo.dxf.radius
    perimetro = 2 * pi * radio
    return perimetro

def analizar_archivo_dxf(ruta_completa):
    """
    Función para analizar y calcular el área neta, el perímetro y realizar validaciones de seguridad en un archivo DXF.
    Retorna el área neta en metros cuadrados y el perímetro total en metros.
    """
    try:
        # Cargar el archivo DXF
        doc = ezdxf.readfile(ruta_completa)
        msp = doc.modelspace()
        
        # Detectar polilíneas abiertas
        detectar_polilineas_abiertas(msp)
        
        # Almacenar áreas y perímetros
        areas_polilineas = []
        perimetro_total = 0

        # Analizar polilíneas cerradas (LWPOLYLINE)
        for polilinea in msp.query('LWPOLYLINE'):
            if polilinea.is_closed:
                area = calcular_area_polilinea(polilinea)
                perimetro = calcular_perimetro_polilinea(polilinea)
                areas_polilineas.append({"polilinea": polilinea, "area": area, "perimetro": perimetro})
                perimetro_total += perimetro

        if not areas_polilineas:
            print("No se encontraron polilíneas cerradas para analizar.")
            return None, None  # Retornamos None si no hay datos

        # Encontrar la polilínea externa (la más grande)
        polilinea_externa = max(areas_polilineas, key=lambda p: p["area"])
        area_externa = polilinea_externa["area"]
        ancho, alto = calcular_dimensiones_polilinea(polilinea_externa["polilinea"])

        print(f"Dimensiones de la polilínea externa: Ancho = {ancho/1000:.3f} metros, Alto = {alto/1000:.3f} metros.")
        print(f"Área de la polilínea externa: {area_externa/1000000:.6f} metros cuadrados.")

        # Calcular áreas de las polilíneas internas y sumar el perímetro total
        area_interna_total = 0
        polilineas_internas = []
        for polilinea in areas_polilineas:
            if polilinea != polilinea_externa:
                polilineas_internas.append(polilinea["polilinea"])
                area_interna_total += polilinea["area"]
                perimetro_total += polilinea["perimetro"]

        # Analizar círculos
        circulos_internos = []
        for circulo in msp.query('CIRCLE'):
            centro = circulo.dxf.center
            x_centro = centro[0]
            y_centro = centro[1]
            # Verificar si el centro del círculo está dentro de la polilínea externa
            if punto_dentro_polilinea((x_centro, y_centro), polilinea_externa["polilinea"]):
                # El círculo está dentro de la polilínea externa
                area = calcular_area_circulo(circulo)
                perimetro = calcular_perimetro_circulo(circulo)
                area_interna_total += area
                perimetro_total += perimetro
                circulos_internos.append(circulo)
            else:
                print("Se encontró un círculo fuera de la polilínea externa.")

        # Validar si las figuras internas están contenidas en la polilínea externa
        if validar_figuras(polilinea_externa["polilinea"], polilineas_internas, circulos_internos):
            print("Todas las figuras están correctamente contenidas dentro de la polilínea externa.")
        
        # Calcular el área neta (área externa - áreas internas)
        area_neta = area_externa - area_interna_total
        print(f"Área neta de la pieza: {area_neta/1000000:.6f} metros cuadrados.")
        print(f"Perímetro total de todas las entidades: {perimetro_total/1000:.3f} metros.")  # Asumiendo milímetros

        # Retornar el área neta y el perímetro total en metros
        return area_neta / 1_000_000, perimetro_total / 1_000

    except Exception as e:
        print(f"Ocurrió un error al analizar el archivo: {e}")
        return None, None  # Retornamos None si hay un error
