import sys
import csv

class Tarea:
    def __init__(self, id: str, duracion: str, categoria: str):
        self.id = id
        self.duracion = duracion
        self.categoria: str = categoria 

        
class Recurso:
    def __init__(self, id: str, categoria: str) -> None:
        self.id: str = id
        self.categoria: str = categoria

class Asignacion:
    def __init__(self, id_tarea: str, id_recurso: str, inicio: int, fin: int) -> None:
        self.id_tarea = id_tarea
        self.id_recurso = id_recurso
        self.inicio = inicio
        self.fin = fin
class GestorTareas:
    def __init__(self):
        self.tareas = []
        self.recursos = []
    
    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
    
    def agregar_recurso(self, recurso):
        self.recursos.append(recurso)
    
    def cargar_desde_csv(self, archivo):
        
        pass
    
    def guardar_a_csv(self, archivo):
        
        pass
    
    def leer_tareas(ruta:str) -> list[Tarea]:
        tareas = []
        with open(ruta, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            for row in reader:
                tarea = Tarea(id=row[0], duracion=row[1], categoria=row[2])
                tareas.append(tarea)
        return tareas
    
    def leer_recursos(self, ruta: str) -> list[Recurso]:
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