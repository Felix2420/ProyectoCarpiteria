# distancias.py — Funciones de distancia y cálculo del costo total de recorrido.

import math
from layout import Layout
from config import SECUENCIA


def manhattan(p1: tuple, p2: tuple) -> float:
    """
    Distancia Manhattan entre dos celdas.

    Parámetros:
        p1, p2: tuplas (col, fila)

    Retorna:
        Distancia entera.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidiana(p1: tuple, p2: tuple) -> float:
    """
    Distancia Euclidiana entre dos celdas.

    Parámetros:
        p1, p2: tuplas (col, fila)

    Retorna:
        Distancia flotante.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def calcular_costo_total(asignacion: dict, secuencia: list, metrica: str, layout: Layout) -> float:
    """
    Calcula el costo total de la secuencia de recorrido.

    Parámetros:
        asignacion: dict {id_maquina: (col, fila)}
        secuencia:  lista de IDs en orden de visita
        metrica:    'manhattan' o 'euclidiana'
        layout:     instancia de Layout para resolver posiciones

    Retorna:
        Costo total (suma de distancias entre pares consecutivos).
    """
    fn = manhattan if metrica == "manhattan" else euclidiana
    costo = 0.0
    for i in range(len(secuencia) - 1):
        p1 = layout.posicion(secuencia[i], asignacion)
        p2 = layout.posicion(secuencia[i + 1], asignacion)
        costo += fn(p1, p2)
    return costo
