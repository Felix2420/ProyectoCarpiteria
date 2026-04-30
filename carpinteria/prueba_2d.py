# prueba_2d.py — Prueba de animación 2D con GA solamente.

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout import Layout
from algoritmos.genetico import ejecutar_ga
from visualizacion.animacion_2d import generar_animacion_2d

RESULTADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultados")
os.makedirs(RESULTADOS, exist_ok=True)


def main():
    layout = Layout()

    print("=" * 60)
    print("  PRUEBA: GA + ANIMACION 2D INTERACTIVA")
    print("=" * 60)
    print()

    # Ejecutar GA con ambas métricas
    for metrica in ["manhattan", "euclidiana"]:
        print(f"\n[GA - {metrica.capitalize()}]")
        asig, costo = ejecutar_ga(metrica, layout, verbose=True)

        print(f"  >> Mejor costo: {costo:.2f}")
        print(f"  >> Mejor asignacion: {asig}")

        # Generar animación 2D
        html_path = os.path.join(RESULTADOS, f"animacion_2d_GA_{metrica}.html")
        titulo = f"GA - {metrica.capitalize()} | Costo: {costo:.2f}"
        generar_animacion_2d(asig, metrica, layout, html_path, titulo)

    print("\n" + "=" * 60)
    print(f"  Listo! Abre los archivos HTML en tu navegador.")
    print(f"  Ubicacion: {RESULTADOS}")
    print("=" * 60)


if __name__ == "__main__":
    main()
