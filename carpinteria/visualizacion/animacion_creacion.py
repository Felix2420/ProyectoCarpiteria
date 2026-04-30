# animacion_creacion.py — Muestra paso a paso cómo cada algoritmo crea un individuo.
# Ejecutar desde carpinteria/: python visualizacion/animacion_creacion.py

import os
import sys
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import MAQUINAS, NOMBRES, CELDAS_BLOQUEADAS, GRID_COLS, GRID_ROWS

# ─── Constantes ──────────────────────────────────────────────────────────────

CELDAS_POR_FIJO = {
    8:  [(1, 4)],
    9:  [(1, 3)],
    10: [(4, 3), (4, 4)],
    11: [(1, 1), (1, 2)],
}

CELDAS_DISP = [
    (col, row)
    for col in range(1, GRID_COLS + 1)
    for row in range(1, GRID_ROWS + 1)
    if (col, row) not in CELDAS_BLOQUEADAS
]

# ─── Helpers de grilla ───────────────────────────────────────────────────────

def _shapes_fijos(xref="x", yref="y"):
    shapes = []
    for celdas in CELDAS_POR_FIJO.values():
        xs = [c[0] for c in celdas]
        ys = [c[1] for c in celdas]
        shapes.append(dict(
            type="rect", xref=xref, yref=yref,
            x0=min(xs) - 0.46, y0=min(ys) - 0.46,
            x1=max(xs) + 0.46, y1=max(ys) + 0.46,
            fillcolor="rgba(70, 130, 180, 0.75)",
            line=dict(color="darkblue", width=2),
            layer="below",
        ))
    return shapes


def _annots_fijos(xref="x", yref="y"):
    annots = []
    for id_el, celdas in CELDAS_POR_FIJO.items():
        cx = sum(c[0] for c in celdas) / len(celdas)
        cy = sum(c[1] for c in celdas) / len(celdas)
        annots.append(dict(
            x=cx, y=cy, xref=xref, yref=yref,
            text=f"<b>{NOMBRES[id_el]}</b>",
            showarrow=False,
            font=dict(size=10, color="white"),
        ))
    return annots


def _grid_traces(asignadas=None, actual_celda=None, actual_id=None):
    asignadas = asignadas or {}
    ocupadas = set(asignadas.values()) | ({actual_celda} if actual_celda else set())
    libres = [c for c in CELDAS_DISP if c not in ocupadas]

    t_lib = go.Scatter(
        x=[c[0] for c in libres], y=[c[1] for c in libres],
        mode='markers+text',
        marker=dict(size=46, color='#BDD7EE', symbol='square',
                    line=dict(width=1.5, color='steelblue')),
        text=[f"({c[0]},{c[1]})" for c in libres],
        textposition='middle center', textfont=dict(size=9, color='#444'),
        hoverinfo='skip', showlegend=False,
    )

    t_asig = go.Scatter(
        x=[v[0] for v in asignadas.values()],
        y=[v[1] for v in asignadas.values()],
        mode='markers+text',
        marker=dict(size=40, color='#70AD47', symbol='circle',
                    line=dict(width=2.5, color='darkgreen')),
        text=[f"M{k}" for k in asignadas],
        textposition='middle center',
        textfont=dict(size=10, color='white', family='Arial Black'),
        hoverinfo='skip', showlegend=False,
    )

    if actual_celda and actual_id:
        t_act = go.Scatter(
            x=[actual_celda[0]], y=[actual_celda[1]],
            mode='markers+text',
            marker=dict(size=48, color='#FFD966', symbol='circle',
                        line=dict(width=3, color='darkorange')),
            text=[f"M{actual_id}"], textposition='middle center',
            textfont=dict(size=11, color='#333', family='Arial Black'),
            hoverinfo='skip', showlegend=False,
        )
    else:
        t_act = go.Scatter(x=[], y=[], mode='markers',
                           marker=dict(size=1, color='rgba(0,0,0,0)'),
                           hoverinfo='skip', showlegend=False)

    return [t_lib, t_asig, t_act]


