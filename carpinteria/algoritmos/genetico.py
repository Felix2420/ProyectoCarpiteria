# genetico.py — Algoritmo Genético Tradicional (GA) para optimización de layout.

import random
import copy
from distancias import calcular_costo_total
from layout import Layout
from config import MAQUINAS, SECUENCIA, GA_PARAMS


def _crear_individuo(celdas_disponibles: list) -> list:
    """
    Crea un individuo aleatorio (permutación de celdas para las 7 máquinas).

    Parámetros:
        celdas_disponibles: lista de celdas libres

    Retorna:
        Lista de 7 celdas (una por máquina, en el mismo orden que MAQUINAS).
    """
    return random.sample(celdas_disponibles, len(MAQUINAS))


def _decodificar(individuo: list) -> dict:
    """
    Convierte lista de celdas en diccionario {id_maquina: celda}.

    Parámetros:
        individuo: lista de tuplas de celdas

    Retorna:
        dict {id_maquina: (col, fila)}
    """
    return {MAQUINAS[i]: individuo[i] for i in range(len(MAQUINAS))}


def _fitness(individuo: list, metrica: str, layout: Layout) -> float:
    """
    Evalúa el costo total de un individuo (menor es mejor).

    Parámetros:
        individuo: lista de celdas
        metrica:   'manhattan' o 'euclidiana'
        layout:    instancia de Layout

    Retorna:
        Costo total de recorrido.
    """
    return calcular_costo_total(_decodificar(individuo), SECUENCIA, metrica, layout)


def _seleccion_torneo(poblacion: list, costos: list, k: int) -> list:
    """
    Selección por torneo: elige k candidatos al azar y retorna el mejor.

    Parámetros:
        poblacion: lista de individuos
        costos:    lista de costos correspondientes
        k:         tamaño del torneo

    Retorna:
        El individuo ganador del torneo.
    """
    candidatos = random.sample(range(len(poblacion)), k)
    ganador = min(candidatos, key=lambda i: costos[i])
    return copy.deepcopy(poblacion[ganador])


def _cruce_ox(padre1: list, padre2: list) -> tuple:
    """
    Cruce de orden (OX) entre dos padres.

    Parámetros:
        padre1, padre2: listas de celdas

    Retorna:
        Tupla (hijo1, hijo2).
    """
    n = len(padre1)
    i, j = sorted(random.sample(range(n), 2))

    def ox(p1, p2):
        segmento = p1[i:j+1]
        resto = [x for x in p2 if x not in segmento]
        return resto[:i] + segmento + resto[i:]

    return ox(padre1, padre2), ox(padre2, padre1)


def _mutacion_swap(individuo: list) -> list:
    """
    Mutación por intercambio de dos posiciones aleatorias.

    Parámetros:
        individuo: lista de celdas

    Retorna:
        Individuo mutado (modificado in-place y retornado).
    """
    i, j = random.sample(range(len(individuo)), 2)
    individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo


def ejecutar_ga(metrica: str, layout: Layout, verbose: bool = True) -> tuple:
    """
    Ejecuta el Algoritmo Genético Tradicional.

    Parámetros:
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout
        verbose: si True, imprime progreso cada 50 generaciones

    Retorna:
        Tupla (mejor_asignacion: dict, mejor_costo: float)
    """
    params = GA_PARAMS
    tam_pob   = params["poblacion"]
    n_gen     = params["generaciones"]
    p_cruce   = params["prob_cruce"]
    p_mutac   = params["prob_mutacion"]
    k_torneo  = params["torneo_k"]
    celdas    = layout.celdas_disponibles

    poblacion = [_crear_individuo(celdas) for _ in range(tam_pob)]
    costos    = [_fitness(ind, metrica, layout) for ind in poblacion]

    idx_elite = min(range(tam_pob), key=lambda i: costos[i])
    mejor_ind = copy.deepcopy(poblacion[idx_elite])
    mejor_costo = costos[idx_elite]

    for gen in range(1, n_gen + 1):
        nueva_pob = [copy.deepcopy(mejor_ind)]  # elitismo

        while len(nueva_pob) < tam_pob:
            p1 = _seleccion_torneo(poblacion, costos, k_torneo)
            p2 = _seleccion_torneo(poblacion, costos, k_torneo)

            if random.random() < p_cruce:
                h1, h2 = _cruce_ox(p1, p2)
            else:
                h1, h2 = copy.deepcopy(p1), copy.deepcopy(p2)

            if random.random() < p_mutac:
                _mutacion_swap(h1)
            if random.random() < p_mutac:
                _mutacion_swap(h2)

            nueva_pob.extend([h1, h2])

        poblacion = nueva_pob[:tam_pob]
        costos    = [_fitness(ind, metrica, layout) for ind in poblacion]

        idx = min(range(tam_pob), key=lambda i: costos[i])
        if costos[idx] < mejor_costo:
            mejor_costo = costos[idx]
            mejor_ind   = copy.deepcopy(poblacion[idx])

        if verbose and gen % 50 == 0:
            print(f"  Generación {gen}/{n_gen} | Mejor costo: {mejor_costo:.2f}")

    return _decodificar(mejor_ind), mejor_costo
