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

class Asignacion:
    def __init__(self, id_tarea: str, id_recurso: str, inicio: int, fin: int) -> None:
        self.id_tarea = id_tarea
        self.id_recurso = id_recurso
        self.inicio = inicio
        self.fin = fin