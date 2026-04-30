# compacto.py — Algoritmo Genético Compacto (cGA) para optimización de layout.

import random
import copy
from distancias import calcular_costo_total
from layout import Layout
from config import MAQUINAS, SECUENCIA, CGA_PARAMS


def _muestrear(P: list, celdas: list) -> list:
    """
    Genera un individuo a partir del vector de probabilidades P.
    Asigna celdas sin repetición: para cada máquina elige la celda
    con mayor probabilidad dentro de las aún no asignadas.

    Parámetros:
        P:      lista de listas P[i][j] = prob de que maquina i esté en celda j
        celdas: lista de celdas disponibles (mismo orden que columnas de P)

    Retorna:
        Lista de celdas asignadas (una por máquina).
    """
    n_maq  = len(MAQUINAS)
    n_cel  = len(celdas)
    usadas = set()
    individuo = []

    for i in range(n_maq):
        probs = [(P[i][j], j) for j in range(n_cel) if j not in usadas]
        probs.sort(reverse=True)
        # sorteo ponderado entre las disponibles
        disponibles = [j for _, j in probs]
        pesos       = [p for p, _ in probs]
        total = sum(pesos)
        if total == 0:
            elegido = random.choice(disponibles)
        else:
            r, acum = random.random() * total, 0.0
            elegido = disponibles[-1]
            for p, j in zip(pesos, disponibles):
                acum += p
                if r <= acum:
                    elegido = j
                    break
        usadas.add(elegido)
        individuo.append(celdas[elegido])

    return individuo


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
    Evalúa el costo total de un individuo.

    Parámetros:
        individuo: lista de celdas
        metrica:   'manhattan' o 'euclidiana'
        layout:    instancia de Layout

    Retorna:
        Costo total de recorrido.
    """
    return calcular_costo_total(_decodificar(individuo), SECUENCIA, metrica, layout)


def _actualizar_P(P: list, ganador: list, perdedor: list, celdas: list, N: int):
    """
    Actualiza el vector de probabilidades según el resultado de la competencia.

    Parámetros:
        P:        vector de probabilidades (modificado in-place)
        ganador:  individuo ganador
        perdedor: individuo perdedor
        celdas:   lista de celdas disponibles
        N:        tamaño de población virtual
    """
    idx_cel = {c: j for j, c in enumerate(celdas)}
    for i, maq in enumerate(MAQUINAS):
        j_gan = idx_cel[ganador[i]]
        j_per = idx_cel[perdedor[i]]
        if j_gan != j_per:
            P[i][j_gan] = min(1.0, P[i][j_gan] + 1.0 / N)
            P[i][j_per] = max(0.0, P[i][j_per] - 1.0 / N)


def _convergido(P: list, eps: float = 0.02) -> bool:
    """
    Comprueba si el vector P ha convergido (todos los valores cerca de 0 o 1).

    Parámetros:
        P:   vector de probabilidades
        eps: umbral de convergencia

    Retorna:
        True si P está convergido.
    """
    return all(
        all(p < eps or p > 1 - eps for p in fila)
        for fila in P
    )


def ejecutar_cga(metrica: str, layout: Layout, verbose: bool = True) -> tuple:
    """
    Ejecuta el Algoritmo Genético Compacto (cGA).

    Parámetros:
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout
        verbose: si True, imprime progreso cada 100 iteraciones

    Retorna:
        Tupla (mejor_asignacion: dict, mejor_costo: float)
    """
    params  = CGA_PARAMS
    N       = params["N"]
    max_it  = params["iteraciones"]
    celdas  = layout.celdas_disponibles
    n_maq   = len(MAQUINAS)
    n_cel   = len(celdas)

    # P[i][j] = prob de que maquina i esté en celda j, inicializa uniforme
    P = [[1.0 / n_cel] * n_cel for _ in range(n_maq)]

    mejor_ind   = _muestrear(P, celdas)
    mejor_costo = _fitness(mejor_ind, metrica, layout)

    for it in range(1, max_it + 1):
        ind1 = _muestrear(P, celdas)
        ind2 = _muestrear(P, celdas)

        c1 = _fitness(ind1, metrica, layout)
        c2 = _fitness(ind2, metrica, layout)

        if c1 <= c2:
            ganador, perdedor, cg = ind1, ind2, c1
        else:
            ganador, perdedor, cg = ind2, ind1, c2

        if cg < mejor_costo:
            mejor_costo = cg
            mejor_ind   = copy.deepcopy(ganador)

        _actualizar_P(P, ganador, perdedor, celdas, N)

        if verbose and it % 100 == 0:
            conv = sum(1 for fila in P for p in fila if p < 0.02 or p > 0.98)
            total = n_maq * n_cel
            pct = 100 * conv // total
            print(f"  Iteracion {it}/{max_it} | Convergencia: {pct}% | Mejor: {mejor_costo:.2f}")

        if _convergido(P):
            if verbose:
                print(f"  Convergido en iteracion {it}")
            break

    return _decodificar(mejor_ind), mejor_costo
