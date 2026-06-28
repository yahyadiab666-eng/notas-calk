# biblioteca.py
import json
import os

ARCHIVO_DB = "base_datos.json"

def cargar_base_datos():
    """Lee el archivo JSON. Si no existe, devuelve un diccionario vacío."""
    if not os.path.exists(ARCHIVO_DB):
        return {}
    try:
        with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def guardar_base_datos(datos):
    """Guarda el diccionario completo en el archivo JSON."""
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def guardar_materia_estudiante(nombre_estudiante, materia, notas):
    """Guarda o actualiza las notas de una materia para un estudiante específico."""
    db = cargar_base_datos()
    
    # Si el estudiante no existe, lo crea
    if nombre_estudiante not in db:
        db[nombre_estudiante] = {"materias": {}, "promedio_general": 0.0}
        
    db[nombre_estudiante]["materias"][materia] = notas
    guardar_base_datos(db)

def eliminar_estudiante(nombre_estudiante):
    """Elimina por completo a un estudiante de la base de datos."""
    db = cargar_base_datos()
    if nombre_estudiante in db:
        del db[nombre_estudiante]
        guardar_base_datos(db)
        return True
    return False

def resetear_todo():
    """Borra todos los datos de la aplicación."""
    guardar_base_datos({})