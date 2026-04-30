# generar_pdf.py — Genera PDF explicando cómo cada algoritmo crea un individuo.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "carpinteria"))

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import (HexColor, black, white, Color)
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.flowables import Flowable

# ── Paleta de colores ────────────────────────────────────────────────────────
AZUL_OSCURO  = HexColor("#1a237e")
AZUL_MEDIO   = HexColor("#1565c0")
AZUL_CLARO   = HexColor("#e3f2fd")
AZUL_HEADER  = HexColor("#1976d2")
VERDE        = HexColor("#2e7d32")
VERDE_CLARO  = HexColor("#e8f5e9")
NARANJA      = HexColor("#e65100")
NARANJA_CLARO= HexColor("#fff3e0")
MORADO       = HexColor("#4a148c")
MORADO_CLARO = HexColor("#f3e5f5")
GRIS_CLARO   = HexColor("#f5f5f5")
GRIS_BORDE   = HexColor("#bdbdbd")
ROJO         = HexColor("#c62828")

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados",
                      "explicacion_algoritmos.pdf")

# ── Estilos ──────────────────────────────────────────────────────────────────
def crear_estilos():
    base = getSampleStyleSheet()

    estilos = {
        "titulo_doc": ParagraphStyle(
            "titulo_doc", parent=base["Title"],
            fontSize=22, textColor=white,
            alignment=TA_CENTER, leading=28,
            fontName="Helvetica-Bold",
        ),
        "subtitulo_doc": ParagraphStyle(
            "subtitulo_doc", parent=base["Normal"],
            fontSize=12, textColor=HexColor("#e3f2fd"),
            alignment=TA_CENTER, leading=16,
            fontName="Helvetica",
        ),
        "titulo_seccion": ParagraphStyle(
            "titulo_seccion", parent=base["Heading1"],
            fontSize=16, textColor=white,
            spaceBefore=0, spaceAfter=0,
            fontName="Helvetica-Bold",
            alignment=TA_LEFT, leading=20,
        ),
        "titulo_sub": ParagraphStyle(
            "titulo_sub", parent=base["Heading2"],
            fontSize=13, textColor=AZUL_OSCURO,
            spaceBefore=10, spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "cuerpo": ParagraphStyle(
            "cuerpo", parent=base["Normal"],
            fontSize=10.5, textColor=black,
            leading=15, alignment=TA_JUSTIFY,
            fontName="Helvetica",
            spaceAfter=6,
        ),
        "codigo": ParagraphStyle(
            "codigo", parent=base["Code"],
            fontSize=9, textColor=HexColor("#1a237e"),
            fontName="Courier",
            leading=13, leftIndent=12,
            spaceAfter=4,
        ),
        "paso": ParagraphStyle(
            "paso", parent=base["Normal"],
            fontSize=10.5, textColor=black,
            leading=15, fontName="Helvetica",
            leftIndent=16, spaceAfter=4,
        ),
        "nota": ParagraphStyle(
            "nota", parent=base["Normal"],
            fontSize=9.5, textColor=HexColor("#555555"),
            leading=13, fontName="Helvetica-Oblique",
            leftIndent=12, spaceAfter=4,
        ),
        "celda_tabla": ParagraphStyle(
            "celda_tabla", parent=base["Normal"],
            fontSize=9.5, fontName="Helvetica",
            leading=12, alignment=TA_CENTER,
        ),
        "celda_tabla_bold": ParagraphStyle(
            "celda_tabla_bold", parent=base["Normal"],
            fontSize=9.5, fontName="Helvetica-Bold",
            leading=12, alignment=TA_CENTER,
        ),
    }
    return estilos


class CajaColoreada(Flowable):
    """Rectángulo de color de fondo para encabezados de sección."""
    def __init__(self, texto, estilo, color_fondo, ancho, alto=32, radio=6):
        Flowable.__init__(self)
        self.texto = texto
        self.estilo = estilo
        self.color_fondo = color_fondo
        self.ancho = ancho
        self.alto = alto
        self.radio = radio

    def wrap(self, *args):
        return self.ancho, self.alto

    def draw(self):
        c = self.canv
        c.setFillColor(self.color_fondo)
        c.roundRect(0, 0, self.ancho, self.alto, self.radio, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(14, 10, self.texto)


def tabla_grilla(celdas_disponibles, asignacion, estilos):
    """Genera tabla visual de la grilla 4x4 con asignación de ejemplo."""
    from config import ELEMENTOS_FIJOS, NOMBRES, CELDAS_BLOQUEADAS

    nombres_cortos = {
        1: "E.Trab", 2: "Destro", 3: "S.Cinta",
        4: "Cantea", 5: "Cepill", 6: "Trompo", 7: "Esclop",
        8: "Mat.P", 9: "Triply", 10: "Almacen", 11: "Bano",
    }

    # Mapa inverso celda → contenido
    mapa = {}
    for id_el, pos in ELEMENTOS_FIJOS.items():
        mapa[pos] = ("fijo", id_el)
    mapa[(4, 4)] = ("fijo_extra", 10)
    mapa[(1, 2)] = ("fijo_extra", 11)
    for id_m, pos in asignacion.items():
        mapa[pos] = ("maquina", id_m)

    data = []
    # Encabezado columnas
    header = [Paragraph("<b>Fila\\Col</b>", estilos["celda_tabla_bold"])] + \
             [Paragraph(f"<b>Col {c}</b>", estilos["celda_tabla_bold"]) for c in range(1, 5)]
    data.append(header)

    for f in range(4, 0, -1):
        fila = [Paragraph(f"<b>Fila {f}</b>", estilos["celda_tabla_bold"])]
        for c in range(1, 5):
            celda = (c, f)
            if celda in mapa:
                tipo, id_el = mapa[celda]
                if tipo in ("fijo", "fijo_extra"):
                    txt = Paragraph(
                        f"<font color='white'><b>({id_el})<br/>{nombres_cortos[id_el]}</b></font>",
                        estilos["celda_tabla"]
                    )
                else:
                    txt = Paragraph(
                        f"<b>({id_el})<br/>{nombres_cortos[id_el]}</b>",
                        estilos["celda_tabla_bold"]
                    )
            else:
                txt = Paragraph("—", estilos["celda_tabla"])
            fila.append(txt)
        data.append(fila)

    # Colores por celda
    style = [
        ("GRID",      (0, 0), (-1, -1), 1, GRIS_BORDE),
        ("ALIGN",     (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
        ("ROWHEIGHT", (0, 0), (-1, -1), 36),
        ("FONTSIZE",  (0, 0), (-1, -1), 9),
        # Encabezado
        ("BACKGROUND", (0, 0), (-1, 0), AZUL_MEDIO),
        ("TEXTCOLOR",  (0, 0), (-1, 0), white),
        ("BACKGROUND", (0, 1), (0, -1), GRIS_CLARO),
    ]

    # Colorear celdas fijas
    fijos_colores = {
        (1, 4): (1, 1), (1, 3): (2, 1),  # Mat.Prima fila4, Triplay fila3
        (4, 3): (1, 4), (4, 4): (2, 4),  # Almacén fila3 y fila4→row2,col4 y row1,col4
        (1, 1): (4, 1), (1, 2): (3, 1),  # Baño fila1 y fila2
    }
    # Índices en la tabla: fila 0=header, fila 1=fila4, fila 2=fila3, fila 3=fila2, fila 4=fila1
    fila_map = {4: 1, 3: 2, 2: 3, 1: 4}
    for (c, f), id_el in {**{(1,4):8,(1,3):9,(4,3):10,(4,4):10,(1,1):11,(1,2):11}}.items():
        tr = fila_map[f]
        tc = c  # columna en tabla (col 1 → índice 1)
        style.append(("BACKGROUND", (tc, tr), (tc, tr), AZUL_MEDIO))
        style.append(("TEXTCOLOR",  (tc, tr), (tc, tr), white))

    # Colorear máquinas
    for id_m, (c, f) in asignacion.items():
        tr = fila_map[f]
        tc = c
        style.append(("BACKGROUND", (tc, tr), (tc, tr), HexColor("#bbdefb")))

    t = Table(data, colWidths=[1.1*cm] + [2.5*cm]*4)
    t.setStyle(TableStyle(style))
    return t


# ── SECCIONES DEL PDF ────────────────────────────────────────────────────────

def seccion_intro(story, estilos, W):
    story.append(CajaColoreada("   Contexto del Problema", estilos["titulo_seccion"],
                               AZUL_OSCURO, W))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "La carpintería tiene una <b>grilla de 4×4 celdas</b>. Cuatro elementos son <b>fijos</b> "
        "(azul en el PDF): Mat. Prima (8), Triplay (9), Almacén (10) y Baño (11). "
        "Las <b>7 máquinas</b> (IDs 1–7) deben ubicarse en las <b>10 celdas disponibles</b> "
        "minimizando el recorrido del personal según la secuencia:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph(
        "<b>1→8, 8→1, 1→4, 4→5, 5→3, 3→4, 4→3, 3→1, 1→9, 9→1, 1→3, 3→1, 1→10</b>",
        estilos["codigo"]
    ))
    story.append(Spacer(1, 6))

    data_maq = [
        [Paragraph("<b>ID</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Máquina</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>ID</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Máquina</b>", estilos["celda_tabla_bold"])],
        ["1", "E. Trabajo",   "5", "Cepillo"],
        ["2", "Destrozadora", "6", "Trompo"],
        ["3", "Sierra Cinta", "7", "Esclopeadora"],
        ["4", "Canteadora",   "",  ""],
    ]
    t = Table(data_maq, colWidths=[1.2*cm, 5*cm, 1.2*cm, 5*cm])
    t.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("BACKGROUND", (0,0), (-1, 0), AZUL_MEDIO),
        ("TEXTCOLOR",  (0,0), (-1, 0), white),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 18),
        ("BACKGROUND", (0,1), (-1,-1), AZUL_CLARO),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    # Grilla visual
    story.append(Paragraph("<b>Distribución de la grilla (layout del PDF):</b>", estilos["titulo_sub"]))
    data_grilla = [
        ["Col→", "Col 1", "Col 2", "Col 3", "Col 4"],
        ["Fila 4", "(8) Mat. Prima", "Libre", "Libre", "Libre"],
        ["Fila 3", "(9) Triplay",    "Libre", "Libre", "(10) Almacén"],
        ["Fila 2", "(11) Baño",      "Libre", "Libre", "Libre"],
        ["Fila 1", "(11) Baño",      "Libre", "Libre", "Libre"],
    ]
    tg = Table(data_grilla, colWidths=[1.5*cm, 3.1*cm, 2.8*cm, 2.8*cm, 3.1*cm])
    tg.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 1, GRIS_BORDE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 22),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("BACKGROUND", (0,0), (-1, 0), AZUL_OSCURO),
        ("TEXTCOLOR",  (0,0), (-1, 0), white),
        ("BACKGROUND", (0,1), (0,-1), AZUL_OSCURO),
        ("TEXTCOLOR",  (0,1), (0,-1), white),
        # Fijos azul
        ("BACKGROUND", (1,1), (1,1), AZUL_MEDIO),  # Mat. Prima
        ("TEXTCOLOR",  (1,1), (1,1), white),
        ("BACKGROUND", (1,2), (1,2), AZUL_MEDIO),  # Triplay
        ("TEXTCOLOR",  (1,2), (1,2), white),
        ("BACKGROUND", (4,2), (4,2), AZUL_MEDIO),  # Almacén fila3
        ("TEXTCOLOR",  (4,2), (4,2), white),
        ("BACKGROUND", (1,3), (1,4), AZUL_MEDIO),  # Baño filas 1-2
        ("TEXTCOLOR",  (1,3), (1,4), white),
        # Libres verde claro
        ("BACKGROUND", (2,1), (4,1), VERDE_CLARO),
        ("BACKGROUND", (2,2), (3,2), VERDE_CLARO),
        ("BACKGROUND", (2,3), (4,3), VERDE_CLARO),
        ("BACKGROUND", (2,4), (4,4), VERDE_CLARO),
    ]))
    story.append(tg)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Azul = elementos fijos (no se mueven). Verde = celdas disponibles para máquinas (10 celdas).</i>",
        estilos["nota"]
    ))


