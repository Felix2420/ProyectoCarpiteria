# estrategia_ev.py — Estrategia Evolutiva (μ + λ) para optimización de layout.

import random
import math
import copy
from distancias import calcular_costo_total
from layout import Layout
from config import MAQUINAS, SECUENCIA, ES_PARAMS


def _asignacion_aleatoria(celdas: list) -> list:
    """
    Crea una asignación aleatoria como lista de índices de celda (espacio real).

    Parámetros:
        celdas: lista de celdas disponibles

    Retorna:
        Lista de índices flotantes (posición en el espacio de celdas).
    """
    indices = random.sample(range(len(celdas)), len(MAQUINAS))
    return [float(i) for i in indices]


def _decodificar_real(vector: list, celdas: list) -> dict:
    """
    Convierte un vector real en una asignación discreta sin repetición.
    Ordena las máquinas por valor flotante y asigna celdas secuencialmente.

    Parámetros:
        vector: lista de flotantes (uno por máquina)
        celdas: lista de celdas disponibles

    Retorna:
        dict {id_maquina: (col, fila)}
    """
    n_cel = len(celdas)
    orden = sorted(range(len(MAQUINAS)), key=lambda i: vector[i])
    usadas = set()
    asignacion = {}

    for idx in orden:
        # celda preferida (módulo para mantenerse en rango)
        pref = int(round(vector[idx])) % n_cel
        if pref < 0:
            pref += n_cel
        # buscar la celda más cercana no usada
        for delta in range(n_cel):
            for signo in (0, 1, -1):
                candidato = (pref + signo * delta) % n_cel
                if candidato not in usadas:
                    usadas.add(candidato)
                    asignacion[MAQUINAS[idx]] = celdas[candidato]
                    break
            if MAQUINAS[idx] in asignacion:
                break

    return asignacion


def _fitness(vector: list, metrica: str, layout: Layout) -> float:
    """
    Evalúa el costo total de un individuo en representación real.

    Parámetros:
        vector:  lista de flotantes
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout

    Retorna:
        Costo total de recorrido.
    """
    asig = _decodificar_real(vector, layout.celdas_disponibles)
    return calcular_costo_total(asig, SECUENCIA, metrica, layout)


def _mutar(vector: list, sigma: float, n_cel: int) -> list:
    """
    Mutación gaussiana adaptativa del vector.

    Parámetros:
        vector: lista de flotantes
        sigma:  paso de mutación actual
        n_cel:  número de celdas disponibles (para acotar)

    Retorna:
        Vector mutado (nueva lista).
    """
    return [
        max(0.0, min(float(n_cel - 1), v + random.gauss(0, sigma)))
        for v in vector
    ]


def ejecutar_es(metrica: str, layout: Layout, verbose: bool = True) -> tuple:
    """
    Ejecuta la Estrategia Evolutiva (μ + λ).

    Parámetros:
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout
        verbose: si True, imprime progreso cada 50 generaciones

    Retorna:
        Tupla (mejor_asignacion: dict, mejor_costo: float)
    """
    params   = ES_PARAMS
    mu       = params["mu"]
    lambda_  = params["lambda_"]
    sigma    = params["sigma_inicial"]
    n_gen    = params["generaciones"]
    celdas   = layout.celdas_disponibles
    n_cel    = len(celdas)

    # Crear μ padres iniciales
    padres  = [_asignacion_aleatoria(celdas) for _ in range(mu)]
    costos  = [_fitness(p, metrica, layout) for p in padres]

    idx_mejor   = min(range(mu), key=lambda i: costos[i])
    mejor_vec   = copy.deepcopy(padres[idx_mejor])
    mejor_costo = costos[idx_mejor]

    exitos_ventana = 0
    VENTANA = 10 * lambda_

    for gen in range(1, n_gen + 1):
        # Generar λ hijos
        hijos  = []
        c_hijos = []
        for _ in range(lambda_):
            padre = random.choice(padres)
            hijo  = _mutar(padre, sigma, n_cel)
            c     = _fitness(hijo, metrica, layout)
            hijos.append(hijo)
            c_hijos.append(c)

        # Contar mejoras para regla 1/5
        exitos_ventana += sum(1 for c in c_hijos if c < mejor_costo)

        # Selección (μ + λ): mejores μ entre padres e hijos
        pool    = padres + hijos
        c_pool  = costos + c_hijos
        ranking = sorted(range(len(pool)), key=lambda i: c_pool[i])
        padres  = [copy.deepcopy(pool[i]) for i in ranking[:mu]]
        costos  = [c_pool[i] for i in ranking[:mu]]

        if costos[0] < mejor_costo:
            mejor_costo = costos[0]
            mejor_vec   = copy.deepcopy(padres[0])

        # Regla del 1/5 para adaptar sigma (cada VENTANA evaluaciones)
        if gen % VENTANA == 0:
            tasa = exitos_ventana / VENTANA
            if tasa > 0.2:
                sigma /= 0.85
            elif tasa < 0.2:
                sigma *= 0.85
            sigma = max(0.01, min(sigma, float(n_cel)))
            exitos_ventana = 0

        if verbose and gen % 50 == 0:
            print(f"  Generacion {gen}/{n_gen} | sigma={sigma:.3f} | Mejor costo: {mejor_costo:.2f}")

    mejor_asig = _decodificar_real(mejor_vec, celdas)
    return mejor_asig, mejor_costo
