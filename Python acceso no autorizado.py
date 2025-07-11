Python

import re

def detectar_accesos_no_autorizados(ruta_archivo_log, umbral_fallos=3):
    """
    Detecta patrones de accesos no autorizados (fallos de inicio de sesión)
    en un archivo de log, identificando intentos múltiples desde la misma IP.
    """
    fallos_por_ip = {}
    eventos_sospechosos = []

    try:
        with open(ruta_archivo_log, 'r') as f:
            for i, linea in enumerate(f, 1):
                linea = linea.strip()
                # Patrón para detectar "fallo de inicio de sesión" y una IP
                # Esto es un ejemplo, el patrón real dependerá del formato de tus logs
                match = re.search(r'(failed|fail|failure|denied).*from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', linea, re.IGNORECASE)
                if match:
                    ip_atacante = match.group(2)
                    fallos_por_ip[ip_atacante] = fallos_por_ip.get(ip_atacante, 0) + 1
                    if fallos_por_ip[ip_atacante] >= umbral_fallos:
                        # Para evitar duplicados en eventos_sospechosos si ya se reportó
                        if not any(e['ip'] == ip_atacante for e in eventos_sospechosos if e['tipo'] == 'multiple_fallo'):
                            eventos_sospechosos.append({
                                "tipo": "multiple_fallo",
                                "ip": ip_atacante,
                                "descripcion": f"Múltiples ({fallos_por_ip[ip_atacante]}) intentos de inicio de sesión fallidos desde {ip_atacante}"
                            })
                
                # Otros patrones (ej. "access denied" sin IP específica, o cambios en archivos críticos)
                if re.search(r'access denied to (.*)', linea, re.IGNORECASE):
                    recurso = re.search(r'access denied to (.*)', linea, re.IGNORECASE).group(1)
                    eventos_sospechosos.append({
                        "tipo": "acceso_denegado",
                        "descripcion": f"Acceso denegado a recurso: {recurso} en línea {i}"
                    })
                        
        print("\n--- Detección de Accesos No Autorizados ---")
        if eventos_sospechosos:
            for evento in eventos_sospechosos:
                print(f"- **{evento['tipo'].replace('_', ' ').title()}**: {evento['descripcion']}")
        else:
            print("No se detectaron patrones de acceso no autorizado significativos.")
        
        return eventos_sospechosos
    except FileNotFoundError:
        print(f"Error: El archivo de log '{ruta_archivo_log}' no fue encontrado.")
        return []
    except Exception as e:
        print(f"Ocurrió un error al procesar el archivo de log: {e}")
        return []

# Ejemplo de log de sistema simulado
log_simulado = """
Jan 1 00:00:01 server sshd[123]: Accepted password for user1 from 192.168.1.1
Jan 1 00:00:02 server sshd[124]: Failed password for invalid user from 192.168.1.10
Jan 1 00:00:03 server sshd[125]: Failed password for root from 192.168.1.10
Jan 1 00:00:04 server sshd[126]: Failed password for admin from 192.168.1.10
Jan 1 00:00:05 server kernel: User 'guest' tried to access /var/log/critical.log, access denied.
Jan 1 00:00:06 server sshd[127]: Failed password for userX from 192.168.1.11
Jan 1 00:00:07 server sshd[128]: Failed password for userY from 192.168.1.11
Jan 1 00:00:08 server kernel: Another access denied to /etc/shadow.
"""
with open("syslog_auditoria.log", "w") as f:
    f.write(log_simulado)

detecciones = detectar_accesos_no_autorizados("syslog_auditoria.log", umbral_fallos=3)