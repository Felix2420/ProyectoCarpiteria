# animacion_3d.py — Animación 3D interactiva con Plotly para el recorrido del personal.

import plotly.graph_objects as go
from distancias import manhattan, euclidiana
from layout import Layout
from config import NOMBRES, SECUENCIA, ELEMENTOS_FIJOS


def _distancia_paso(p1, p2, metrica):
    fn = manhattan if metrica == "manhattan" else euclidiana
    return fn(p1, p2)


def generar_animacion(asignacion: dict, metrica: str, layout: Layout,
                      nombre_archivo: str, titulo: str = ""):
    """
    Genera un archivo HTML con la animación 3D interactiva del recorrido.

    Parámetros:
        asignacion:     dict {id_maquina: (col, fila)}
        metrica:        'manhattan' o 'euclidiana'
        layout:         instancia de Layout
        nombre_archivo: ruta completa del archivo HTML de salida
        titulo:         título del gráfico
    """
    # ── Construir posición completa (fijos + ubicados) ──────────────────────
    posiciones = {**ELEMENTOS_FIJOS, **asignacion}

    # ── Precalcular recorrido ────────────────────────────────────────────────
    pasos = []
    dist_acum = 0.0
    for i in range(len(SECUENCIA) - 1):
        id_o = SECUENCIA[i]
        id_d = SECUENCIA[i + 1]
        p1   = posiciones[id_o]
        p2   = posiciones[id_d]
        dist = _distancia_paso(p1, p2, metrica)
        dist_acum += dist
        pasos.append({
            "origen": id_o, "destino": id_d,
            "x1": p1[0], "y1": p1[1],
            "x2": p2[0], "y2": p2[1],
            "dist": dist, "acum": dist_acum,
        })

    # ── Capa base: nodos de la grilla ────────────────────────────────────────
    ids_fijos    = list(ELEMENTOS_FIJOS.keys())
    ids_moviles  = list(asignacion.keys())

    x_fijos  = [ELEMENTOS_FIJOS[i][0] for i in ids_fijos]
    y_fijos  = [ELEMENTOS_FIJOS[i][1] for i in ids_fijos]
    txt_fijos = [f"({i}) {NOMBRES[i]}" for i in ids_fijos]

    x_mov  = [asignacion[i][0] for i in ids_moviles]
    y_mov  = [asignacion[i][1] for i in ids_moviles]
    txt_mov = [f"({i}) {NOMBRES[i]}" for i in ids_moviles]

    trace_fijos = go.Scatter3d(
        x=x_fijos, y=y_fijos, z=[0]*len(ids_fijos),
        mode="markers+text",
        marker=dict(size=12, color="crimson", symbol="square"),
        text=txt_fijos, textposition="top center",
        name="Elementos fijos",
    )
    trace_moviles = go.Scatter3d(
        x=x_mov, y=y_mov, z=[0]*len(ids_moviles),
        mode="markers+text",
        marker=dict(size=12, color="steelblue", symbol="circle"),
        text=txt_mov, textposition="top center",
        name="Máquinas ubicadas",
    )

    # ── Frames de animación ──────────────────────────────────────────────────
    frames = []
    acumulado_x, acumulado_y, acumulado_z = [], [], []

    for k, paso in enumerate(pasos):
        acumulado_x += [paso["x1"], paso["x2"], None]
        acumulado_y += [paso["y1"], paso["y2"], None]
        acumulado_z += [paso["acum"] - paso["dist"], paso["acum"], None]

        trace_recorrido = go.Scatter3d(
            x=acumulado_x[:], y=acumulado_y[:], z=acumulado_z[:],
            mode="lines",
            line=dict(color="darkorange", width=4),
            name="Recorrido",
        )
        trace_punta = go.Scatter3d(
            x=[paso["x2"]], y=[paso["y2"]], z=[paso["acum"]],
            mode="markers",
            marker=dict(size=8, color="gold", symbol="diamond"),
            name=f"Paso {k+1}",
            showlegend=False,
        )

        anotacion = (
            f"Paso {k+1}: {NOMBRES[paso['origen']]} → {NOMBRES[paso['destino']]}<br>"
            f"Distancia: {paso['dist']:.2f} | Acumulado: {paso['acum']:.2f}"
        )

        frames.append(go.Frame(
            data=[trace_fijos, trace_moviles, trace_recorrido, trace_punta],
            name=str(k),
            layout=go.Layout(title_text=f"{titulo}<br>{anotacion}"),
        ))

    # ── Figura inicial (frame 0) ─────────────────────────────────────────────
    fig = go.Figure(
        data=[trace_fijos, trace_moviles,
              go.Scatter3d(x=[], y=[], z=[], mode="lines",
                           line=dict(color="darkorange", width=4), name="Recorrido"),
              go.Scatter3d(x=[], y=[], z=[], mode="markers",
                           marker=dict(size=8, color="gold"), showlegend=False)],
        frames=frames,
    )

    # ── Controles de animación ───────────────────────────────────────────────
    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis=dict(title="Columna", range=[0.5, 4.5], dtick=1),
            yaxis=dict(title="Fila",    range=[0.5, 4.5], dtick=1),
            zaxis=dict(title="Dist. acumulada"),
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=0,
            x=0.5,
            xanchor="center",
            buttons=[
                dict(label="▶ Play",
                     method="animate",
                     args=[None, {"frame": {"duration": 800, "redraw": True},
                                  "fromcurrent": True}]),
                dict(label="⏸ Pausa",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
            ],
        )],
        sliders=[dict(
            steps=[dict(method="animate",
                        args=[[str(k)], {"frame": {"duration": 0, "redraw": True},
                                         "mode": "immediate"}],
                        label=f"Paso {k+1}") for k in range(len(pasos))],
            active=0,
            x=0.1, len=0.8,
            currentvalue=dict(prefix="Paso: ", visible=True),
        )],
        legend=dict(x=0.01, y=0.99),
        height=650,
    )

    fig.write_html(nombre_archivo)
    print(f"  [OK] Guardado: {nombre_archivo}")
