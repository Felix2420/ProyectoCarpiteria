# aco.py — Ant Colony Optimization (ACO) para optimización de layout.

import random
import copy
from distancias import calcular_costo_total
from layout import Layout
from config import MAQUINAS, SECUENCIA, ACO_PARAMS


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
    Evalúa el costo total de una solución construida por una hormiga.

    Parámetros:
        individuo: lista de celdas (una por máquina)
        metrica:   'manhattan' o 'euclidiana'
        layout:    instancia de Layout

    Retorna:
        Costo total de recorrido.
    """
    return calcular_costo_total(_decodificar(individuo), SECUENCIA, metrica, layout)


def _construir_solucion(tau: list, celdas: list, alpha: float) -> list:
    """
    Una hormiga construye una solución completa eligiendo celdas
    probabilísticamente según la feromona τ[maquina][celda].

    Parámetros:
        tau:   matriz de feromonas [n_maquinas][n_celdas]
        celdas: lista de celdas disponibles
        alpha: exponente de feromona

    Retorna:
        Lista de celdas asignadas (una por máquina, en orden de MAQUINAS).
    """
    disponibles = list(range(len(celdas)))  # índices de celdas aún no usadas
    solucion = []

    for i in range(len(MAQUINAS)):
        pesos = [tau[i][j] ** alpha for j in disponibles]
        total = sum(pesos)

        # Selección por ruleta
        r = random.random() * total
        acum = 0.0
        elegido = disponibles[-1]
        for idx, j in enumerate(disponibles):
            acum += pesos[idx]
            if acum >= r:
                elegido = j
                break

        solucion.append(celdas[elegido])
        disponibles.remove(elegido)

    return solucion


def _depositar(tau: list, solucion: list, celdas: list, costo: float, Q: float):
    """
    Deposita feromona de una solución en la matriz tau (in-place).

    Parámetros:
        tau:     matriz de feromonas [n_maquinas][n_celdas]
        solucion: lista de celdas asignadas
        celdas:  lista de celdas disponibles (para obtener índice)
        costo:   costo total de la solución
        Q:       constante de depósito
    """
    deposito = Q / costo
    for i, celda in enumerate(solucion):
        j = celdas.index(celda)
        tau[i][j] += deposito


def ejecutar_aco(metrica: str, layout: Layout, verbose: bool = True) -> tuple:
    """
    Ejecuta Ant Colony Optimization para el problema de asignación de layout.

    Las hormigas construyen soluciones guiadas por feromonas. Se usa elitismo
    global: en cada iteración depositan feromona la mejor hormiga de la
    iteración y la mejor solución global encontrada hasta ese momento.

    Parámetros:
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout
        verbose: si True, imprime progreso cada 50 iteraciones

    Retorna:
        Tupla (mejor_asignacion: dict, mejor_costo: float)
    """
    params     = ACO_PARAMS
    n_hormigas = params["hormigas"]
    n_iter     = params["iteraciones"]
    alpha      = params["alpha"]
    rho        = params["rho"]
    Q          = params["Q"]
    tau0       = params["tau_inicial"]
    celdas     = layout.celdas_disponibles

    n_maq  = len(MAQUINAS)
    n_cel  = len(celdas)

    # Inicializar matriz de feromonas
    tau = [[tau0] * n_cel for _ in range(n_maq)]

    # Mejor global
    mejor_global = None
    costo_global = float("inf")

    for it in range(1, n_iter + 1):
        # Construir soluciones
        soluciones = [_construir_solucion(tau, celdas, alpha) for _ in range(n_hormigas)]
        costos     = [_fitness(s, metrica, layout) for s in soluciones]

        # Mejor de esta iteración
        idx_iter  = min(range(n_hormigas), key=lambda i: costos[i])
        mejor_iter = soluciones[idx_iter]
        costo_iter = costos[idx_iter]

        if costo_iter < costo_global:
            costo_global = costo_iter
            mejor_global = copy.copy(mejor_iter)

        # Evaporar feromonas
        for i in range(n_maq):
            for j in range(n_cel):
                tau[i][j] *= (1 - rho)
                tau[i][j]  = max(tau[i][j], 1e-6)  # evitar cero

        # Depositar: mejor de la iteración + elitismo global
        _depositar(tau, mejor_iter,  celdas, costo_iter,  Q)
        _depositar(tau, mejor_global, celdas, costo_global, Q)

        if verbose and it % 50 == 0:
            print(f"  Iteración {it}/{n_iter} | Mejor costo: {costo_global:.2f}")

    return _decodificar(mejor_global), costo_global
