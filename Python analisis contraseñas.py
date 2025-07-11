Python

import re

def analizar_contrasena(contrasena, politica):
    """
    Analiza una contraseña contra una política de seguridad.
    Política es un diccionario con reglas como:
    {
        'min_longitud': 8,
        'requiere_mayuscula': True,
        'requiere_minuscula': True,
        'requiere_numero': True,
        'requiere_caracter_especial': True,
        'caracteres_especiales': r'[!@#$%^&*()_+={}\[\]:;"\'|<,>.?/~`]'
    }
    """
    resultados = {
        "cumple_longitud": len(contrasena) >= politica.get('min_longitud', 0),
        "cumple_mayuscula": True if not politica.get('requiere_mayuscula', False) else bool(re.search(r'[A-Z]', contrasena)),
        "cumple_minuscula": True if not politica.get('requiere_minuscula', False) else bool(re.search(r'[a-z]', contrasena)),
        "cumple_numero": True if not politica.get('requiere_numero', False) else bool(re.search(r'[0-9]', contrasena)),
        "cumple_especial": True if not politica.get('requiere_caracter_especial', False) else bool(re.search(politica.get('caracteres_especiales', r''), contrasena))
    }
    
    cumple_todas = all(resultados.values())
    return cumple_todas, resultados

def verificar_politicas_contrasena(lista_contrasenas, politica):
    """
    Verifica una lista de contraseñas contra una política dada.
    """
    informe_cumplimiento = {}
    print("\n--- Análisis de Cumplimiento de Políticas de Contraseñas ---")
    for i, contrasena in enumerate(lista_contrasenas):
        cumple, detalles = analizar_contrasena(contrasena, politica)
        informe_cumplimiento[f"Contraseña_{i+1}"] = {"contrasena": contrasena, "cumple_politica": cumple, "detalles": detalles}
        
        estado = "CUMPLE" if cumple else "NO CUMPLE"
        print(f"Contraseña '{contrasena}': {estado}")
        if not cumple:
            for regla, resultado in detalles.items():
                if not resultado:
                    print(f"  - Falló: {regla.replace('_', ' ')}")
        print("-" * 30)
    return informe_cumplimiento

# Ejemplo de política de seguridad (ajusta según tus necesidades)
politica_ejemplo = {
    'min_longitud': 10,
    'requiere_mayuscula': True,
    'requiere_minuscula': True,
    'requiere_numero': True,
    'requiere_caracter_especial': True,
    'caracteres_especiales': r'[!@#$%^&*()_+=\-\[\]{};:\'",.<>/?`~]'
}

contrasenas_a_auditar = [
    "Password123!",       # Cumple
    "short",              # No cumple longitud
    "NoNumbers!",         # No cumple número
    "no_upper_case123",   # No cumple mayúscula
    "TEST123456",         # No cumple minúscula
    "Segura@2025"         # Cumple
]

informe_contrasenas = verificar_politicas_contrasena(contrasenas_a_auditar, politica_eje