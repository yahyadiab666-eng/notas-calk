# consola.py
import biblioteca
import calculo

def procesar_materia_estudiante(nombre_estudiante, materia, notas):
    # 1. Guardar datos iniciales
    biblioteca.guardar_materia_estudiante(nombre_estudiante, materia, notas)
    
    # 2. Recalcular promedio general de ese estudiante
    db = biblioteca.cargar_base_datos()
    materias_estudiante = db[nombre_estudiante]["materias"]
    nuevo_promedio = calculo.calcular_promedio_general(materias_estudiante)
    
    # 3. Actualizar promedio y guardar
    db[nombre_estudiante]["promedio_general"] = nuevo_promedio
    biblioteca.guardar_base_datos(db)

def obtener_estudiantes():
    return biblioteca.cargar_base_datos()

def eliminar_registro_estudiante(nombre_estudiante):
    return biblioteca.eliminar_estudiante(nombre_estudiante)

def vaciar_aplicacion():
    biblioteca.resetear_todo()