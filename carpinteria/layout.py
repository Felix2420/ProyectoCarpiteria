# layout.py — Modela la grilla 4x4: celdas disponibles, posiciones fijas, validación.

from config import GRID_COLS, GRID_ROWS, ELEMENTOS_FIJOS, CELDAS_BLOQUEADAS, MAQUINAS


class Layout:
    """Representa la grilla de la carpintería y gestiona las asignaciones."""

    def __init__(self):
        self.fijos = ELEMENTOS_FIJOS.copy()
        self.todas_las_celdas = [
            (c, f)
            for c in range(1, GRID_COLS + 1)
            for f in range(1, GRID_ROWS + 1)
        ]
        self.celdas_disponibles = [
            celda for celda in self.todas_las_celdas
            if celda not in CELDAS_BLOQUEADAS
        ]

    def es_valida(self, asignacion: dict) -> bool:
        """
        Verifica que la asignación sea válida.

        Parámetros:
            asignacion: dict {id_maquina: (col, fila)}

        Retorna:
            True si no hay colisiones ni celdas inválidas.
        """
        celdas_usadas = list(asignacion.values())
        if len(celdas_usadas) != len(set(celdas_usadas)):
            return False
        for celda in celdas_usadas:
            if celda not in self.celdas_disponibles:
                return False
        return True

    def posicion(self, id_elemento: int, asignacion: dict) -> tuple:
        """
        Retorna la posición (col, fila) de un elemento.

        Parámetros:
            id_elemento: ID del elemento (fijo o máquina)
            asignacion:  dict con posiciones de las máquinas móviles

        Retorna:
            Tupla (col, fila).
        """
        if id_elemento in self.fijos:
            return self.fijos[id_elemento]
        return asignacion[id_elemento]
