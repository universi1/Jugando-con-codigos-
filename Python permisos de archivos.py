Python

import os
import stat

def analizar_permisos_directorio(ruta_directorio):
    """
    Analiza y reporta los permisos de los archivos y subdirectorios en una ruta dada.
    """
    informe_permisos = {}
    if not os.path.isdir(ruta_directorio):
        return "Error: La ruta proporcionada no es un directorio."

    print(f"\n--- Análisis de Permisos para: {ruta_directorio} ---")
    for nombre in os.listdir(ruta_directorio):
        ruta_completa = os.path.join(ruta_directorio, nombre)
        try:
            st = os.stat(ruta_completa)
            modo = st.st_mode

            permisos = {
                'owner_read': bool(modo & stat.S_IRUSR),
                'owner_write': bool(modo & stat.S_IWUSR),
                'owner_execute': bool(modo & stat.S_IXUSR),
                'group_read': bool(modo & stat.S_IRGRP),
                'group_write': bool(modo & stat.S_IWGRP),
                'group_execute': bool(modo & stat.S_IXGRP),
                'others_read': bool(modo & stat.S_IROTH),
                'others_write': bool(modo & stat.S_IWOTH),
                'others_execute': bool(modo & stat.S_IXOTH),
                'is_dir': stat.S_ISDIR(modo),
                'is_file': stat.S_ISREG(modo)
            }
            informe_permisos[nombre] = permisos
            
            # Formato legible para el informe
            tipo = "D" if permisos['is_dir'] else "F"
            p_str = ""
            p_str += 'r' if permisos['owner_read'] else '-'
            p_str += 'w' if permisos['owner_write'] else '-'
            p_str += 'x' if permisos['owner_execute'] else '-'
            p_str += 'r' if permisos['group_read'] else '-'
            p_str += 'w' if permisos['group_write'] else '-'
            p_str += 'x' if permisos['group_execute'] else '-'
            p_str += 'r' if permisos['others_read'] else '-'
            p_str += 'w' if permisos['others_write'] else '-'
            p_str += 'x' if permisos['others_execute'] else '-'
            print(f"{tipo} {p_str} {nombre}")

        except OSError as e:
            informe_permisos[nombre] = f"Error al acceder a los permisos: {e}"
            print(f"Error al acceder a los permisos de '{nombre}': {e}")
    return informe_permisos

# Ejemplo de uso:
# Crea algunos archivos y un subdirectorio para probar
# Esto funciona en sistemas Unix/Linux. En Windows, las funciones de permisos son diferentes.
# Puedes ajustar los permisos manualmente en tu sistema operativo para probar diferentes escenarios.
if os.name == 'posix': # Solo para sistemas Unix-like
    os.makedirs("test_dir_auditoria/sub_dir", exist_ok=True)
    with open("test_dir_auditoria/archivo1.txt", "w") as f:
        f.write("Contenido 1")
    with open("test_dir_auditoria/archivo2.sh", "w") as f:
        f.write("#!/bin/bash\necho 'Hola'")
    os.chmod("test_dir_auditoria/archivo1.txt", 0o644) # rw-r--r--
    os.chmod("test_dir_auditoria/archivo2.sh", 0o755) # rwxr-xr-x
    os.chmod("test_dir_auditoria/sub_dir", 0o700) # rwx------

    informe_p = analizar_permisos_directorio("test_dir_auditoria")
    # print("\nInforme Detallado (Diccionario):")
    # print(informe_p)
else:
    print("\nEste ejemplo de permisos de archivo es más adecuado para sistemas Unix/Linux.")
    print("En Windows, la gestión de permisos (ACLs) es más compleja y requiere biblio