import sys
import csv
import time 


class Tarea:
    def __init__(self, id: str, duracion: str, categoria: str):
        self.id = id
        self.duracion = duracion
        self.categoria: str = categoria 

        
class Recurso:
    def __init__(self, id: str, categorias: set[str]) -> None:
        self.id: str = id
        self.categorias: set[str] = categorias

class Asignacion:
    def __init__(self, id_tarea: str, id_recurso: str, inicio: int, fin: int) -> None:
        self.id_tarea = id_tarea
        self.id_recurso = id_recurso
        self.inicio = inicio
        self.fin = fin

def leer_tareas(ruta:str) -> list[Tarea]:
    tareas = []
    with open(ruta, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar la cabecera
        for row in reader:
            tarea = Tarea(id=row[0], duracion=row[1], categoria=row[2])
            tareas.append(tarea)
    return tareas
    
def leer_recursos(ruta: str) -> list[Recurso]:
    recursos: list[Recurso] = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(',')
            recursos.append(Recurso(
                id=partes[0].strip(),
                categoria=partes[1].strip()
            ))
    return recursos
    
def planificar(tareas: list[Tarea], recursos: list[Recurso]) -> list[Asignacion]:
    tiempo_libre: dict[str, int] = {}
    for recurso in recursos:
        tiempo_libre[recurso.id] = 0

tareas_ordenadas: list[Tarea] = sorted(
    tareas,
key=lambda t: t.duracion,
reverse=True



   
