# animacion_2d.py — Animacion 2D vista superior con elementos fijos de tamaño real.

import plotly.graph_objects as go
from distancias import manhattan, euclidiana
from layout import Layout
from config import NOMBRES, SECUENCIA, ELEMENTOS_FIJOS, CELDAS_BLOQUEADAS, GRID_COLS, GRID_ROWS

# Celdas que ocupa cada elemento fijo (para dibujar tamaño real)
CELDAS_POR_FIJO = {
    8:  [(1, 4)],          # Mat. Prima — 1 celda
    9:  [(1, 3)],          # Triplay    — 1 celda
    10: [(4, 3), (4, 4)],  # Almacén    — 2 celdas
    11: [(1, 1), (1, 2)],  # Baño       — 2 celdas
}


def _shapes_fijos():
    """
    Genera las formas (rectángulos) para cada elemento fijo según su tamaño real.
    Retorna lista de dicts compatibles con layout.shapes de Plotly.
    """
    shapes = []
    colores = {8: "royalblue", 9: "royalblue", 10: "royalblue", 11: "royalblue"}

    for id_el, celdas in CELDAS_POR_FIJO.items():
        xs = [c[0] for c in celdas]
        ys = [c[1] for c in celdas]
        x0 = min(xs) - 0.45
        x1 = max(xs) + 0.45
        y0 = min(ys) - 0.45
        y1 = max(ys) + 0.45
        shapes.append(dict(
            type="rect",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor="rgba(70, 130, 180, 0.6)",  # azul como en el PDF
            line=dict(color="darkblue", width=2),
            layer="below",
        ))

    return shapes


def _anotaciones_fijos():
    """Genera anotaciones de texto para cada elemento fijo."""
    anotaciones = []
    for id_el, celdas in CELDAS_POR_FIJO.items():
        xs = [c[0] for c in celdas]
        ys = [c[1] for c in celdas]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        anotaciones.append(dict(
            x=cx, y=cy,
            text=f"<b>({id_el}) {NOMBRES[id_el]}</b>",
            showarrow=False,
            font=dict(size=11, color="white"),
            bgcolor="rgba(0,0,0,0)",
        ))
    return anotaciones


