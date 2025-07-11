Python

import socket

def escanear_puerto(host, puerto, timeout=1):
    """
    Intenta conectar a un puerto específico para ver si está abierto.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((host, puerto))
        sock.close()
        return resultado == 0  # 0 significa conexión exitosa
    except socket.gaierror:
        return "Hostname no resuelto"
    except Exception as e:
        return f"Error: {e}"

def auditar_configuracion_red(objetivo, puertos_comunes):
    """
    Audita puertos comunes en un objetivo dado y reporta su estado.
    """
    informe_vulnerabilidades = {}
    print(f"\n--- Auditoría Básica de Puertos para: {objetivo} ---")
    for puerto in puertos_comunes:
        estado = escanear_puerto(objetivo, puerto)
        if estado is True:
            informe_vulnerabilidades[puerto] = "ABIERTO (Posible Vulnerabilidad)"
            print(f"Puerto {puerto}: ABIERTO")
        elif estado is False:
            informe_vulnerabilidades[puerto] = "CERRADO"
            print(f"Puerto {puerto}: CERRADO")
        else:
            informe_vulnerabilidades[puerto] = f"Error: {estado}"
            print(f"Puerto {puerto}: Error ({estado})")
    return informe_vulnerabilidades

# Ejemplo de uso:
# NOTA: Realizar escaneos de puertos en redes sin permiso puede ser ilegal.
# Usa esto solo en tus propias redes o con autorización explícita.
objetivo_ip = "127.0.0.1" # Tu propia máquina local
puertos_a_escanear = [22, 80, 443, 3306, 8080] # SSH, HTTP, HTTPS, MySQL, Proxy/Web

resultados_auditoria_red = auditar_configuracion_red(objetivo_ip, puertos_a_escanear)
# print("\nInforme Detallado (Diccionario):")
# print(resultados_auditoria_red)