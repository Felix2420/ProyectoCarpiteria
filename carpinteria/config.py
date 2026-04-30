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
    "poblacion":     100,
    "generaciones":  200,
    "prob_cruce":    0.85,
    "prob_mutacion": 0.15,
    "torneo_k":      3,
}

# ──────────────────────────────────────────────
# Parámetros del Algoritmo Genético Compacto
# ──────────────────────────────────────────────
CGA_PARAMS = {
    "N":           200,   # tamaño de población virtual
    "iteraciones": 1000,
}

# ──────────────────────────────────────────────
# Parámetros de la Estrategia Evolutiva (μ + λ)
# ──────────────────────────────────────────────
ES_PARAMS = {
    "mu":            10,
    "lambda_":       50,
    "sigma_inicial": 1.0,
    "generaciones":  300,
}
