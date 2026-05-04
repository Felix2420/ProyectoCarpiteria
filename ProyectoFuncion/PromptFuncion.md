Perfecto, entonces vamos a extender el prompt anterior usando tu función específica y añadiendo que el problema se resuelva con varios algoritmos evolutivos y de enjambre (tradicionales, compactos, estrategias evolutivas, colmena y hormigas).

La función a optimizar será la que muestras en la imagen y en tu HTML:

z
=
sin
⁡
(
x
2
+
y
2
)
⋅
cos
⁡
(
x
⋅
y
)
+
x
2
+
y
2
10
z=sin(x 
2
 +y 
2
 )⋅cos(x⋅y)+ 
10
x 
2
 +y 
2
 
​
 

Aquí tienes el nuevo prompt completo para Claude; solo pégalo y ajusta si quieres cambiar algo de texto:

Prompt actualizado para Claude
Genera una sola página web completa que incluya todo el código necesario en HTML + CSS + JavaScript (en un solo archivo) para lo siguiente. Todo debe estar en español y el código debe estar muy bien documentado con comentarios claros.

Función y objetivo de optimización

Usa exactamente la siguiente función de dos variables para todo el análisis y la optimización:

f
(
x
,
y
)
=
sin
⁡
(
x
2
+
y
2
)
⋅
cos
⁡
(
x
⋅
y
)
+
x
2
+
y
2
10
f(x,y)=sin(x 
2
 +y 
2
 )⋅cos(x⋅y)+ 
10
x 
2
 +y 
2
 
​
 
Explica al usuario que es una función multimodal, con múltiples máximos y mínimos locales en el plano 
x
x-
y
y, ideal para probar algoritmos de optimización global.

El objetivo principal es encontrar un máximo (o mínimo) global o casi global de esta función en un dominio acotado, por ejemplo 
x
,
y
∈
[
−
5
,
5
]
x,y∈[−5,5], usando diferentes familias de algoritmos evolutivos y de enjambre.

Sección teórica (cálculo multivariable básico)
Incluye una sección donde expliques brevemente, de forma didáctica:

Qué es un máximo local, mínimo local y punto de silla en funciones de dos variables, con explicación geométrica (pico, valle, silla de montar).

De manera esquemática, cómo se usarían derivadas parciales y la prueba de la segunda derivada para clasificar puntos críticos, sin necesidad de hacer todo el cálculo analítico completo (puedes mostrar la idea general porque esta función es compleja).

Visualización 3D interactiva de la función

Usa Plotly.js u otra librería apta para generar una superficie 3D de 
f
(
x
,
y
)
f(x,y).

Características mínimas:

Ejes etiquetados 
x
x, 
y
y, 
z
=
f
(
x
,
y
)
z=f(x,y).

Interacción: rotación, zoom con el ratón.

Controles (sliders o inputs) para ajustar el rango de 
x
x e 
y
y dentro de un intervalo razonable, por ejemplo de 
[
−
5
,
5
]
[−5,5] a otros valores, actualizando la superficie en tiempo real.

Animación / actualización de la superficie

Implementa la lógica JS para recalcular la malla de puntos y re-renderizar la superficie al cambiar el rango.

Documenta con comentarios cada parte importante: creación de la malla, evaluación de 
f
(
x
,
y
)
f(x,y), construcción del objeto de datos de Plotly y actualización de la gráfica.

Algoritmos de optimización a implementar
Implementa, todos en JavaScript puro, al menos las siguientes familias de algoritmos, bien separados en funciones y muy comentados, todos trabajando sobre la misma función 
f
(
x
,
y
)
f(x,y) y el mismo dominio: a) Algoritmos evolutivos tradicionales (Genetic Algorithm clásico)

Representación de individuos como vectores 
[
x
,
y
]
[x,y].

Población inicial aleatoria en el dominio.

Evaluación de fitness usando 
f
(
x
,
y
)
f(x,y) (explica si buscas máximo o mínimo).

Selección (por ejemplo, torneo o ruleta).

Cruza (por ejemplo, blend o aritmética) y mutación (perturbación gaussiana o uniforme).

Elitismo opcional.

Bucle generacional hasta un número fijo de iteraciones.

b) Algoritmos evolutivos compactos (cGA o similar)