def seccion_ga(story, estilos, W):
    story.append(PageBreak())
    story.append(CajaColoreada("   GA — Algoritmo Genético Tradicional", estilos["titulo_seccion"],
                               VERDE, W))
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Qué es un individuo en GA?", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Un <b>individuo</b> es una lista de 7 celdas, una por máquina, en el orden "
        "[máq.1, máq.2, ..., máq.7]. Representa <b>dónde se ubica cada máquina</b> "
        "en la grilla. No puede haber dos máquinas en la misma celda.",
        estilos["cuerpo"]
    ))

    story.append(Paragraph("Paso 1 — Tomar las 10 celdas disponibles", estilos["titulo_sub"]))
    story.append(Paragraph(
        "El algoritmo parte de la lista de celdas que NO están bloqueadas por elementos fijos:",
        estilos["cuerpo"]
    ))
    celdas = ["(2,1)", "(2,2)", "(2,3)", "(2,4)",
              "(3,1)", "(3,2)", "(3,3)", "(3,4)", "(4,1)", "(4,2)"]
    data = [[Paragraph(f"<b>{i+1}</b>", estilos["celda_tabla_bold"]),
             Paragraph(c, estilos["celda_tabla"])] for i, c in enumerate(celdas)]
    t = Table(data, colWidths=[1.5*cm, 2.5*cm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 16),
        ("BACKGROUND", (0,0), (-1,-1), VERDE_CLARO),
        ("BACKGROUND", (0,0), (0,-1), VERDE),
        ("TEXTCOLOR",  (0,0), (0,-1), white),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Paso 2 — Selección aleatoria sin repetición (random.sample)", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Se eligen <b>7 celdas distintas</b> al azar de las 10 disponibles, una por máquina. "
        "Esto garantiza que no haya colisiones. La función utilizada es:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph("individuo = random.sample(celdas_disponibles, 7)", estilos["codigo"]))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Paso 3 — Resultado: individuo creado", estilos["titulo_sub"]))
    story.append(Paragraph(
        "El individuo resultante asigna una celda a cada máquina. Por ejemplo:",
        estilos["cuerpo"]
    ))

    ejemplo_ga = {1:(2,3), 2:(3,1), 3:(3,3), 4:(2,2), 5:(3,2), 6:(4,2), 7:(2,4)}
    data_ej = [
        [Paragraph("<b>Máquina</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Nombre</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Celda asignada</b>", estilos["celda_tabla_bold"])],
    ]
    nombres = {1:"E.Trabajo",2:"Destrozadora",3:"Sierra Cinta",
               4:"Canteadora",5:"Cepillo",6:"Trompo",7:"Esclopeadora"}
    for id_m, celda in ejemplo_ga.items():
        data_ej.append([
            Paragraph(str(id_m), estilos["celda_tabla"]),
            Paragraph(nombres[id_m], estilos["celda_tabla"]),
            Paragraph(str(celda), estilos["celda_tabla"]),
        ])
    t2 = Table(data_ej, colWidths=[2*cm, 4.5*cm, 3.5*cm])
    t2.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 18),
        ("BACKGROUND", (0,0), (-1, 0), VERDE),
        ("TEXTCOLOR",  (0,0), (-1, 0), white),
        ("BACKGROUND", (0,1), (-1,-1), VERDE_CLARO),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, VERDE_CLARO]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Cómo evoluciona la población?", estilos["titulo_sub"]))
    pasos_ev = [
        ("Población inicial", "Se crean 100 individuos aleatorios con el mismo proceso."),
        ("Evaluación (fitness)", "Se calcula el costo total del recorrido para cada individuo. "
                                  "Menor costo = mejor individuo."),
        ("Selección por torneo", "Se eligen grupos de 3 individuos al azar y gana el de menor costo."),
        ("Cruce OX (Order Crossover)", "Se combina el material genético de dos padres preservando "
                                        "el orden relativo de las celdas."),
        ("Mutación por swap", "Con probabilidad 15%, se intercambian dos celdas dentro del individuo."),
        ("Elitismo", "El mejor individuo de la generación siempre pasa a la siguiente."),
    ]
    data_ev = [[Paragraph(f"<b>{p}</b>", estilos["celda_tabla_bold"]),
                Paragraph(d, estilos["celda_tabla"])] for p, d in pasos_ev]
    t3 = Table(data_ev, colWidths=[4.5*cm, 9*cm])
    t3.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 28),
        ("FONTSIZE",   (0,0), (-1,-1), 9.5),
        ("BACKGROUND", (0,0), (0,-1), VERDE_CLARO),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, VERDE_CLARO]),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
    ]))
    story.append(t3)