def _controls(duration=1300):
    return (
        [dict(
            type="buttons", showactive=True,
            y=1.05, x=0.0, xanchor="left", yanchor="top",
            bgcolor="rgba(200,220,255,0.9)", bordercolor="darkblue", borderwidth=2,
            font=dict(size=13),
            buttons=[
                dict(label="▶ PLAY", method="animate",
                     args=[None, {"frame": {"duration": duration, "redraw": True},
                                  "fromcurrent": True, "transition": {"duration": 0}}]),
                dict(label="⏸ PAUSA", method="animate",
                     args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}]),
            ],
        )],
        None  # slider built per-function
    )


def _slider(frames):
    return [dict(
        steps=[dict(
            method="animate",
            args=[[f.name], {"frame": {"duration": 0, "redraw": True},
                             "mode": "immediate", "transition": {"duration": 0}}],
            label=f.name.replace("step_", ""),
        ) for f in frames],
        active=0, y=-0.05, len=0.92,
        currentvalue=dict(prefix="Paso: ", visible=True,
                          font=dict(size=13, color="#cc0000")),
        pad=dict(b=10, t=50),
        bgcolor="rgba(200,220,255,0.5)",
        bordercolor="darkblue", borderwidth=1,
    )]


# ─── GA ──────────────────────────────────────────────────────────────────────

