# main.py — Punto de entrada: ejecuta los 3 algoritmos con ambas métricas.

import sys
import os

# Permite importar módulos hermanos desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout import Layout
from algoritmos.genetico      import ejecutar_ga
from algoritmos.compacto      import ejecutar_cga
from algoritmos.estrategia_ev import ejecutar_es
from algoritmos.pso           import ejecutar_pso
from algoritmos.aco           import ejecutar_aco
from visualizacion.animacion_2d import generar_animacion_2d
from config import NOMBRES

METRICAS    = ["manhattan", "euclidiana"]
RESULTADOS  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")
os.makedirs(RESULTADOS, exist_ok=True)


def _nombre_asig(asig: dict) -> str:
    return "{" + ", ".join(f"{k}:{v}" for k, v in sorted(asig.items())) + "}"


def main():
    layout = Layout()

    print("=" * 50)
    print("  CARPINTERIA - OPTIMIZACION DE LAYOUT")
    print("=" * 50)
    print(f"  Celdas disponibles ({len(layout.celdas_disponibles)}): {layout.celdas_disponibles}\n")

    algoritmos = [
        ("GA",     ejecutar_ga),
        ("cGA",    ejecutar_cga),
        ("ES",     ejecutar_es),
        ("PSO",    ejecutar_pso),
        ("ACO",    ejecutar_aco),
    ]

    tabla = []

    for nombre_alg, fn in algoritmos:
        for metrica in METRICAS:
            etiqueta = f"[{nombre_alg} - {metrica.capitalize()}]"
            print(f"\n{etiqueta}")

            asig, costo = fn(metrica, layout, verbose=True)

            print(f"  >> Mejor asignacion: {_nombre_asig(asig)}")
            print(f"  >> Costo total: {costo:.2f}")

            # Generar animación 2D
            slug = nombre_alg.lower()
            html_path = os.path.join(RESULTADOS, f"resultado_{slug}_{metrica}.html")
            titulo = f"{nombre_alg} | {metrica.capitalize()} | Costo: {costo:.2f}"
            generar_animacion_2d(asig, metrica, layout, html_path, titulo)

            tabla.append((nombre_alg, metrica.capitalize(), costo, asig))

    # ── Tabla comparativa ────────────────────────────────────────────────────
    print("\n")
    print("=" * 100)
    print(f"{'Algoritmo':<12} {'Metrica':<12} {'Mejor Costo':>12}  Asignacion optima")
    print("-" * 100)
    for alg, met, cost, asig in tabla:
        print(f"{alg:<12} {met:<12} {cost:>12.2f}  {_nombre_asig(asig)}")
    print("=" * 100)

    print(f"\n[OK] Animaciones guardadas en: {RESULTADOS}")


if __name__ == "__main__":
    main()
