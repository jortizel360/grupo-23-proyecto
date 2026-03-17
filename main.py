import sys
import csv

class Tarea:
    def __init__(self, id: str, duracion: str):
        self.id = id
        self.duracion = duracion
        self.categoria: str = categoria 

        
class Recurso:
    def __init__(self, id: str, categoria: str) -> None:
        self.id: str = id
        self.categoria: str = categoria

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