def seccion_cga(story, estilos, W):
    story.append(PageBreak())
    story.append(CajaColoreada("   cGA — Algoritmo Genético Compacto", estilos["titulo_seccion"],
                               NARANJA, W))
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Qué es un individuo en cGA?", estilos["titulo_sub"]))
    story.append(Paragraph(
        "El cGA <b>no mantiene una población explícita</b>. En su lugar guarda una "
        "<b>matriz de probabilidades P</b> de tamaño 7×10 (7 máquinas × 10 celdas). "
        "Cada valor P[i][j] representa la probabilidad de que la <b>máquina i</b> "
        "sea asignada a la <b>celda j</b>.",
        estilos["cuerpo"]
    ))

    story.append(Paragraph("Paso 1 — Inicializar P con probabilidad uniforme", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Al inicio, como no se sabe nada, todas las celdas son igual de probables. "
        "La probabilidad inicial es <b>1/10 = 0.10</b> para cada combinación máquina–celda:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph("P[i][j] = 1 / 10 = 0.10  para toda máquina i y celda j", estilos["codigo"]))
    story.append(Spacer(1, 6))

    celdas_header = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]
    maq_names = ["Máq.1", "Máq.2", "Máq.3", "Máq.4", "Máq.5", "Máq.6", "Máq.7"]
    data_p = [[Paragraph("", estilos["celda_tabla"])] +
              [Paragraph(f"<b>{c}</b>", estilos["celda_tabla_bold"]) for c in celdas_header]]
    for i, m in enumerate(maq_names):
        fila = [Paragraph(f"<b>{m}</b>", estilos["celda_tabla_bold"])]
        for j in range(10):
            fila.append(Paragraph("0.10", estilos["celda_tabla"]))
        data_p.append(fila)
    t_p = Table(data_p, colWidths=[1.5*cm] + [1.1*cm]*10)
    t_p.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 16),
        ("FONTSIZE",   (0,0), (-1,-1), 8.5),
        ("BACKGROUND", (0,0), (-1, 0), NARANJA),
        ("TEXTCOLOR",  (0,0), (-1, 0), white),
        ("BACKGROUND", (0,1), (0,-1), NARANJA_CLARO),
        ("BACKGROUND", (1,1), (-1,-1), HexColor("#fff8f0")),
    ]))
    story.append(t_p)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Paso 2 — Muestrear un individuo desde P", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Para crear un individuo se procesa <b>cada máquina en orden</b>. "
        "Para la máquina i, se elige una celda disponible según las probabilidades "
        "de la fila P[i], sin repetir celdas ya usadas:",
        estilos["cuerpo"]
    ))
    pasos_muest = [
        ("Máquina 1 (E. Trabajo)", "Todas las celdas disponibles con prob. 0.10. Se sortea → resulta (2,3)."),
        ("Máquina 2 (Destrozadora)", "Se excluye (2,3). Quedan 9 celdas. Se sortea → resulta (3,1)."),
        ("Máquina 3 (Sierra Cinta)", "Se excluyen (2,3) y (3,1). Quedan 8 celdas. Se sortea → resulta (3,3)."),
        ("... y así", "Se continúa hasta asignar todas las 7 máquinas sin repetir celda."),
    ]
    data_m = [[Paragraph(f"<b>{p}</b>", estilos["celda_tabla_bold"]),
               Paragraph(d, estilos["celda_tabla"])] for p, d in pasos_muest]
    t_m = Table(data_m, colWidths=[4.5*cm, 9*cm])
    t_m.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 26),
        ("FONTSIZE",   (0,0), (-1,-1), 9.5),
        ("BACKGROUND", (0,0), (0,-1), NARANJA_CLARO),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [white, NARANJA_CLARO]),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(t_m)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Paso 3 — Competencia y actualización de P", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Se generan <b>2 individuos</b> con el proceso anterior y se evalúa cuál tiene "
        "menor costo de recorrido. El ganador <b>incrementa</b> sus probabilidades en P "
        "y el perdedor las <b>reduce</b> en <b>1/N</b> (N = 200, tamaño virtual):",
        estilos["cuerpo"]
    ))
    story.append(Paragraph(
        "Si ganador usó celda j para máquina i:\n"
        "  P[i][j] += 1/200 = +0.005   (se vuelve más probable)\n"
        "  P[i][j] -= 1/200 = -0.005   (para el perdedor: menos probable)",
        estilos["codigo"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Al converger</b>, cada fila de P tendrá un valor cercano a 1.0 en una sola celda "
        "y 0.0 en el resto: el algoritmo ha encontrado la mejor asignación para esa máquina.",
        estilos["cuerpo"]
    ))


def seccion_es(story, estilos, W):
    story.append(PageBreak())
    story.append(CajaColoreada("   ES — Estrategia Evolutiva (mu + lambda)", estilos["titulo_seccion"],
                               MORADO, W))
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Qué es un individuo en ES?", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Un individuo en ES es un <b>vector de 7 números reales (flotantes)</b>, uno por máquina. "
        "Cada número representa un <b>índice continuo</b> dentro de la lista de celdas disponibles. "
        "Al momento de evaluar, se convierte al espacio discreto (una celda real).",
        estilos["cuerpo"]
    ))

    story.append(Paragraph("Paso 1 — Crear individuo en espacio real", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Se generan 7 índices enteros distintos (sin repetición) del rango [0, 9] "
        "(porque hay 10 celdas disponibles) y se convierten a flotantes:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph(
        "indices = random.sample(range(10), 7)  →  [2, 7, 1, 5, 8, 0, 4]\n"
        "individuo = [float(i) for i in indices]  →  [2.0, 7.0, 1.0, 5.0, 8.0, 0.0, 4.0]",
        estilos["codigo"]
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Paso 2 — Decodificar individuo a asignación discreta", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Para evaluar el costo, el vector real se convierte a celdas reales. "
        "El proceso ordena las máquinas por su valor flotante y asigna celdas "
        "en ese orden, tomando la celda del índice más cercano no usada:",
        estilos["cuerpo"]
    ))

    celdas_lista = ["(2,1)","(2,2)","(2,3)","(2,4)","(3,1)","(3,2)","(3,3)","(3,4)","(4,1)","(4,2)"]
    data_dec = [
        [Paragraph("<b>Máquina</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Valor flotante</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Índice redondeado</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>Celda asignada</b>", estilos["celda_tabla_bold"])],
        ["Máq.6",  "0.0", "0", "(2,1)"],
        ["Máq.3",  "1.0", "1", "(2,2)"],
        ["Máq.1",  "2.0", "2", "(2,3)"],
        ["Máq.7",  "4.0", "4", "(3,1)"],
        ["Máq.4",  "5.0", "5", "(3,2)"],
        ["Máq.2",  "7.0", "7", "(3,4)"],
        ["Máq.5",  "8.0", "8", "(4,1)"],
    ]
    t_dec = Table(data_dec, colWidths=[3*cm, 3.5*cm, 3.5*cm, 3.5*cm])
    t_dec.setStyle(TableStyle([
        ("GRID",       (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ROWHEIGHT",  (0,0), (-1,-1), 18),
        ("FONTSIZE",   (0,0), (-1,-1), 9.5),
        ("BACKGROUND", (0,0), (-1, 0), MORADO),
        ("TEXTCOLOR",  (0,0), (-1, 0), white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [white, MORADO_CLARO]),
    ]))
    story.append(t_dec)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Paso 3 — Mutación Gaussiana (cómo evolucionan los individuos)", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Los hijos se generan añadiendo <b>ruido gaussiano N(0, σ)</b> a cada valor del vector padre. "
        "Esto desplaza los índices levemente, explorando celdas vecinas:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph(
        "hijo[i] = padre[i] + random.gauss(0, sigma)\n"
        "Ejemplo con sigma=1.0:\n"
        "  padre = [2.0, 7.0, 1.0, 5.0, 8.0, 0.0, 4.0]\n"
        "  ruido  = [+0.3, -1.2, +0.8, +0.1, -0.5, +1.1, -0.2]\n"
        "  hijo   = [2.3,  5.8,  1.8,  5.1,  7.5,  1.1,  3.8]",
        estilos["codigo"]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Paso 4 — Selección (mu + lambda)", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Con <b>mu=10 padres</b> se generan <b>lambda=50 hijos</b>. Luego se evalúan "
        "todos (60 individuos) y los <b>10 mejores</b> se convierten en los nuevos padres. "
        "Esto garantiza que la calidad nunca empeora entre generaciones.",
        estilos["cuerpo"]
    ))

    story.append(Paragraph("Paso 5 — Adaptación del paso sigma (Regla del 1/5)", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Si más del 20% de los hijos son mejores que sus padres, sigma <b>aumenta</b> "
        "(exploración más amplia). Si menos del 20% mejoran, sigma <b>disminuye</b> "
        "(refinamiento fino). Esto adapta automáticamente la intensidad de la búsqueda:",
        estilos["cuerpo"]
    ))
    story.append(Paragraph(
        "tasa_exito > 0.20  →  sigma /= 0.85  (sigma crece)\n"
        "tasa_exito < 0.20  →  sigma *= 0.85  (sigma decrece)",
        estilos["codigo"]
    ))


