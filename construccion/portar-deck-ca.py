#!/usr/bin/env python3
"""Porta los layouts del deck de Computación Avanzada
(MCD-computaci-n-avanzada-3/presentacion) como diapositivas nuevas de esta
plantilla, sin tocar las 24 que ya existen.

Se extraen las <section> del deck original y se adaptan a la estructura de
"signal" (slide-chrome / slide-body / slide-foot + data-anim). Todo el CSS
portado queda acotado bajo .slide--ca para que no se filtre a las otras
diapositivas.
"""
import pathlib, re, shutil

BASE = pathlib.Path(__file__).parent
ORIGEN = pathlib.Path(
    "/Users/fcabezas/Documents/GitHub/MCD-computaci-n-avanzada-3/presentacion"
)
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")
fuente = (ORIGEN / "index.html").read_text(encoding="utf-8")

# ── copiar la foto de la portada ───────────────────────────────────────────
(BASE / "img").mkdir(exist_ok=True)
shutil.copy2(ORIGEN / "img" / "lapislazuli-portada.jpg", BASE / "img" / "lapislazuli-portada.jpg")

# ── extraer las <section class="slide"> del deck original ──────────────────
secciones = re.findall(r'<section class="slide[^"]*">(.*?)</section>', fuente, re.S)
assert len(secciones) == 9, f"esperaba 9 diapositivas, encontré {len(secciones)}"

def limpiar(cuerpo: str) -> str:
    """Saca lo que en esta plantilla lo resuelve otro mecanismo."""
    cuerpo = re.sub(r'<div class="notas">.*?</div>\s*', "", cuerpo, flags=re.S)
    cuerpo = re.sub(r'<div class="lapis-fondo"[^>]*></div>\s*', "", cuerpo)
    cuerpo = re.sub(r'<div class="formato-conmutador".*?</div>\s*', "", cuerpo, flags=re.S)
    return cuerpo.strip()

# (índice en el deck original, título de chrome, número final)
PLAN = [
    (0, "[Portada con fotografía]", "ca-portada"),
    (1, "[Dos columnas · pregunta]", "ca-pregunta"),
    (2, "[Grilla de referencias]", "ca-refs"),
    (3, "[Diagrama de arquitectura]", "ca-arq"),
    (4, "[Diagrama de ciclo]", "ca-ciclo"),
    (5, "[Reglas con código]", "ca-reglas"),
    (6, "[Guion de demo]", "ca-demo"),
    (7, "[Columnas de herramientas]", "ca-taller"),
    (8, "[Tarjetas de criterio]", "ca-criterio"),
]

nuevas = []
for orden, (idx, etiqueta, slug) in enumerate(PLAN, start=25):
    cuerpo = limpiar(secciones[idx])
    # animar los bloques principales: cada hijo de primer nivel entra escalonado
    cuerpo = re.sub(
        r'<(h1|h2|p class="num-seccion"|p class="bajada"|div class="(?:cols-2|ref-grid|split-codigo|taller|cols-3|siguientes|portada-pie)"|svg class="diagrama"|ol class="guion"|a class="url-demo"|p class="pie-slide")',
        lambda m, c=[0]: (c.__setitem__(0, c[0] + 1) or
                          f'<{m.group(1)} data-anim="fade-up" data-delay="{min(c[0]-1, 6)}"'),
        cuerpo,
    )
    portada = " slide--ca-portada" if slug == "ca-portada" else ""
    nuevas.append(f"""
      <!-- ═══════ {orden} · {etiqueta} · portado del deck de Computación Avanzada ═══ -->
      <section class="slide dark slide--ca{portada}">
        <header class="slide-chrome">
          <span class="label muted">{etiqueta}</span>
          <span class="label muted">{orden}</span>
        </header>
        <div class="slide-body">
{cuerpo}
        </div>
        <div class="slide-foot">
          <span class="label muted">[Institución] · [Periodo]</span>
          <span class="label muted">{orden} / 33</span>
        </div>
      </section>
""")