def generar_animacion_2d(asignacion: dict, metrica: str, layout: Layout,
                         nombre_archivo: str, titulo: str = ""):
    """
    Genera animacion 2D vista superior del recorrido con elementos fijos a tamaño real.

    Parámetros:
        asignacion:     dict {id_maquina: (col, fila)}
        metrica:        'manhattan' o 'euclidiana'
        layout:         instancia de Layout
        nombre_archivo: ruta completa del archivo HTML
        titulo:         título del gráfico
    """
    posiciones = {**ELEMENTOS_FIJOS, **asignacion}
    fn_dist = manhattan if metrica == "manhattan" else euclidiana

    # Precalcular pasos del recorrido
    pasos = []
    dist_acum = 0.0
    for i in range(len(SECUENCIA) - 1):
        id_o = SECUENCIA[i]
        id_d = SECUENCIA[i + 1]
        p1 = posiciones[id_o]
        p2 = posiciones[id_d]
        dist = fn_dist(p1, p2)
        dist_acum += dist
        pasos.append({
            "origen": id_o, "destino": id_d,
            "x1": p1[0], "y1": p1[1],
            "x2": p2[0], "y2": p2[1],
            "dist": dist, "acum": dist_acum,
        })

    ids_moviles = sorted(asignacion.keys())

    # ── Figura base ──────────────────────────────────────────────────────────
    fig = go.Figure()

    # Traza vacía reservada para el recorrido (primer trace = índice 0)
    fig.add_trace(go.Scatter(
        x=[], y=[],
        mode="lines",
        line=dict(width=10, color="orangered"),
        name="Recorrido",
        hoverinfo="skip",
    ))

    # Máquinas móviles (círculos azules)
    for id_el in ids_moviles:
        pos = asignacion[id_el]
        fig.add_trace(go.Scatter(
            x=[pos[0]], y=[pos[1]],
            mode="markers+text",
            marker=dict(size=22, color="steelblue", symbol="circle",
                       line=dict(color="darkblue", width=2)),
            text=[f"({id_el}) {NOMBRES[id_el]}"],
            textposition="top center",
            textfont=dict(size=9, color="black"),
            name=NOMBRES[id_el],
            hovertemplate="<b>%{text}</b><extra></extra>",
        ))

    # Estrella de posición actual (vacía al inicio)
    fig.add_trace(go.Scatter(
        x=[], y=[],
        mode="markers",
        marker=dict(size=18, color="gold", symbol="star",
                   line=dict(color="red", width=3)),
        name="Posicion actual",
        hoverinfo="skip",
    ))

    # ── Frames de animación ──────────────────────────────────────────────────
    frames = []

    for paso_idx in range(len(pasos)):
        # Ruta acumulativa continua
        x_ruta, y_ruta = [], []
        for seg_idx in range(paso_idx + 1):
            p = pasos[seg_idx]
            if seg_idx == 0:
                x_ruta.append(p["x1"])
                y_ruta.append(p["y1"])
            x_ruta.append(p["x2"])
            y_ruta.append(p["y2"])

        paso_act = pasos[paso_idx]

        frame_data = [
            # Recorrido (índice 0)
            go.Scatter(x=x_ruta, y=y_ruta, mode="lines",
                      line=dict(width=10, color="orangered"),
                      hoverinfo="skip"),
        ]

        # Máquinas móviles
        for id_el in ids_moviles:
            pos = asignacion[id_el]
            frame_data.append(go.Scatter(
                x=[pos[0]], y=[pos[1]],
                mode="markers+text",
                marker=dict(size=22, color="steelblue", symbol="circle",
                           line=dict(color="darkblue", width=2)),
                text=[f"({id_el}) {NOMBRES[id_el]}"],
                textposition="top center",
                textfont=dict(size=9, color="black"),
                hovertemplate="<b>%{text}</b><extra></extra>",
            ))

        # Posición actual
        frame_data.append(go.Scatter(
            x=[paso_act["x2"]], y=[paso_act["y2"]],
            mode="markers",
            marker=dict(size=18, color="gold", symbol="star",
                       line=dict(color="red", width=3)),
            hoverinfo="skip",
        ))

        anno = (
            f"<b>Paso {paso_idx + 1}/{len(pasos)}</b>  |  "
            f"{NOMBRES[paso_act['origen']]} → {NOMBRES[paso_act['destino']]}  |  "
            f"Dist: {paso_act['dist']:.2f}  |  Acum: {paso_act['acum']:.2f}"
        )
        frames.append(go.Frame(
            data=frame_data,
            name=f"paso_{paso_idx}",
            layout=go.Layout(title_text=f"{titulo}<br>{anno}"),
        ))

    fig.frames = frames

    # ── Layout con shapes y anotaciones de elementos fijos ───────────────────
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=16, color="#222", family="Arial Black")),
        xaxis=dict(
            title="Columna",
            range=[0.5, GRID_COLS + 0.5],
            dtick=1,
            showgrid=True, gridwidth=2, gridcolor="rgba(0,0,0,0.15)",
            zeroline=False, tickfont=dict(size=13),
        ),
        yaxis=dict(
            title="Fila",
            range=[0.5, GRID_ROWS + 0.5],
            dtick=1,
            showgrid=True, gridwidth=2, gridcolor="rgba(0,0,0,0.15)",
            zeroline=False, tickfont=dict(size=13),
            scaleanchor="x", scaleratio=1,
        ),
        shapes=_shapes_fijos(),
        annotations=_anotaciones_fijos(),
        hovermode="closest",
        height=700,
        width=800,
        plot_bgcolor="rgba(245, 250, 255, 1)",
        paper_bgcolor="white",
        updatemenus=[dict(
            type="buttons",
            showactive=True,
            y=1.0, x=0.0,
            xanchor="left", yanchor="top",
            bgcolor="rgba(200,220,255,0.9)",
            bordercolor="darkblue",
            borderwidth=2,
            font=dict(size=13),
            buttons=[
                dict(label="▶ PLAY",
                     method="animate",
                     args=[None, {"frame": {"duration": 900, "redraw": True},
                                  "fromcurrent": True}]),
                dict(label="⏸ PAUSA",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
            ],
        )],
        sliders=[dict(
            steps=[dict(
                method="animate",
                args=[[f"paso_{k}"], {"frame": {"duration": 0, "redraw": True},
                                      "mode": "immediate"}],
                label=f"{k + 1}",
            ) for k in range(len(pasos))],
            active=0,
            y=-0.08, len=0.95,
            currentvalue=dict(prefix="Paso: ", visible=True,
                              font=dict(size=13, color="#cc0000")),
            pad=dict(b=10, t=50),
            bgcolor="rgba(200,220,255,0.5)",
            bordercolor="darkblue",
            borderwidth=1,
        )],
        showlegend=True,
        legend=dict(x=1.02, y=1.0, bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="gray", borderwidth=1),
        margin=dict(l=60, r=160, t=120, b=130),
        font=dict(family="Arial", size=12),
    )

    fig.write_html(
        nombre_archivo,
        config=dict(responsive=True, displayModeBar=True,
                    displaylogo=False,
                    modeBarButtonsToRemove=["lasso2d", "select2d"]),
    )
    print(f"  [OK] Guardado: {nombre_archivo}")
