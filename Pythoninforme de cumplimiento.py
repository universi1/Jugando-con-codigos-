Python

def generar_informe_cumplimiento(resultados_auditoria):
    """
    Genera un informe de cumplimiento de políticas de seguridad de la información
    basado en los resultados de varias auditorías.
    'resultados_auditoria' es un diccionario con hallazgos de diferentes auditorías.
    """
    informe = []
    cumplimiento_general = True

    print("\n--- INFORME DE CUMPLIMIENTO DE POLÍTICAS DE SEGURIDAD ---")
    print(f"Fecha del Informe: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # 1. Cumplimiento de Políticas de Contraseñas
    informe.append("\n## 1. Cumplimiento de Políticas de Contraseñas")
    if "contrasenas" in resultados_auditoria:
        fallos_contrasenas = [c['contrasena'] for c in resultados_auditoria["contrasenas"].values() if not c['cumple_politica']]
        if fallos_contrasenas:
            informe.append(f"Estado: **NO CONFORME**")
            informe.append(f"Se encontraron {len(fallos_contrasenas)} contraseñas que no cumplen la política:")
            for pwd in fallos_contrasenas:
                informe.append(f"  - '{pwd}'")
            cumplimiento_general = False
        else:
            informe.append("Estado: **CONFORME** (Todas las contraseñas revisadas cumplen la política).")
    else:
        informe.append("No se proporcionaron datos de auditoría de contraseñas.")

    # 2. Integridad de Archivos Críticos
    informe.append("\n## 2. Integridad de Archivos Críticos")
    if "integridad_archivos" in resultados_auditoria:
        archivos_comprometidos = [f for f, res in resultados_auditoria["integridad_archivos"].items() if "COMPROMETIDA" in res]
        if archivos_comprometidos:
            informe.append("Estado: **NO CONFORME**")
            informe.append(f"Se detectaron {len(archivos_comprometidos)} archivos con integridad comprometida:")
            for archivo in archivos_comprometidos:
                informe.append(f"  - '{archivo}'")
            cumplimiento_general = False
        else:
            informe.append("Estado: **CONFORME** (Integridad de archivos críticos verificada).")
    else:
        informe.append("No se proporcionaron datos de auditoría de integridad de archivos.")

    # 3. Detección de Accesos No Autorizados
    informe.append("\n## 3. Detección de Accesos No Autorizados")
    if "accesos_no_autorizados" in resultados_auditoria:
        if resultados_auditoria["accesos_no_autorizados"]:
            informe.append("Estado: **ALERTA**")
            informe.append(f"Se detectaron {len(resultados_auditoria['accesos_no_autorizados'])} eventos sospechosos/no autorizados:")
            for evento in resultados_auditoria['accesos_no_autorizados']:
                informe.append(f"  - Tipo: {evento['tipo'].title()}, Descripción: {evento['descripcion']}")
            cumplimiento_general = False
        else:
            informe.append("Estado: **CONFORME** (No se detectaron patrones significativos de acceso no autorizado).")
    else:
        informe.append("No se proporcionaron datos de auditoría de accesos no autorizados.")
    
    # 4. Resumen de Logs del Sistema (Solo para información, no necesariamente cumplimiento directo)
    informe.append("\n## 4. Resumen de Logs del Sistema (Informativo)")
    if "resumen_logs" in resultados_auditoria:
        informe.append("Conteo de niveles de log:")
        for nivel, cantidad in resultados_auditoria["resumen_logs"].items():
            informe.append(f"  - {nivel}: {cantidad}")
    else:
        informe.append("No se proporcionaron datos de resumen de logs.")

    # 5. Estado General de Cumplimiento
    informe.append("\n## 5. Estado General de Cumplimiento")
    if cumplimiento_general:
        informe.append("El sistema parece **CUMPLIR** con las políticas de seguridad de la información revisadas.")
    else:
        informe.append("El sistema presenta **HALLAZGOS DE NO CONFORMIDAD** que requieren atención inmediata.")
        
    print("\n".join(informe))
    return "\n".join(informe)

# Ejemplo de uso:
# Aquí se usarían los resultados de las funciones anteriores
# Para este ejemplo, simulamos algunos resultados:
resultados_para_informe = {
    "contrasenas": {
        "Contraseña_1": {"contrasena": "P@ssw0rd!", "cumple_politica": True, "detalles": {}},
        "Contraseña_2": {"contrasena": "weak", "cumple_politica": False, "detalles": {'cumple_longitud': False}},
    },
    "integridad_archivos": {
        "archivo_seguro.txt": "INTEGRIDAD OK",
        "archivo_comprometido.dll": "INTEGRIDAD COMPROMETIDA (Esperado: abc, Actual: xyz)"
    },
    "accesos_no_autorizados": [
        {"tipo": "multiple_fallo", "ip": "192.168.1.50", "descripcion": "Múltiples intentos de inicio de sesión fallidos desde 192.168.1.50"}
    ],
    "resumen_logs": {
        "INFO": 100,
        "WARNING": 20,
        "ERROR": 5
    }
}

informe_final = generar_informe_cumplimiento(resultados_para_informe)