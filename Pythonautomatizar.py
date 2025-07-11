Python

def revisar_politicas_configuracion(ruta_archivo_config, politicas_requeridas):
    """
    Revisa un archivo de configuración de servidor para el cumplimiento de políticas de seguridad.
    'politicas_requeridas' es un diccionario de {'parametro': 'valor_esperado'}.
    """
    hallazgos = {}
    cumple_todo = True

    print(f"\n--- Revisión de Políticas de Configuración para: {ruta_archivo_config} ---")

    try:
        with open(ruta_archivo_config, 'r') as f:
            contenido_config = f.readlines()
            
        for parametro, valor_esperado in politicas_requeridas.items():
            encontrado = False
            for linea in contenido_config:
                linea_limpia = linea.strip()
                if linea_limpia.startswith(parametro):
                    # Asumiendo formato simple "Parametro=Valor" o "Parametro Valor"
                    # Esto puede necesitar ser más robusto para configuraciones complejas
                    partes = re.split(r'[:=\s]+', linea_limpia, 1)
                    if len(partes) > 1 and partes[0] == parametro:
                        valor_actual = partes[1].strip()
                        if valor_actual.lower() == str(valor_esperado).lower():
                            hallazgos[parametro] = "CUMPLE"
                            print(f"Parámetro '{parametro}': CUMPLE (Valor: {valor_actual})")
                        else:
                            hallazgos[parametro] = f"NO CUMPLE (Esperado: {valor_esperado}, Actual: {valor_actual})"
                            print(f"Parámetro '{parametro}': NO CUMPLE (Esperado: {valor_esperado}, Actual: {valor_actual})")
                            cumple_todo = False
                        encontrado = True
                        break # Ya encontramos el parámetro, pasamos al siguiente
            if not encontrado:
                hallazgos[parametro] = "NO ENCONTRADO EN CONFIGURACIÓN"
                print(f"Parámetro '{parametro}': NO ENCONTRADO (Debería ser: {valor_esperado})")
                cumple_todo = False

    except FileNotFoundError:
        print(f"Error: El archivo de configuración '{ruta_archivo_config}' no fue encontrado.")
        return None, False
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo de configuración: {e}")
        return None, False

    print("\n--- Resumen de Cumplimiento de Configuración ---")
    if cumple_todo:
        print("Todas las políticas de seguridad de configuración revisadas están en cumplimiento.")
    else:
        print("Se encontraron una o más políticas de seguridad de configuración que no cumplen.")
        
    return hallazgos, cumple_todo

# Ejemplo de un archivo de configuración de servidor simulado (ej. sshd_config, apache2.conf)
config_simulada = """
# Configuración SSH
Port 22
PermitRootLogin no
PasswordAuthentication yes
MaxAuthTries 6
UseDNS no
LoginGraceTime 120
StrictModes yes

# Configuración de red
EnableIPv6 yes
BindAddress 0.0.0.0

# Otras políticas
MinPasswordLength 12
"""
with open("server_config.conf", "w") as f:
    f.write(config_simulada)

# Políticas de seguridad que un auditor podría querer verificar
politicas_servidor = {
    "PermitRootLogin": "no",       # No permitir acceso directo como root
    "PasswordAuthentication": "no", # Preferir autenticación por clave
    "MaxAuthTries": "3",           # Limitar intentos de autenticación fallidos
    "UseDNS": "no",                # Evitar retrasos por DNS lookups
    "MinPasswordLength": "12",     # Longitud mínima de contraseña
    "EnableIPv6": "yes",           # Asegurar IPv6 habilitado
    "" # Ejemplo de un parámetro que no existe
}

hallazgos_config, estado_cumplimiento = revisar_politicas_configuracion("server_config.conf