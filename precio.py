# precio.py

def calcular_margen_lineal(PP, PP_max=500000):
    """
    Calcula el margen de ganancia de forma lineal en función del PP.
    """
    if PP <= PP_max:
        margen = 0.60 - (0.30 * (PP / PP_max))
    else:
        margen = 0.30
    return margen

def calcular_descuento_maximo(margen):
    """
    Calcula el descuento máximo permitido en función del margen de ganancia.
    """
    # Relacionamos el descuento máximo con el margen de forma lineal
    # Descuento máximo disminuye de 55% a 25% mientras el margen disminuye de 60% a 30%
    descuento_maximo = 0.9167 * (margen * 100) - 0.7143  # Resultado en porcentaje

    # Aseguramos que el descuento máximo esté entre 25% y 55%
    descuento_maximo = max(min(descuento_maximo, 55), 25)
    return descuento_maximo

def calcular_precio_total(C_a, area, C_c, corte, n):
    """
    Calcula el precio total basado en los parámetros proporcionados, con margen de ganancia y descuentos variables.
    """
    # Paso 1: Calcular el Precio de Producción por Unidad (PP)
    PP = (C_a * area) + (C_c * corte)

    # Paso 2: Calcular el Margen de Ganancia Lineal
    margen = calcular_margen_lineal(PP)
    
    # Paso 3: Calcular el Precio de Venta antes de Descuento (PV)
    PV = PP / (1 - margen)

    # Paso 4: Calcular el Descuento Máximo en función del margen
    descuento_maximo = calcular_descuento_maximo(margen)

    # Paso 5: Aplicar la estructura de descuentos según el margen de ganancia
    amount = n  # Cantidad de piezas

    # Definir la estructura de descuentos
    if amount >= 200:
        D_n = descuento_maximo
    elif amount >= 150:
        D_n = descuento_maximo - 5
    elif amount >= 100:
        D_n = descuento_maximo - 10
    elif amount >= 50:
        D_n = descuento_maximo - 20
    elif amount >= 10:
        D_n = descuento_maximo - 25
    elif amount >= 2:
        D_n = descuento_maximo - 35
    else:
        D_n = 0

    # Aseguramos que el descuento no sea negativo
    D_n = max(D_n, 0)

    # Paso 6: Calcular el Precio Unitario después del Descuento (PV_d)
    PV_d = PV * (1 - D_n / 100)

    # Paso 7: Calcular el Precio Total
    precio_total = PV_d * n

    # **Implementar el precio total mínimo de $59,000**
    if precio_total < 59000:
        precio_total = 59000
        PV_d = precio_total / n  # Ajustamos el precio unitario en consecuencia

    # Calcular el Margen por Unidad y el Margen Total
    margen_por_unidad = PV_d - PP
    margen_total = margen_por_unidad * n

    # Calcular el Porcentaje de Ganancia por Unidad
    if PV_d != 0:
        porcentaje_ganancia_por_unidad = (margen_por_unidad / PV_d) * 100
    else:
        porcentaje_ganancia_por_unidad = 0

    return {
        'precio_produccion': PP,
        'precio_unitario_antes_descuento': PV,
        'descuento_aplicado': D_n,
        'precio_unitario': PV_d,
        'precio_total': precio_total,
        'margen_por_unidad': margen_por_unidad,
        'margen_total': margen_total,
        'porcentaje_ganancia_por_unidad': porcentaje_ganancia_por_unidad,
        'margen_aplicado': margen * 100  # Margen aplicado en porcentaje
    }