Implementa una versión compacta donde no se mantiene una población explícita, sino una distribución de probabilidad sobre el espacio de soluciones o sobre parámetros (por ejemplo, modelo simple tipo cGA adaptado a dos variables reales).

Muestra cómo se actualiza la distribución a partir de comparaciones entre soluciones muestreadas.

Documenta claramente la diferencia conceptual con el GA tradicional.

c) Estrategias evolutivas (Evolution Strategies, ES)

Implementa una estrategia del tipo 
(
μ
,
λ
)
(μ,λ) o 
(
μ
+
λ
)
(μ+λ), con:

Individuos que incluyen posición y parámetros de mutación (por ejemplo, desviaciones estándar para 
x
x y 
y
y).

Mutación gaussiana controlada por esos parámetros.

Selección de descendientes según fitness.

Explica en comentarios la idea de adaptación de la variancia en ES.

d) Algoritmo de colmena / enjambre (por ejemplo, Bee Colony Optimization básico o Particle Swarm simplificado estilo “colmena”)

Implementa una versión simplificada de un algoritmo de colmena:

Población de abejas/exploradores que se mueven en el espacio 
(
x
,
y
)
(x,y).

Exploración global y explotación local alrededor de las mejores posiciones encontradas.

Documenta en español la lógica de exploración-explotación de la colmena.

e) Algoritmo de hormigas (Ant Colony Optimization adaptado a continuo)

Implementa una versión simplificada de un algoritmo de hormigas adaptado a un espacio continuo 2D:

Trail de feromonas sobre una cuadrícula discreta en el dominio 
(
x
,
y
)
(x,y) o sobre un conjunto de puntos de referencia.

Hormigas que generan soluciones moviéndose guiadas por probabilidad dependiente de feromonas y calidad de las soluciones.

Actualización de feromonas (refuerzo en zonas buenas, evaporación global).

Explica con comentarios cómo se traduce la lógica clásica de ACO a este problema continuo.

Comparación de resultados entre algoritmos

Para cada algoritmo, muestra en la interfaz:

Mejor valor de 
f
(
x
,
y
)
f(x,y) encontrado.

Coordenadas aproximadas 
(
x
∗
,
y
∗
)
(x 
∗
 ,y 
∗
 ).

Número de evaluaciones de la función.

Dibuja en la gráfica 3D un marcador para la mejor solución encontrada por cada algoritmo, con un color o símbolo distinto, y agrega una pequeña leyenda (“GA”, “cGA”, “ES”, “Colmena”, “Hormigas”).

Controles de la interfaz para ejecutar los algoritmos

Agrega botones tipo:

“Ejecutar GA clásico”

“Ejecutar Algoritmo Evolutivo Compacto”

“Ejecutar Estrategias Evolutivas (ES)”

“Ejecutar Algoritmo de Colmena”

“Ejecutar Algoritmo de Hormigas”

Cada botón debe:

Lanzar la ejecución del algoritmo correspondiente.

Actualizar en pantalla los resultados numéricos (mejor 
f
f, coordenadas, evaluaciones).

Actualizar la gráfica 3D con el marcador de la mejor solución.

Estructura visual y documentación del código

Organiza la página con secciones claras:

Introducción y descripción de la función multimodal.

Visualización 3D.

Panel de control de algoritmos (botones y parámetros básicos, por ejemplo número de iteraciones, tamaño de población, etc.).

Resultados comparativos.

Usa CSS para:

Centrar el contenido.

Crear un layout claro (por ejemplo, gráfica a la izquierda, panel de control a la derecha en pantallas grandes).

Dar buen contraste y tipografía legible.

Comenta el código JS con comentarios en español, explicando:

Definición de la función objetivo.

Implementación de cada algoritmo (paso a paso).

Cómo se integran los resultados con la gráfica Plotly.

Conclusión para el usuario

Al final de la página, incluye un breve texto que:

Resuma qué algoritmos se implementaron.

Destaque cuál suele encontrar mejores soluciones en este paisaje multimodal y por qué (desde una perspectiva cualitativa, no hace falta un análisis estadístico profundo).

Haga énfasis en cómo la visualización 3D ayuda a entender la dificultad de optimizar funciones con muchos máximos y mínimos locales.

Asegúrate de que todo el contenido esté en español, el código sea claro y bien comentado, y que todos los algoritmos realmente operen sobre la función definida 
f
(
x
,
y
)
f(x,y), mostrando sus mejores soluciones sobre la superficie 3D.