def generar_animacion_ga(nombre_archivo: str, seed: int = 42):
    random.seed(seed)
    individuo = random.sample(CELDAS_DISP, len(MAQUINAS))

    shapes = _shapes_fijos()
    annots_base = _annots_fijos()

    def panel(asig):
        lines = ["<b>Individuo (lista):</b>"]
        for mid in MAQUINAS:
            if mid in asig:
                c = asig[mid]
                lines.append(f"  M{mid} {NOMBRES[mid][:10]}: ({c[0]},{c[1]}) ✓")
            else:
                lines.append(f"  M{mid} {NOMBRES[mid][:10]}: ?")
        return dict(
            x=4.55, y=4.1, xref="x", yref="y",
            text="<br>".join(lines),
            showarrow=False, align="left",
            font=dict(size=9, family="Courier New, monospace"),
            bgcolor="rgba(255,255,255,0.93)",
            bordercolor="#4472C4", borderwidth=1, borderpad=5,
        )

    frames = []

    def push(name, titulo, asig_prev, actual_cel, actual_id, asig_full):
        frames.append(go.Frame(
            data=_grid_traces(asignadas=asig_prev, actual_celda=actual_cel, actual_id=actual_id),
            layout=go.Layout(title_text=titulo,
                             annotations=annots_base + [panel(asig_full)]),
            name=name,
        ))

    push("step_0",
         "AG — Creación de individuo<br>"
         "<sub>Paso 0/7 — Se tienen 10 celdas libres. "
         "Se elegirán 7 al azar <b>sin reemplazo</b> usando random.sample()</sub>",
         {}, None, None, {})

    asig = {}
    for i, mid in enumerate(MAQUINAS):
        celda = individuo[i]
        prev = dict(asig)
        asig[mid] = celda
        push(f"step_{i+1}",
             f"AG — Creación de individuo<br>"
             f"<sub>Paso {i+1}/7 — random.sample() selecciona: "
             f"M{mid} ({NOMBRES[mid]}) → celda ({celda[0]},{celda[1]})</sub>",
             prev, celda, mid, dict(asig))

    push("step_final",
         "AG — Individuo completo<br>"
         f"<sub>Resultado: {individuo}<br>"
         "Lista de 7 celdas, una por máquina, en el orden de MAQUINAS[]</sub>",
         dict(zip(MAQUINAS, individuo)), None, None, dict(zip(MAQUINAS, individuo)))

    fig = go.Figure(data=frames[0].data)
    fig.update_layout(
        title=dict(text=frames[0].layout.title.text, font=dict(size=14, color="#222")),
        xaxis=dict(title="Columna", range=[0.5, 5.15], dtick=1,
                   showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis=dict(title="Fila", range=[0.5, 4.65], dtick=1,
                   showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False,
                   scaleanchor="x", scaleratio=1),
        shapes=shapes,
        annotations=annots_base + [panel({})],
        height=680, width=790,
        plot_bgcolor='rgba(245, 250, 255, 1)', paper_bgcolor='white',
        font=dict(family='Arial', size=12),
        margin=dict(l=55, r=60, t=115, b=120),
        updatemenus=_controls()[0],
        sliders=_slider(frames),
        showlegend=False,
    )
    fig.frames = frames
    fig.write_html(nombre_archivo, config=dict(responsive=True, displaylogo=False))
    print(f"  [OK] {nombre_archivo}")


# ─── cGA ─────────────────────────────────────────────────────────────────────

def generar_animacion_cga(nombre_archivo: str, seed: int = 42):
    random.seed(seed)
    n_maq = len(MAQUINAS)
    n_cel = len(CELDAS_DISP)
    P_base = [[1.0 / n_cel] * n_cel for _ in range(n_maq)]

    # Reproducir _muestrear() de compacto.py
    usadas, individuo, selecciones = set(), [], []
    for i in range(n_maq):
        probs = [(P_base[i][j], j) for j in range(n_cel) if j not in usadas]
        probs.sort(reverse=True)
        disponibles = [j for _, j in probs]
        pesos = [p for p, _ in probs]
        total = sum(pesos)
        r, acum = random.random() * total, 0.0
        elegido = disponibles[-1]
        for p, j in zip(pesos, disponibles):
            acum += p
            if r <= acum:
                elegido = j
                break
        usadas.add(elegido)
        individuo.append(CELDAS_DISP[elegido])
        selecciones.append(elegido)

    cel_labels = [f"({c[0]},{c[1]})" for c in CELDAS_DISP]
    maq_labels = [f"M{m} {NOMBRES[m][:9]}" for m in MAQUINAS]

    def make_heatmap(fila_activa=None):
        z = [list(row) for row in P_base]
        # Resaltar celdas ya seleccionadas en filas ya procesadas
        if fila_activa is not None:
            for i in range(fila_activa):
                z[i][selecciones[i]] = 0.19
        return go.Heatmap(
            z=z,
            x=cel_labels, y=maq_labels,
            text=[[f"{v:.2f}" for v in row] for row in z],
            texttemplate="%{text}",
            colorscale=[[0, "#f5f8ff"], [0.45, "#93C6E8"], [1, "#1A4F8A"]],
            zmin=0, zmax=0.20,
            showscale=True,
            colorbar=dict(x=0.51, y=0.5, len=0.75, thickness=12,
                          title=dict(text="P", side="right"),
                          tickfont=dict(size=9)),
            hoverinfo='skip', xgap=2, ygap=2,
        )

    def hm_annots(fila_activa, cel_elegida_idx):
        annots = []
        if fila_activa is None:
            return annots
        y_label = maq_labels[fila_activa]
        annots.append(dict(
            x=0.51, y=y_label, xref="paper", yref="y",
            text="◀ sorteo aquí",
            showarrow=False,
            font=dict(size=10, color="darkorange", family="Arial Black"),
            xanchor="right",
            bgcolor="rgba(255,230,150,0.85)",
            bordercolor="orange", borderpad=3, borderwidth=1,
        ))
        if cel_elegida_idx is not None:
            annots.append(dict(
                x=cel_labels[cel_elegida_idx], y=y_label,
                xref="x", yref="y",
                text="★",
                showarrow=False,
                font=dict(size=18, color="#CC0000"),
            ))
        return annots

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.56, 0.44],
        subplot_titles=[
            "Matriz P [7 máquinas × 10 celdas]",
            "Grilla (Vista Superior)",
        ],
        horizontal_spacing=0.10,
    )

    fig.add_trace(make_heatmap(), row=1, col=1)
    for t in _grid_traces():
        fig.add_trace(t, row=1, col=2)
    # trazas: 0=heatmap, 1=libres, 2=asignadas, 3=actual

    shapes_grid = _shapes_fijos(xref="x2", yref="y2")
    annots_grid = _annots_fijos(xref="x2", yref="y2")

    frames = []

    def push(name, titulo, fila_act, cel_idx, asig_prev, actual_cel, actual_id):
        frames.append(go.Frame(
            data=[make_heatmap(fila_act)]
                 + _grid_traces(asignadas=asig_prev,
                                actual_celda=actual_cel, actual_id=actual_id),
            traces=[0, 1, 2, 3],
            layout=go.Layout(title_text=titulo,
                             annotations=annots_grid + hm_annots(fila_act, cel_idx)),
            name=name,
        ))

    push("step_0",
         "cGA — Muestreo de individuo<br>"
         "<sub>Paso 0/7 — P inicial uniforme: P[i][j] = 1/10 = 0.10 para todas las celdas. "
         "Cada máquina tiene igual probabilidad en cada celda.</sub>",
         None, None, {}, None, None)

    asig = {}
    for i, mid in enumerate(MAQUINAS):
        cel_idx = selecciones[i]
        celda = individuo[i]
        prev = dict(asig)
        asig[mid] = celda
        push(f"step_{i+1}",
             f"cGA — Muestreo de individuo<br>"
             f"<sub>Paso {i+1}/7 — M{mid} ({NOMBRES[mid]}): "
             f"sorteo ponderado de fila {i} de P → celda ({celda[0]},{celda[1]}) "
             f"(★ rojo). Esa celda queda bloqueada para las siguientes máquinas.</sub>",
             i, cel_idx, prev, celda, mid)

    push("step_final",
         "cGA — Individuo muestreado<br>"
         "<sub>7 celdas elegidas por sorteo ponderado sin reemplazo. "
         "Tras evaluar dos individuos, P se actualiza: ganador ↑ probabilidades, perdedor ↓.</sub>",
         None, None, dict(zip(MAQUINAS, individuo)), None, None)

    fig.frames = frames
    fig.update_layout(
        title=dict(text=frames[0].layout.title.text, font=dict(size=14)),
        shapes=shapes_grid,
        annotations=annots_grid,
        height=640, width=1160,
        plot_bgcolor='rgba(245, 250, 255, 1)', paper_bgcolor='white',
        font=dict(family='Arial', size=11),
        margin=dict(l=55, r=55, t=115, b=130),
        xaxis=dict(title="Celda disponible", tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(title="Máquina", tickfont=dict(size=9.5)),
        xaxis2=dict(title="Columna", range=[0.5, 4.5], dtick=1,
                    showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis2=dict(title="Fila", range=[0.5, 4.5], dtick=1,
                    showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        updatemenus=_controls(1400)[0],
        sliders=_slider(frames),
        showlegend=False,
    )
    fig.write_html(nombre_archivo, config=dict(responsive=True, displaylogo=False))
    print(f"  [OK] {nombre_archivo}")


# ─── ES ──────────────────────────────────────────────────────────────────────

def generar_animacion_es(nombre_archivo: str, seed: int = 42):
    random.seed(seed)
    n_maq = len(MAQUINAS)
    n_cel = len(CELDAS_DISP)

    indices = random.sample(range(n_cel), n_maq)
    vector = [float(i) for i in indices]

    orden = sorted(range(n_maq), key=lambda i: vector[i])

    # Decodificar (_decodificar_real de estrategia_ev.py)
    usadas, asig_final = set(), {}
    decode_steps = []
    for idx in orden:
        pref = int(round(vector[idx])) % n_cel
        for delta in range(n_cel):
            for signo in (0, 1, -1):
                candidato = (pref + signo * delta) % n_cel
                if candidato not in usadas:
                    usadas.add(candidato)
                    celda = CELDAS_DISP[candidato]
                    asig_final[MAQUINAS[idx]] = celda
                    decode_steps.append((idx, candidato, celda))
                    break
            if MAQUINAS[idx] in asig_final:
                break

    labels_orig = [f"M{m}<br>{NOMBRES[m][:8]}" for m in MAQUINAS]
    labels_sort = [f"M{MAQUINAS[i]}<br>({vector[i]:.1f})" for i in orden]
    vals_sort = [vector[i] for i in orden]

    def make_bars(mode="original", hl=None):
        if mode == "original":
            x = labels_orig
            y = vector
            colors = ['#BDD7EE'] * n_maq
        else:
            x = labels_sort
            y = vals_sort
            colors = ['#FFD966' if hl == k else '#93C6E8'
                      for k in range(n_maq)]
        return go.Bar(
            x=x, y=y,
            marker_color=colors,
            marker_line=dict(color='steelblue', width=1.5),
            text=[f"{v:.1f}" for v in y],
            textposition='outside', textfont=dict(size=11, color='#222'),
            hoverinfo='skip', showlegend=False,
        )

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.48, 0.52],
        subplot_titles=[
            "Vector real (7 flotantes = índices de celda)",
            "Grilla (Vista Superior)",
        ],
        horizontal_spacing=0.10,
    )

    fig.add_trace(make_bars(), row=1, col=1)
    for t in _grid_traces():
        fig.add_trace(t, row=1, col=2)

    shapes_grid = _shapes_fijos(xref="x2", yref="y2")
    annots_grid = _annots_fijos(xref="x2", yref="y2")

    frames = []

    def push(name, titulo, bars, asig_prev, actual_cel, actual_id):
        frames.append(go.Frame(
            data=[bars] + _grid_traces(asignadas=asig_prev,
                                       actual_celda=actual_cel, actual_id=actual_id),
            traces=[0, 1, 2, 3],
            layout=go.Layout(title_text=titulo, annotations=annots_grid),
            name=name,
        ))

    push("step_0",
         "EE — Creación de individuo (representación real)<br>"
         f"<sub>Paso 0 — Se generan 7 flotantes aleatorios (índices de celda): "
         f"{[f'{v:.1f}' for v in vector]}</sub>",
         make_bars("original"), {}, None, None)

    orden_str = " → ".join(f"M{MAQUINAS[i]}" for i in orden)
    push("step_1",
         "EE — Creación de individuo<br>"
         f"<sub>Paso 1 — Ordenar máquinas por valor flotante (↑): {orden_str}. "
         "Este orden determina quién elige celda primero durante la decodificación.</sub>",
         make_bars("sorted"), {}, None, None)

    asig = {}
    for step_i, (maq_idx, cel_idx, celda) in enumerate(decode_steps):
        mid = MAQUINAS[maq_idx]
        prev = dict(asig)
        asig[mid] = celda
        pref = int(round(vector[maq_idx])) % n_cel
        push(f"step_{step_i+2}",
             f"EE — Creación de individuo<br>"
             f"<sub>Paso {step_i+2} — M{mid} ({NOMBRES[mid]}): "
             f"valor {vector[maq_idx]:.1f} → índice preferido = {pref} "
             f"→ asignada celda ({celda[0]},{celda[1]})</sub>",
             make_bars("sorted", hl=step_i), prev, celda, mid)

    push("step_final",
         "EE — Individuo completo<br>"
         "<sub>Vector real decodificado: flotante → entero → celda más cercana libre. "
         "Permite mutación gaussiana continua con mapeo a espacio discreto sin colisiones.</sub>",
         make_bars("sorted"),
         {m: asig_final[m] for m in MAQUINAS}, None, None)

    fig.frames = frames
    fig.update_layout(
        title=dict(text=frames[0].layout.title.text, font=dict(size=14)),
        shapes=shapes_grid,
        annotations=annots_grid,
        height=640, width=1160,
        plot_bgcolor='rgba(245, 250, 255, 1)', paper_bgcolor='white',
        font=dict(family='Arial', size=11),
        margin=dict(l=55, r=55, t=115, b=130),
        xaxis=dict(title="Máquina", tickangle=-20, tickfont=dict(size=9.5)),
        yaxis=dict(title="Valor flotante (índice de celda)", range=[0, n_cel + 0.8]),
        xaxis2=dict(title="Columna", range=[0.5, 4.5], dtick=1,
                    showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        yaxis2=dict(title="Fila", range=[0.5, 4.5], dtick=1,
                    showgrid=True, gridcolor='rgba(0,0,0,0.1)', zeroline=False),
        updatemenus=_controls(1400)[0],
        sliders=_slider(frames),
        showlegend=False,
    )
    fig.write_html(nombre_archivo, config=dict(responsive=True, displaylogo=False))
    print(f"  [OK] {nombre_archivo}")


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "resultados")
    os.makedirs(out_dir, exist_ok=True)

    print("Generando animaciones de creación de individuos...")
    generar_animacion_ga(os.path.join(out_dir, "creacion_ga.html"))
    generar_animacion_cga(os.path.join(out_dir, "creacion_cga.html"))
    generar_animacion_es(os.path.join(out_dir, "creacion_es.html"))
    print("\n¡Listo! Archivos en resultados/")
