# main.py

from analisis_dxf import analizar_archivo_dxf
from precio import calcular_precio_total

if __name__ == "__main__":
    # Ruta del archivo DXF - Modifica la ruta para que apunte al archivo que deseas analizar
    ruta_completa = r"C:\Users\asistente.logistico\Desktop\DXF\1m.dxf"

    # Analizar el archivo DXF y obtener el área neta y el perímetro total
    area_neta_m2, perimetro_total_m = analizar_archivo_dxf(ruta_completa)

    # Verificar que se hayan obtenido valores válidos
    if area_neta_m2 is not None and perimetro_total_m is not None:
        # Datos de costos (puedes ajustarlos según tus necesidades)
        C_a = 90000   # Costo por unidad de área en pesos
        C_c = 6000    # Costo por unidad de corte en pesos

        # Cantidad de piezas (puedes cambiar este valor)
        n = 7        # Cantidad de piezas

        # Calcular el precio total
        resultado = calcular_precio_total(C_a, area_neta_m2, C_c, perimetro_total_m, n)

        # Mostrar los resultados
        
        print(f"Precio de Producción por Unidad (PP): ${resultado['precio_produccion']:,.2f}")
        print(f"Margen Aplicado: {resultado['margen_aplicado']:.2f}%")
        print(f"Precio Unitario antes de Descuento (PV): ${resultado['precio_unitario_antes_descuento']:,.2f}")
        print(f"Descuento Aplicado (D_n): {resultado['descuento_aplicado']}%")
        print(f"Precio Unitario después de Descuento (PV_d): ${resultado['precio_unitario']:,.2f}")
        print(f"Precio Total: ${resultado['precio_total']:,.2f}")
        print(f"Margen por Unidad: ${resultado['margen_por_unidad']:,.2f}")
        print(f"Margen Total: ${resultado['margen_total']:,.2f}")
        print(f"Porcentaje de Ganancia por Unidad: {resultado['porcentaje_ganancia_por_unidad']:.2f}%")
    else:
        print("No se pudo calcular el precio debido a errores en el análisis del archivo DXF.")