# ── CSS portado, todo acotado bajo .slide--ca ──────────────────────────────
CSS = """
      /* ═══════════════════════════════════════════════════════════════════
         LAYOUTS PORTADOS del deck de Computación Avanzada.
         Todo va acotado bajo .slide--ca para no afectar a las otras
         diapositivas. Los colores se remapean a las variables de esta
         plantilla, así que siguen la marca aunque cambies :root.
         ═══════════════════════════════════════════════════════════════════ */
      :root {
        --c-panel: #10152a;      /* panel de las tarjetas del deck original */
        --c-azul: #6478c2;       /* azul de marca: flechas, bordes, enlaces */
        --c-propio: #92b39c;     /* verde: medición propia */
        --c-lit: #c98a6b;        /* terracota: dato de literatura */
        --c-fallida: #c9695f;    /* rojo: prueba fallida / decisión de no hacer */
      }

      .slide--ca .slide-body {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 0;
      }
      .slide--ca h1 {
        margin: 0;
        font-family: var(--f-display);
        font-size: clamp(2.6rem, 6.6vw, 5.2rem);
        font-weight: 500; letter-spacing: -0.02em; line-height: 1.02;
        color: var(--c-accent); position: relative;
      }
      .slide--ca h2 {
        margin: 0 0 1.6rem;
        font-family: var(--f-display);
        font-size: clamp(1.5rem, 3.1vw, 2.6rem);
        font-weight: 500; letter-spacing: -0.015em; line-height: 1.15;
        color: var(--c-accent); max-width: 24ch;
      }
      .slide--ca p, .slide--ca li, .slide--ca span { font-family: var(--f-body); }
      .slide--ca .num-seccion {
        margin: 0 0 0.9rem; font-size: clamp(0.82rem, 1.05vw, 0.95rem);
        letter-spacing: 0.2em; text-transform: uppercase;
        color: var(--c-azul); font-weight: 600;
      }
      .slide--ca .eyebrow {
        margin: 0 0 2rem; font-family: var(--f-mono);
        font-size: clamp(0.72rem, 1.15vw, 1rem);
        letter-spacing: 0.22em; color: var(--c-accent);
      }
      .slide--ca .bajada {
        margin: 1.3rem 0 0; font-size: clamp(0.95rem, 1.75vw, 1.45rem);
        color: var(--c-fg); font-weight: 300; line-height: 1.4; max-width: 46ch;
      }
      .slide--ca .portada-pie { margin-top: auto; padding-top: 2.5rem; }
      .slide--ca .autoras { margin: 0; font-size: clamp(1rem, 1.4vw, 1.2rem); color: var(--c-fg); }
      .slide--ca .contexto { margin: 0.3rem 0 0; font-size: clamp(0.9rem, 1.15vw, 1.05rem); color: var(--c-fg-2); }
      .slide--ca .pie-slide {
        margin: 1.6rem 0 0; font-size: clamp(0.88rem, 1.1vw, 1.02rem);
        color: var(--c-fg-2); border-top: 1px solid var(--c-border); padding-top: 0.9rem;
      }
      .slide--ca .rojo { color: var(--c-fallida); }
      .slide--ca strong { color: var(--c-fg); font-weight: 600; }

      /* portada con fotografía a sangre */
      .slide--ca-portada { position: relative; }
      .slide--ca-portada::after {
        content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none;
        background-image:
          linear-gradient(90deg,
            rgba(10, 14, 28, 0.94) 0%, rgba(10, 14, 28, 0.78) 32%,
            rgba(10, 14, 28, 0.32) 58%, rgba(10, 14, 28, 0.05) 78%),
          url("img/lapislazuli-portada.jpg");
        background-size: cover, cover;
        background-position: center, center right;
      }
      .slide--ca-portada > * { position: relative; z-index: 1; }

      /* cajas y columnas */
      .slide--ca .cols-3, .slide--ca .cols-2 { display: grid; gap: 1.1rem; }
      .slide--ca .cols-3 { grid-template-columns: repeat(3, 1fr); }
      .slide--ca .cols-2 { grid-template-columns: repeat(2, 1fr); }
      .slide--ca .caja {
        background: var(--c-panel); border: 1px solid var(--c-border);
        border-left: 3px solid var(--c-azul); border-radius: 10px; padding: 1.1rem 1.2rem;
      }
      .slide--ca .caja-meta { border-left-color: var(--c-accent); }
      .slide--ca .caja-no { border-left-color: var(--c-fallida); }
      .slide--ca .caja-titulo {
        margin: 0 0 0.5rem; color: var(--c-accent);
        font-size: clamp(0.9rem, 1.15vw, 1.05rem); font-weight: 700; letter-spacing: 0.04em;
      }
      .slide--ca .caja p { font-size: clamp(0.84rem, 1.02vw, 0.96rem); color: var(--c-fg-2); line-height: 1.5; }
      .slide--ca .pregunta-grande {
        font-size: clamp(1.1rem, 1.6vw, 1.38rem); color: var(--c-fg) !important;
        line-height: 1.35; margin-bottom: 0.8rem;
      }
      .slide--ca .preguntas .caja { padding: 1.4rem 1.5rem; }

      /* grilla de referencias */
      .slide--ca .ref-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.9rem; }
      .slide--ca .ref {
        background: var(--c-panel); border: 1px solid var(--c-border);
        border-top: 3px solid var(--c-lit); border-radius: 10px; padding: 1rem 1.1rem;
      }
      .slide--ca .ref.propia { border-top-color: var(--c-propio); }
      .slide--ca .ref-fuente { margin: 0; font-size: clamp(0.82rem, 1vw, 0.92rem); color: var(--c-fg-2); }
      .slide--ca .ref-dato {
        margin: 0.35rem 0 0.5rem; font-family: var(--f-display);
        font-size: clamp(1.25rem, 2.2vw, 1.85rem); font-weight: 300;
        color: var(--c-accent); line-height: 1;
      }
      .slide--ca .ref-detalle { margin: 0; font-size: clamp(0.84rem, 1.02vw, 0.94rem); line-height: 1.45; color: var(--c-fg-2); }

      /* reglas con bloques de código */
      .slide--ca .split-codigo { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start; }
      .slide--ca .split-codigo-4 { gap: 1rem 1.4rem; }
      .slide--ca .regla-bloque {
        background: var(--c-panel); border: 1px solid var(--c-border);
        border-radius: 10px; padding: 0.9rem 1.05rem;
      }
      .slide--ca .regla-num {
        margin: 0 0 0.55rem; color: var(--c-accent); font-weight: 700;
        font-size: clamp(0.82rem, 1.05vw, 0.95rem);
      }
      .slide--ca .regla-io { margin: 0 0 0.3rem; font-size: clamp(0.72rem, 0.92vw, 0.84rem); color: var(--c-fg); }
      .slide--ca .regla-io span {
        display: inline-block; min-width: 52px; color: var(--c-azul);
        font-family: var(--f-mono); font-size: 0.8em; letter-spacing: 0.12em;
        text-transform: uppercase; font-weight: 700;
      }
      .slide--ca .regla-bloque p:not(.regla-io):not(.regla-num) {
        margin-top: 0.55rem; font-size: clamp(0.74rem, 0.94vw, 0.86rem); color: var(--c-fg-2);
      }
      .slide--ca pre {
        margin-top: 0.6rem; padding: 0.6rem 0.75rem; background: var(--c-bg);
        border: 1px solid var(--c-border); border-radius: 6px; overflow-x: auto;
      }
      .slide--ca code {
        font-family: var(--f-mono); font-size: clamp(0.66rem, 0.82vw, 0.76rem);
        line-height: 1.5; color: var(--c-fg-2);
      }

      /* guion de demo */
      .slide--ca .url-demo {
        display: inline-block; margin-bottom: 1.8rem; font-family: var(--f-mono);
        font-size: clamp(1rem, 1.7vw, 1.4rem); color: var(--c-azul);
        text-decoration: none; border-bottom: 1px solid var(--c-azul); padding-bottom: 0.2rem;
      }
      .slide--ca .guion { margin: 0; padding-left: 1.4rem; max-width: 70ch; }
      .slide--ca .guion li {
        margin-bottom: 1rem; color: var(--c-fg-2);
        font-size: clamp(1rem, 1.38vw, 1.22rem); padding-left: 0.3rem;
      }
      .slide--ca .guion li::marker { color: var(--c-accent); font-weight: 700; }
      .slide--ca .siguientes { margin-top: 2.2rem; border-top: 1px solid var(--c-border); padding-top: 1.1rem; }
      .slide--ca .siguientes-cap {
        margin: 0 0 0.8rem; font-family: var(--f-mono);
        font-size: clamp(0.72rem, 0.92vw, 0.85rem); letter-spacing: 0.18em;
        color: var(--c-accent); font-weight: 700;
      }
      .slide--ca .siguientes-items { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9rem; }
      .slide--ca .siguientes-items span {
        background: var(--c-panel); border: 1px solid var(--c-border);
        border-left: 3px solid var(--c-azul); border-radius: 8px; padding: 0.7rem 0.9rem;
        font-size: clamp(0.82rem, 1vw, 0.95rem); color: var(--c-fg-2);
      }

      /* columnas de herramientas */
      .slide--ca .taller { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
      .slide--ca .taller-cap {
        margin: 0 0 0.7rem; font-family: var(--f-mono);
        font-size: clamp(0.8rem, 1vw, 0.92rem); letter-spacing: 0.18em;
        color: var(--c-accent); font-weight: 700;
        border-bottom: 1px solid var(--c-border); padding-bottom: 0.5rem;
      }
      .slide--ca .herr {
        background: var(--c-panel); border: 1px solid var(--c-border);
        border-radius: 8px; padding: 0.75rem 0.85rem; margin-bottom: 0.7rem;
      }
      .slide--ca .herr-n {
        display: block; color: var(--c-fg); font-size: clamp(0.9rem, 1.12vw, 1.04rem);
        font-weight: 600; margin-bottom: 0.25rem;
      }
      .slide--ca .herr-d {
        display: block; color: var(--c-fg-2); font-size: clamp(0.82rem, 1vw, 0.93rem); line-height: 1.45;
      }

      /* diagramas SVG del deck original */
      .slide--ca .diagrama { width: 100%; height: auto; max-height: 44vh; }
      .slide--ca .d-caja rect { fill: var(--c-panel); stroke: var(--c-border); stroke-width: 1; }
      .slide--ca .d-reglas rect { fill: rgba(217, 178, 90, 0.07); stroke: var(--c-accent); }
      .slide--ca .d-estado rect { fill: rgba(100, 120, 194, 0.11); stroke: var(--c-azul); }
      .slide--ca .d-out rect { fill: var(--c-bg-alt); }
      .slide--ca .d-t { fill: var(--c-fg); font-family: var(--f-body); font-size: 16px; text-anchor: middle; }
      .slide--ca .d-s { fill: var(--c-fg-2); font-family: var(--f-body); font-size: 13px; text-anchor: middle; }
      .slide--ca .d-cap {
        fill: var(--c-accent); font-family: var(--f-mono); font-size: 12.5px;
        letter-spacing: 0.14em; text-anchor: middle;
      }
      .slide--ca .d-flecha { stroke: var(--c-azul); stroke-width: 1.6; }
      .slide--ca .d-conector { fill: none; stroke: var(--c-azul); stroke-width: 1.6; }
"""

assert html.count("    </style>") == 1
html = html.replace("    </style>", CSS + "    </style>")

CIERRE = "    </div>\n    <!-- /deck -->"
assert html.count(CIERRE) == 1
html = html.replace(CIERRE, "".join(nuevas) + CIERRE)

# los pies de las diapositivas anteriores ahora son sobre 33
html = re.sub(r"(\d\d) / 24<", lambda m: m.group(1) + " / 33<", html)

f.write_text(html, encoding="utf-8")
print("portadas 9 diapositivas ·", len(html), "bytes")
