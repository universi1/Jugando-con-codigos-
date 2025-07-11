Python

import csv

def analizar_transacciones_csv(ruta_archivo_csv, umbral_alto_valor=1000):
    """
    Extrae y analiza transacciones financieras de un archivo CSV.
    Calcula totales y reporta transacciones de alto valor.
    """
    transacciones = []
    transacciones_alto_valor = []
    total_ingresos = 0.0
    total_egresos = 0.0
    
    try:
        with open(ruta_archivo_csv, mode='r', newline='', encoding='utf-8') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for fila in lector_csv:
                try:
                    monto = float(fila['Monto'])
                    tipo = fila['Tipo'].strip().lower()
                    transacciones.append(fila)

                    if tipo == 'ingreso':
                        total_ingresos += monto
                    elif tipo == 'egreso':
                        total_egresos += monto
                    
                    if abs(monto) >= umbral_alto_valor:
                        transacciones_alto_valor.append(fila)
                except ValueError:
                    print(f"Advertencia: Monto inválido en la fila: {fila}")
                except KeyError as e:
                    print(f"Advertencia: Columna '{e}' no encontrada en la fila: {fila}")
                    
        print(f"\n--- Análisis de Transacciones desde: {ruta_archivo_csv} ---")
        print(f"Total de Ingresos: ${total_ingresos:,.2f}")
        print(f"Total de Egresos: ${total_egresos:,.2f}")
        print(f"Saldo Neto: ${total_ingresos - total_egresos:,.2f}")

        if transacciones_alto_valor:
            print(f"\n--- Transacciones de Alto Valor ( >= ${umbral_alto_valor:,.2f}) ---")
            for trans in transacciones_alto_valor:
                print(f"ID: {trans.get('ID', 'N/A')}, Fecha: {trans.get('Fecha', 'N/A')}, Descripción: {trans.get('Descripcion', 'N/A')}, Monto: ${float(trans.get('Monto', 0)):,.2f}, Tipo: {trans.get('Tipo', 'N/A')}")
        else:
            print(f"\nNo se encontraron transacciones de alto valor (>= ${umbral_alto_valor:,.2f}).")

        return {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "transacciones_alto_valor": transacciones_alto_valor
        }

    except FileNotFoundError:
        print(f"Error: El archivo CSV '{ruta_archivo_csv}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo CSV: {e}")
        return None

# Ejemplo de uso:
# Crear un archivo CSV de ejemplo
csv_contenido = """ID,Fecha,Descripcion,Monto,Tipo
1,2025-01-15,Venta de Producto A,500.00,Ingreso
2,2025-01-16,Pago de Alquiler,-1200.50,Egreso
3,2025-01-17,Servicios de Consultoria,2500.75,Ingreso
4,2025-01-18,Compra de Materiales,-300.00,Egreso
5,2025-01-19,Venta Grande,5000.00,Ingreso
6,2025-01-20,Salario Empleado,-800.00,Egreso
7,2025-01-21,Bonificacion,-2000.00,Egreso
"""
with open("transacciones.csv", "w", newline='', encoding='utf-8') as f:
    f.write(csv_contenido)

analisis_transacciones = analizar_transacciones_csv("transacciones.csv", umbral_alto