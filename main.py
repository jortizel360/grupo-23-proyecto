import sys
import csv
import time



class Tarea:
    def __init__(self, id: str, duracion: str, categoria: str) -> None:
        self.id: str = id
        self.duracion: int = duracion
        self.categoria: str = categoria 

        
class Recurso:
    def __init__(self, id: str, categorias: set[str]) -> None:
        self.id: str = id
        self.categorias: set[str] = categorias

class Asignacion:
    def __init__(self, id_tarea: str, id_recurso: str, inicio: int, fin: int) -> None:
        self.id_tarea: str = id_tarea
        self.id_recurso: str = id_recurso
        self.inicio: int = inicio
        self.fin: int = fin

def leer_tareas(ruta:str) -> list[Tarea]:
    lista_tareas: list[Tarea] = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(',')
            lista_tareas.append(Tarea(
                id=partes[0].strip(),
                duracion=int(partes[1].strip()),
                categoria=partes[2].strip()
            ))
    return lista_tareas
    

def leer_recursos(ruta: str) -> list[Recurso]:
    lista_recursos: list[Recurso] = []
    with open(ruta, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = [p.strip() for p in linea.split(',')]
            lista_recursos.append(Recurso(
                id=partes[0],
                categorias=set(partes[1:])
            ))
    return lista_recursos

    
def planificar(tareas: list[Tarea], recursos: list[Recurso]) -> list[Asignacion]:

    tareas_ordenadas: list[Tarea] = sorted(
        tareas, key=lambda t: t.duracion, reverse=True
    )

    recursos_por_categoria: dict[str, list[Recurso]] = {}
    for recurso in recursos:
        for cat in recurso.categorias:
            if cat not in recursos_por_categoria:
                recursos_por_categoria[cat] = []
            recursos_por_categoria[cat].append(recurso)

    tiempo_libre: dict[str, int] = {r.id: 0 for r in recursos}
    lista_asignaciones: list[Asignacion] = []

    for tarea in tareas_ordenadas:
        compatibles: list[Recurso] = recursos_por_categoria.get(tarea.categoria, [])

        mejor_recurso: Recurso = min(
            compatibles, key=lambda r: tiempo_libre[r.id]
        )

        inicio: int = tiempo_libre[mejor_recurso.id]
        fin: int = inicio + tarea.duracion

        lista_asignaciones.append(Asignacion(
            id_tarea=tarea.id,
            id_recurso=mejor_recurso.id,
            inicio=inicio,
            fin=fin
        ))
        tiempo_libre[mejor_recurso.id] = fin

    return lista_asignaciones

def busqueda_local(
    asignaciones: list[Asignacion],
    tareas: list[Tarea],
    recursos: list[Recurso],
    tiempo_inicio: float,
    limite: float = 8.5
) -> list[Asignacion]:
    tarea_por_id: dict[str, Tarea] = {t.id: t for t in tareas}
    mejoro = True
    while mejoro and (time.time() - tiempo_inicio) < limite:
        mejoro = False

        carga: dict[str, int] = {}
        for a in asignaciones:
            if a.id_recurso not in carga or a.fin > carga[a.id_recurso]:
                carga[a.id_recurso] = a.fin

        makespan_actual: int = max(carga.values())
        id_critico: str = max(carga, key=lambda r: carga[r])
        tareas_criticas: list[Asignacion] = sorted(
            [a for a in asignaciones if a.id_recurso == id_critico],
            key=lambda a: a.fin - a.inicio,
            reverse=True
        )
        for asig in tareas_criticas:
            if (time.time() - tiempo_inicio) >= limite:
                break
            tarea = tarea_por_id[asig.id_tarea]

            for recurso in recursos:
                if recurso.id == id_critico:
                    continue
                if tarea.categoria not in recurso.categorias:
                    continue
                fin_alt: int = max(
                    (a.fin for a in asignaciones if a.id_recurso == recurso.id),
                    default=0
                )
                nuevo_fin: int = fin_alt + tarea.duracion
                nuevo_fin_critico: int = max(
                    (a.fin for a in asignaciones
                     if a.id_recurso == id_critico and a.id_tarea != tarea.id),
                    default=0
                )
                nuevo_fin_alt: int = max(carga.get(recurso.id, 0), nuevo_fin)
                nuevo_makespan: int = max(
                    v for k, v in carga.items()
                    if k != id_critico and k != recurso.id
                )
                nuevo_makespan = max(nuevo_makespan, nuevo_fin_critico, nuevo_fin_alt)
                if nuevo_makespan < makespan_actual:
                    for a in asignaciones:
                        if a.id_tarea == tarea.id:
                            a.id_recurso = recurso.id
                            a.inicio = fin_alt
                            a.fin = nuevo_fin
                            break
                    mejoro = True
                    break

            if mejoro:
                break

    return asignaciones


def escribir_output(asignaciones: list[Asignacion], ruta: str) -> None:
    with open(ruta, 'w', encoding='utf-8') as archivo:
        for asignacion in asignaciones:
            linea = (f'{asignacion.id_tarea},{asignacion.id_recurso},'
                     f'{asignacion.inicio},{asignacion.fin}\n')
            archivo.write(linea)


def main() -> None:
    if len(sys.argv) < 2:
        print('Uso: python main.py <makespan_objetivo>')
        sys.exit(1)

    t_inicio: float = time.time()
    makespan_objetivo: int = int(sys.argv[1])

    tareas: list[Tarea] = leer_tareas('tareas.txt')
    recursos: list[Recurso] = leer_recursos('recursos.txt')

    asignaciones: list[Asignacion] = planificar(tareas, recursos)
    asignaciones = busqueda_local(asignaciones, tareas, recursos, t_inicio)

    makespan_obtenido: int = max(a.fin for a in asignaciones)
    escribir_output(asignaciones, 'output.txt')

    t_total: float = time.time() - t_inicio
    print(f'Tareas planificadas : {len(asignaciones)}')
    print(f'Makespan objetivo   : {makespan_objetivo}')
    print(f'Makespan obtenido   : {makespan_obtenido}')
    print(f'Tiempo CPU          : {t_total:.3f}s')
    if makespan_obtenido <= makespan_objetivo:
        print('Logramos el objetivo!')
    else:
        print('Makespan supera el objetivo.')

if __name__ == '__main__':
    main()
