# config.py — Centraliza todas las constantes y parámetros del proyecto.

# Grilla 4x4: columnas 1-4 (x), filas 1-4 (y)
GRID_COLS = 4
GRID_ROWS = 4

# Elementos fijos: {id: (col, fila)} — posición de referencia para distancias
ELEMENTOS_FIJOS = {
    8:  (1, 4),  # Mat. Prima  — 1 celda
    9:  (1, 3),  # Triplay     — 1 celda
    10: (4, 3),  # Almacén     — ocupa (4,3) y (4,4)
    11: (1, 1),  # Baño        — ocupa (1,1) y (1,2)
}

# Todas las celdas físicamente bloqueadas por elementos fijos (no disponibles)
CELDAS_BLOQUEADAS = {
    (1, 4),  # Mat. Prima
    (1, 3),  # Triplay
    (4, 3),  # Almacén — celda principal
    (4, 4),  # Almacén — segunda celda
    (1, 1),  # Baño    — celda principal
    (1, 2),  # Baño    — segunda celda
}

# Nombres de todos los elementos
NOMBRES = {
    1: "E. Trabajo",
    2: "Destrozadora",
    3: "Sierra Cinta",
    4: "Canteadora",
    5: "Cepillo",
    6: "Trompo",
    7: "Esclopeadora",
    8: "Mat. Prima",
    9: "Triplay",
    10: "Almacén",
    11: "Baño",
}

# Máquinas a ubicar (IDs)
MAQUINAS = [1, 2, 3, 4, 5, 6, 7]

# Secuencia de recorrido del personal (pares consecutivos)
SECUENCIA = [1, 8, 1, 4, 5, 3, 4, 3, 1, 9, 1, 3, 1, 10]

# ──────────────────────────────────────────────
# Parámetros del Algoritmo Genético Tradicional
# ──────────────────────────────────────────────
GA_PARAMS = {
    "poblacion":     100,  #Numero de individuos en cada generación
    "generaciones":  200,  #Número de generaciones a ejecutar
    "prob_cruce":    0.85, #Probabilidad de cruzar dos individuos para crear descendencia
    "prob_mutacion": 0.15, #Probabilidad de mutar un individuo (cambiar su configuración)
    "torneo_k":      3,    #Número de individuos seleccionados en cada torneo para elegir al mejor (selección por torneo) 
}

# ──────────────────────────────────────────────
# Parámetros del Algoritmo Genético Compacto
# ──────────────────────────────────────────────
CGA_PARAMS = {
    "N":           200,   # tamaño de población virtual
    "iteraciones": 1000, # número de iteraciones a ejecutar
}

# ──────────────────────────────────────────────
# Parámetros de la Estrategia Evolutiva (μ + λ)
# ──────────────────────────────────────────────
ES_PARAMS = {
    "mu":            10,  # número de padres seleccionados para reproducirse en cada generación
    "lambda_":       50,  # número de descendientes generados por los padres en cada generación
    "sigma_inicial": 1.0, # desviación estándar inicial para la mutación gaussiana (controla la magnitud de los cambios en los descendientes)
    "generaciones":  300, # número de generaciones a ejecutar
}

# ──────────────────────────────────────────────
# Parámetros de PSO (Particle Swarm Optimization)
# ──────────────────────────────────────────────
PSO_PARAMS = {
    "particulas":     30, # número de partículas en el swarm
    "iteraciones":   300, # número de iteraciones a ejecutar
    "inercia":       0.7, # factor de inercia
    "coef_personal": 1.5, # coeficiente personal
    "coef_social":   1.5, # coeficiente social
}

# ──────────────────────────────────────────────
# Parámetros de ACO (Ant Colony Optimization)
# ──────────────────────────────────────────────
ACO_PARAMS = {
    "hormigas":    20,     # número de hormigas en cada iteración
    "iteraciones": 300,    # número de iteraciones a ejecutar 
    "alpha":       2.0,   # peso de feromona
    "beta":        1.0,   # peso de heurística (uniforme)
    "rho":         0.1,   # tasa de evaporación
    "Q":          10.0,   # constante de depósito
    "tau_inicial": 1.0,   # feromona inicial uniforme
}
