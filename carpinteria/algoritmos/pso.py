# pso.py — Particle Swarm Optimization (PSO) para optimización de layout.
#
# Representación: permutación COMPLETA de todas las celdas disponibles.
# Las primeras n_maq posiciones determinan qué celda se asigna a cada máquina.
# Esto garantiza que gbest[i] siempre esté en la partícula, permitiendo swaps.

import random
import copy
from distancias import calcular_costo_total
from layout import Layout
from config import MAQUINAS, SECUENCIA, PSO_PARAMS


def _crear_particula(celdas: list) -> list:
    """
    Crea una partícula como permutación completa de todas las celdas disponibles.

    Parámetros:
        celdas: lista de celdas disponibles

    Retorna:
        Permutación completa de celdas; las primeras n_maq asignan las máquinas.
    """
    return random.sample(celdas, len(celdas))


def _decodificar(particula: list) -> dict:
    """
    Convierte los primeros n_maq elementos de la partícula en dict {id_maquina: celda}.

    Parámetros:
        particula: permutación completa de celdas

    Retorna:
        dict {id_maquina: (col, fila)}
    """
    return {MAQUINAS[i]: particula[i] for i in range(len(MAQUINAS))}


def _fitness(particula: list, metrica: str, layout: Layout) -> float:
    """
    Evalúa el costo total usando las primeras n_maq celdas de la partícula.

    Parámetros:
        particula: permutación completa de celdas
        metrica:   'manhattan' o 'euclidiana'
        layout:    instancia de Layout

    Retorna:
        Costo total de recorrido.
    """
    return calcular_costo_total(_decodificar(particula), SECUENCIA, metrica, layout)


def _acercar(origen: list, objetivo: list) -> list:
    """
    Aplica un swap en 'origen' para acercarlo a 'objetivo'.
    Busca la primera posición donde difieren y mueve el valor correcto a esa posición.
    Como ambas son permutaciones del mismo conjunto, el valor siempre existe en origen.

    Parámetros:
        origen:  permutación actual
        objetivo: permutación objetivo (pbest o gbest)

    Retorna:
        Nueva permutación con el swap aplicado.
    """
    nueva = copy.copy(origen)
    for i in range(len(nueva)):
        if nueva[i] != objetivo[i]:
            j = nueva.index(objetivo[i])
            nueva[i], nueva[j] = nueva[j], nueva[i]
            break
    return nueva


def ejecutar_pso(metrica: str, layout: Layout, verbose: bool = True) -> tuple:
    """
    Ejecuta Particle Swarm Optimization discreto para permutaciones.

    Cada partícula es una permutación completa de las celdas disponibles.
    El movimiento se implementa mediante swaps probabilísticos guiados por
    el mejor personal (pbest) y el mejor global (gbest).

    Parámetros:
        metrica: 'manhattan' o 'euclidiana'
        layout:  instancia de Layout
        verbose: si True, imprime progreso cada 50 iteraciones

    Retorna:
        Tupla (mejor_asignacion: dict, mejor_costo: float)
    """
    params   = PSO_PARAMS
    n_part   = params["particulas"]
    n_iter   = params["iteraciones"]
    w        = params["inercia"]
    c1       = params["coef_personal"]
    c2       = params["coef_social"]
    celdas   = layout.celdas_disponibles

    # Inicializar enjambre con permutaciones completas
    particulas = [_crear_particula(celdas) for _ in range(n_part)]
    costos     = [_fitness(p, metrica, layout) for p in particulas]

    pbest      = [copy.copy(p) for p in particulas]
    costos_pb  = list(costos)

    idx_g      = min(range(n_part), key=lambda i: costos[i])
    gbest      = copy.copy(particulas[idx_g])
    mejor_costo = costos[idx_g]

    for it in range(1, n_iter + 1):
        for i in range(n_part):
            pos = copy.copy(particulas[i])

            # Componente inercia: swap aleatorio para mantener diversidad
            if random.random() < w:
                a, b = random.sample(range(len(pos)), 2)
                pos[a], pos[b] = pos[b], pos[a]

            # Componente cognitivo: acercar a pbest con probabilidad c1*r1
            if random.random() < c1 * random.random() / 2:
                pos = _acercar(pos, pbest[i])

            # Componente social: acercar a gbest con probabilidad c2*r2
            if random.random() < c2 * random.random() / 2:
                pos = _acercar(pos, gbest)

            particulas[i] = pos
            costo = _fitness(pos, metrica, layout)

            if costo < costos_pb[i]:
                costos_pb[i] = costo
                pbest[i] = copy.copy(pos)

                if costo < mejor_costo:
                    mejor_costo = costo
                    gbest = copy.copy(pos)

        if verbose and it % 50 == 0:
            print(f"  Iteración {it}/{n_iter} | Mejor costo: {mejor_costo:.2f}")

    return _decodificar(gbest), mejor_costo
