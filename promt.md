Eres un experto en Python, algoritmos de optimización e inteligencia artificial.
Necesito que generes un proyecto completo y bien estructurado en Python que resuelva
el siguiente problema de distribución de planta (layout) para una carpintería.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏭 CONTEXTO DEL PROBLEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Una carpintería tiene un espacio de trabajo en una grilla de 4x4 unidades.
Hay elementos FIJOS (no se pueden mover) y máquinas que deben ser UBICADAS
en los espacios libres para minimizar el recorrido del personal.

ELEMENTOS FIJOS (con su posición en la grilla columna, fila):
  - (8)  Mat. Prima  → celda (1, 4)  [esquina superior izquierda]
  - (9)  Triplay     → celda (1, 3)
  - (10) Almacén     → celda (4, 3)
  - (11) Baño        → celda (1, 1)

CELDAS DISPONIBLES (espacios 2x2 libres en la grilla):
  Las 12 celdas libres restantes en la grilla 4x4, excluyendo las fijas.
  Cada máquina ocupa exactamente 1 celda de las disponibles.
  No puede haber dos máquinas en la misma celda.

MÁQUINAS A UBICAR (7 en total):
  (1) E. Trabajo
  (2) Destrozadora
  (3) Sierra Cinta
  (4) Canteadora
  (5) Cepillo
  (6) Trompo
  (7) Esclopeadora

SECUENCIA DE RECORRIDO DEL PERSONAL (en orden):
  1→8, 8→1, 1→4, 4→5, 5→3, 3→4, 4→3, 3→1, 1→9, 9→1, 1→3, 3→1, 1→10

  Nota: Los números corresponden al ID de la máquina o elemento fijo.
  El costo total es la suma de todas las distancias entre pares consecutivos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ ALGORITMOS A IMPLEMENTAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa los siguientes algoritmos de optimización. Cada uno debe devolver
la mejor asignación encontrada (diccionario máquina → celda) y el costo total.

1. ALGORITMO GENÉTICO TRADICIONAL (GA)
   - Representación: permutación de las 7 máquinas en las celdas disponibles
   - Selección por torneo
   - Cruce de orden (OX - Order Crossover)
   - Mutación por intercambio de posiciones (swap mutation)
   - Elitismo: conservar el mejor individuo por generación
   - Parámetros configurables: población, generaciones, prob_cruce, prob_mutacion

2. ALGORITMO GENÉTICO COMPACTO (cGA - Compact Genetic Algorithm)
   - En lugar de mantener una población explícita, mantiene un vector de
     probabilidades P[i][j] = probabilidad de que la máquina i esté en celda j
   - En cada iteración genera 2 individuos, compite entre ellos y actualiza P
   - Tamaño de población virtual N configurable
   - Criterio de convergencia cuando P converge a 0 o 1

3. ESTRATEGIA EVOLUTIVA (ES) — variante (μ + λ)
   - Representación real: vector de posiciones con ruido gaussiano
   - μ padres generan λ hijos mediante mutación gaussiana adaptativa
   - Selección (μ + λ): los mejores μ individuos entre padres e hijos sobreviven
   - Auto-adaptación del paso de mutación σ (regla del 1/5)
   - Parámetros configurables: mu, lambda_, sigma_inicial, generaciones

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📐 MÉTRICAS DE DISTANCIA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Implementa ambas métricas y permite seleccionar cuál usar al ejecutar:

- Manhattan:   d = |x1 - x2| + |y1 - y2|
- Euclidiana:  d = sqrt((x1-x2)² + (y1-y2)²)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 ANIMACIÓN 3D INTERACTIVA (Plotly)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Genera una animación 3D con Plotly que muestre visualmente el recorrido
del personal sobre el layout de la carpintería para la mejor solución
encontrada por cada algoritmo:

- Eje X, Y: posición en la grilla 4x4
- Eje Z: distancia acumulada en cada paso del recorrido
- Cada paso del recorrido es un frame de la animación
- Incluir botón "▶ Play" y slider de pasos
- Mostrar el nombre de cada máquina/elemento en su celda como anotación
- Usar colores distintos para máquinas fijas vs. ubicadas
- Incluir dropdown para cambiar entre algoritmos (GA, cGA, ES)
- Incluir dropdown para cambiar entre distancia Manhattan y Euclidiana
- Guardar el resultado como archivo HTML interactivo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🗂️ ESTRUCTURA DEL PROYECTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Organiza el código en los siguientes archivos/módulos:

carpinteria/
│
├── main.py                  ← Punto de entrada, ejecuta todo y muestra resultados
│
├── config.py                ← Constantes: grilla, elementos fijos, secuencia de
│                               recorrido, parámetros de cada algoritmo
│
├── layout.py                ← Clase Layout: modela la grilla, celdas disponibles,
│                               posiciones fijas, validación de asignaciones
│
├── distancias.py            ← Funciones manhattan() y euclidiana(), y
│                               calcular_costo_total(asignacion, secuencia, metrica)
│
├── algoritmos/
│   ├── __init__.py
│   ├── genetico.py          ← Algoritmo Genético Tradicional (GA)
│   ├── compacto.py          ← Algoritmo Genético Compacto (cGA)
│   └── estrategia_ev.py     ← Estrategia Evolutiva (μ + λ)
│
└── visualizacion/
    ├── __init__.py
    └── animacion_3d.py      ← Animación 3D interactiva con Plotly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 REQUERIMIENTOS DE CÓDIGO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Python 3.10+
- Librerías: numpy, plotly, random, math, copy (todas estándar o pip install)
- Cada función debe tener docstring explicando: qué hace, parámetros y retorno
- Cada archivo debe tener un comentario de cabecera explicando su propósito
- Los parámetros de los algoritmos deben estar centralizados en config.py
- El código debe ser ejecutable con: python main.py
- Al final de main.py imprimir una tabla comparativa con:
    | Algoritmo | Métrica    | Mejor Costo | Asignación óptima |
    |-----------|------------|-------------|-------------------|
    | GA        | Manhattan  | X.XX        | {1:celda, ...}    |
    | GA        | Euclidiana | X.XX        | ...               |
    | cGA       | Manhattan  | X.XX        | ...               |
    | cGA       | Euclidiana | X.XX        | ...               |
    | ES(μ+λ)   | Manhattan  | X.XX        | ...               |
    | ES(μ+λ)   | Euclidiana | X.XX        | ...               |
- Generar un archivo HTML por cada combinación algoritmo+métrica con la
  animación 3D, nombrado como: resultado_GA_manhattan.html, etc.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 EJEMPLO ESPERADO DE SALIDA EN CONSOLA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

=== CARPINTERÍA - OPTIMIZACIÓN DE LAYOUT ===

[GA - Manhattan]
  Generación 50/100 | Mejor costo: 12.00
  Generación 100/100 | Mejor costo: 9.00
  ✅ Mejor asignación: {1: (2,2), 2: (3,1), 3: (2,3), ...}
  📏 Costo total: 9.00

[cGA - Euclidiana]
  Iteración 200/500 | Convergencia: 45%
  ✅ Mejor asignación: {1: (2,1), ...}
  📏 Costo total: 7.41

... (similar para cada combinación)

🎬 Animaciones guardadas en: ./resultados/