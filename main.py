import sys
import csv

class Tarea:
    def __init__(self, id: str, duracion: int, categoria: str):
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

def leer_tareas(ruta:str) -> list[Tarea]:
    tareas = []
    with open(ruta, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            tarea = Tarea(id=row[0], duracion=int(row[1]), categoria=row[2])
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
    )
    
    lista_asignaciones: list[Asignacion] = []
    for tarea in tareas_ordenadas:
        recursos_compatibles: list[Recurso] = []
        for recurso in recursos:
            if recurso.categoria == tarea.categoria:
                recursos_compatibles.append(recurso)
        
        if not recursos_compatibles:
            print(f'Advertencia: No hay recursos compatibles para la tarea {tarea.id}. Se omitirá.')
            continue

        mejor_recurso: Recurso = min(
            recursos_compatibles,
            key=lambda r: tiempo_libre[r.id]
        )
        inicio: int = tiempo_libre[mejor_recurso.id]
        fin: int = inicio + tarea.duracion

        asignacion_nueva = Asignacion(
            id_tarea=tarea.id,
            id_recurso=mejor_recurso.id,
            inicio=inicio,
            fin=fin
        )
        lista_asignaciones.append(asignacion_nueva)
        tiempo_libre[mejor_recurso.id] = fin

    return lista_asignaciones

def escribir_output(asignaciones: list[Asignacion], ruta: str) -> None:
    with open(ruta, 'w', encoding='utf-8') as archivo:
        for asignacion in asignaciones:
            linea = (f'{asignacion.id_tarea},{asignacion.id_recurso},'
                     f'{asignacion.inicio},{asignacion.fin}\n')
            archivo.write(linea)

def main() -> None:
    if len(sys.argv) < 2:
        print('Error: falta el makespan objetivo.')
        sys.exit(1)

    makespan_objetivo: int = int(sys.argv[1])
    tareas: list[Tarea] = leer_tareas('tareas.txt')
    recursos: list[Recurso] = leer_recursos('recursos.txt')
    asignaciones: list[Asignacion] = planificar(tareas, recursos)
    makespan_obtenido: int = max(a.fin for a in asignaciones)

    escribir_output(asignaciones, 'output.txt')

    print(f'Makespan objetivo : {makespan_objetivo}')
    print(f'Makespan obtenido : {makespan_obtenido}')
    if makespan_obtenido <= makespan_objetivo:
        print('Logramos el objetivo!')

if __name__ == '__main__':
    main()