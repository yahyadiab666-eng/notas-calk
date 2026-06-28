# calculo.py

def calcular_promedio_materia(notas):
    if not notas:
        return 0.0
    return sum(notas) / len(notas)

def calcular_promedio_general(materias_dict):
    if not materias_dict:
        return 0.0
    promedios = [sum(notas)/len(notas) for notas in materias_dict.values() if notas]
    if not promedios:
        return 0.0
    return sum(promedios) / len(promedios)