def seccion_comparativa(story, estilos, W):
    story.append(PageBreak())
    story.append(CajaColoreada("   Comparativa de los 3 Algoritmos", estilos["titulo_seccion"],
                               AZUL_OSCURO, W))
    story.append(Spacer(1, 12))

    data = [
        [Paragraph("<b>Aspecto</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>GA</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>cGA</b>", estilos["celda_tabla_bold"]),
         Paragraph("<b>ES</b>", estilos["celda_tabla_bold"])],
        ["Representación",
         "Lista de 7 celdas (discreta)",
         "Matriz P 7×10 de probabilidades",
         "Vector de 7 flotantes (continua)"],
        ["Creación de individuo",
         "random.sample(celdas, 7)",
         "Sorteo ponderado por P[i][j]",
         "random.sample(range(10),7) → float"],
        ["Tamaño de población",
         "100 individuos explícitos",
         "2 individuos por iteración (virtual N=200)",
         "10 padres + 50 hijos = 60"],
        ["Operador principal",
         "Cruce OX + Mutación swap",
         "Actualización de probabilidades",
         "Mutación Gaussiana N(0,σ)"],
        ["Memoria",
         "Alta (guarda 100 individuos)",
         "Muy baja (solo matriz 7×10)",
         "Media (guarda 60 individuos)"],
        ["Adaptación",
         "No adapta parámetros",
         "P converge sola",
         "Regla del 1/5 adapta sigma"],
        ["Mejor costo\n(Manhattan)",
         "18.00",
         "18.00",
         "18.00"],
        ["Mejor costo\n(Euclidiana)",
         "15.66",
         "15.66",
         "15.66"],
    ]

    col_colors = [AZUL_CLARO, VERDE_CLARO, NARANJA_CLARO, MORADO_CLARO]
    t = Table(data, colWidths=[3.8*cm, 3.8*cm, 3.8*cm, 3.8*cm])
    style = [
        ("GRID",        (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ROWHEIGHT",   (0,0), (-1,-1), 30),
        ("BACKGROUND",  (0,0), (-1, 0), AZUL_OSCURO),
        ("TEXTCOLOR",   (0,0), (-1, 0), white),
        ("BACKGROUND",  (0,1), (0,-1), GRIS_CLARO),
        ("FONTNAME",    (0,1), (0,-1), "Helvetica-Bold"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
    ]
    for i in range(1, len(data)):
        bg = [white, VERDE_CLARO, NARANJA_CLARO, MORADO_CLARO]
        for j, color in enumerate(bg[1:], start=1):
            if i % 2 == 0:
                style.append(("BACKGROUND", (j, i), (j, i), color))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 14))

    story.append(Paragraph("Conclusión", estilos["titulo_sub"]))
    story.append(Paragraph(
        "Los tres algoritmos convergen al <b>mismo óptimo</b> (costo 18.00 Manhattan / "
        "15.66 Euclidiana) gracias a que el espacio de búsqueda es relativamente pequeño "
        "(10 celdas para 7 máquinas = 10!/(10-7)! = 604,800 permutaciones posibles). "
        "La diferencia está en <b>cómo exploran</b> ese espacio: GA con diversidad genética, "
        "cGA con aprendizaje probabilístico, y ES con perturbaciones adaptativas.",
        estilos["cuerpo"]
    ))


# ── CONSTRUCCIÓN DEL DOCUMENTO ────────────────────────────────────────────────

def construir_pdf():
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)

    doc = SimpleDocTemplate(
        SALIDA,
        pagesize=letter,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm, bottomMargin=2*cm,
    )

    W = doc.width
    estilos = crear_estilos()
    story = []

    # ── Portada ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1.2*cm))

    # Bloque azul de portada
    portada_data = [[
        Paragraph("Optimización de Layout — Carpintería", estilos["titulo_doc"]),
    ]]
    portada = Table(portada_data, colWidths=[W])
    portada.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_OSCURO),
        ("ROWHEIGHT",  (0,0), (-1,-1), 60),
        ("TOPPADDING", (0,0), (-1,-1), 16),
        ("BOTTOMPADDING",(0,0),(-1,-1), 16),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(portada)
    story.append(Spacer(1, 0.3*cm))

    sub_data = [[Paragraph(
        "Cómo cada algoritmo crea y evoluciona un individuo",
        estilos["subtitulo_doc"]
    )]]
    sub = Table(sub_data, colWidths=[W])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_MEDIO),
        ("ROWHEIGHT",  (0,0), (-1,-1), 30),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(sub)
    story.append(Spacer(1, 0.6*cm))

    # Índice
    idx_data = [
        [Paragraph("<b>Contenido</b>", estilos["celda_tabla_bold"])],
        [Paragraph("1. Contexto del problema y distribución de la grilla", estilos["cuerpo"])],
        [Paragraph("2. GA — Algoritmo Genético Tradicional", estilos["cuerpo"])],
        [Paragraph("3. cGA — Algoritmo Genético Compacto", estilos["cuerpo"])],
        [Paragraph("4. ES — Estrategia Evolutiva (mu + lambda)", estilos["cuerpo"])],
        [Paragraph("5. Tabla comparativa de los 3 algoritmos", estilos["cuerpo"])],
    ]
    t_idx = Table(idx_data, colWidths=[W])
    t_idx.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1, 0), AZUL_MEDIO),
        ("TEXTCOLOR",     (0,0), (-1, 0), white),
        ("BACKGROUND",    (0,1), (-1,-1), AZUL_CLARO),
        ("GRID",          (0,0), (-1,-1), 0.5, GRIS_BORDE),
        ("ROWHEIGHT",     (0,0), (-1,-1), 20),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("FONTSIZE",      (0,0), (-1,-1), 10),
    ]))
    story.append(t_idx)

    # Secciones
    seccion_intro(story, estilos, W)
    seccion_ga(story, estilos, W)
    seccion_cga(story, estilos, W)
    seccion_es(story, estilos, W)
    seccion_comparativa(story, estilos, W)

    doc.build(story)
    print(f"[OK] PDF generado: {SALIDA}")


if __name__ == "__main__":
    construir_pdf()
