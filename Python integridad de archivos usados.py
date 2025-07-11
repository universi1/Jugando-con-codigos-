Python

import hashlib

def calcular_hash_sha256(ruta_archivo):
    """
    Calcula el hash SHA256 de un archivo dado.
    """
    hasher = hashlib.sha256()
    try:
        with open(ruta_archivo, 'rb') as f:
            for bloque in iter(lambda: f.read(4096), b''):
                hasher.update(bloque)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error al calcular el hash de '{ruta_archivo}': {e}")
        return None

def validar_integridad_archivos(archivos_a_validar):
    """
    Valida la integridad de una lista de archivos comparando sus hashes.
    'archivos_a_validar' es un diccionario {ruta_archivo: hash_esperado}.
    """
    resultados = {}
    print("\n--- Validación de Integridad de Archivos ---")
    for ruta_archivo, hash_esperado in archivos_a_validar.items():
        hash_actual = calcular_hash_sha256(ruta_archivo)
        if hash_actual is None:
            resultados[ruta_archivo] = "Archivo no encontrado o error"
        elif hash_actual == hash_esperado:
            resultados[ruta_archivo] = "INTEGRIDAD OK"
        else:
            resultados[ruta_archivo] = f"INTEGRIDAD COMPROMETIDA (Esperado: {hash_esperado}, Actual: {hash_actual})"
    return resultados

# Ejemplo de uso:
# Crea archivos de ejemplo
with open("documento_original.txt", "w") as f:
    f.write("Este es el contenido original del documento.")
with open("documento_modificado.txt", "w") as f:
    f.write("Este es el contenido modificado del documento.")

# Calcula el hash del archivo original (simulando un hash de línea base)
hash_original = calcular_hash_sha256("documento_original.txt")

archivos = {
    "documento_original.txt": hash_original,
    "documento_modificado.txt": "un_hash_diferente_esperado_simulado_para_demostrar_cambio", # Simula un hash esperado para el modificado
    "archivo_no_existente.txt": "cualquier_hash_simulado"
}

# Para la demostración, el hash_esperado para documento_modificado.txt será diferente.
# Si queremos que pase la validación, su hash_esperado debería ser:
# calcular_hash_sha256("documento_modificado.txt")

resultados_validacion = validar_integridad_archivos(archivos)
for archivo, resultado in resultados_validacion.items():
    print(f"Archivo: {archivo} -> {resultado}")