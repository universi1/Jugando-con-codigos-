Python

import requests
import time

def comprobar_disponibilidad_servicio_web(url, timeout=5):
    """
    Comprueba la disponibilidad de un servicio web haciendo una solicitud GET.
    """
    try:
        inicio = time.time()
        response = requests.get(url, timeout=timeout)
        fin = time.time()
        tiempo_respuesta = (fin - inicio) * 1000 # en milisegundos
        
        estado = "Activo" if response.status_code == 200 else f"Error HTTP {response.status_code}"
        return estado, tiempo_respuesta, response.status_code
    except requests.exceptions.ConnectionError:
        return "Inaccesible (Error de Conexión)", 0, None
    except requests.exceptions.Timeout:
        return "Tiempo de Espera Excedido", timeout * 1000, None
    except requests.exceptions.RequestException as e:
        return f"Error Desconocido: {e}", 0, None

def generar_informe_disponibilidad(urls_servicios):
    """
    Comprueba la disponibilidad de una lista de URLs de servicios web y genera un informe.
    """
    informe = {}
    print("\n--- Informe de Disponibilidad de Servicios Web ---")
    for url in urls_servicios:
        estado, tiempo, status_code = comprobar_disponibilidad_servicio_web(url)
        informe[url] = {"estado": estado, "tiempo_respuesta_ms": tiempo, "codigo_estado_http": status_code}
        
        tiempo_str = f"{tiempo:.2f} ms" if tiempo > 0 else "N/A"
        print(f"URL: {url}")
        print(f"  Estado: {estado}")
        print(f"  Tiempo de Respuesta: {tiempo_str}")
        if status_code:
            print(f"  Código HTTP: {status_code}")
        print("-" * 30)
    return informe

# Ejemplo de uso:
servicios_a_auditar = [
    "https://www.google.com",
    "https://www.microsoft.com",
    "http://sitio-que-no-existe.xyz", # Este debería fallar
    "https://httpbin.org/status/500" # Simula un error de servidor
]

informe_web = generar_informe_disponibilidad(servicios_a_auditar)