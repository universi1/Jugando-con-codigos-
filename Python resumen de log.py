Python

def generar_resumen_logs(ruta_archivo_log):
    """
    Genera un resumen de los tipos de mensajes en un archivo de log.
    """
    resumen = {}
    try:
        with open(ruta_archivo_log, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    # Asumimos un formato simple: [NIVEL] Mensaje
                    if '[' in linea and ']' in linea:
                        nivel_inicio = linea.find('[') + 1
                        nivel_fin = linea.find(']')
                        nivel = linea[nivel_inicio:nivel_fin].upper()
                        resumen[nivel] = resumen.get(nivel, 0) + 1
                    else:
                        # Para líneas que no siguen el formato esperado
                        resumen['UNCLASSIFIED'] = resumen.get('UNCLASSIFIED', 0) + 1
        return resumen
    except FileNotFoundError:
        return "Error: El archivo de log no fue encontrado."
    except Exception as e:
        return f"Ocurrió un error al leer el archivo: {e}"

# Ejemplo de uso:
# Crea un archivo de log de ejemplo para probar
with open("ejemplo.log", "w") as f:
    f.write("[INFO] Usuario 'admin' ha iniciado sesión.\n")
    f.write("[WARNING] Intento de acceso fallido desde 192.168.1.100.\n")
    f.write("[ERROR] Error de base de datos: conexión perdida.\n")
    f.write("[INFO] Archivo descargado exitosamente.\n")
    f.write("[ERROR] Permiso denegado al intentar escribir en disco.\n")

resumen_log = generar_resumen_logs("ejemplo.log")
print("--- Resumen de Logs ---")
if isinstance(resumen_log, dict):
    for nivel, cantidad in resumen_log.items():
        print(f"Nivel {nivel}: {cantidad} ocurrencias")
else:
    print(resumen_log)