#!/usr/bin/env python3
"""Capa de movimiento por elemento.

El template base solo animaba los bloques marcados con data-anim, así que el
único movimiento visible era el cambio de diapositiva. Esto agrega entrada
propia a los elementos internos —tarjetas, barras, flechas, puntos, filas de
leyenda— sin tocar el markup: todo se aplica por selector, encadenado a
.slide.is-active, así que arranca cuando la diapositiva entra y se reinicia
cada vez que se vuelve a ella.

Criterio: sutil y corto. Nada rota, nada rebota, nada se mueve en loop salvo
un pulso muy leve en el punto de acento de dos figuras.
"""
import pathlib

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

CSS = """
      /* ═══════════════════════════════════════════════════════════════════
         MOVIMIENTO POR ELEMENTO
         Todo cuelga de .slide.is-active, así que se dispara al entrar la
         diapositiva y se reinicia al volver a ella. Se aplica por selector
         para no tener que marcar cada elemento en el HTML.
         ═══════════════════════════════════════════════════════════════════ */

      @keyframes mSubir { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
      @keyframes mAparecer { from { opacity: 0; } to { opacity: 1; } }
      @keyframes mEscala { from { opacity: 0; transform: scale(0.82); } to { opacity: 1; transform: none; } }
      @keyframes mCrecerAlto { from { transform: scaleY(0); } to { transform: scaleY(1); } }
      @keyframes mCrecerAncho { from { transform: scaleX(0); } to { transform: scaleX(1); } }
      @keyframes mDibujar { to { stroke-dashoffset: 0; } }
      /* pulso muy leve, solo para el elemento de acento de una figura */
      @keyframes mPulso { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.09); } }

      /* ── 1 · Hijos de contenedores: entran en cascada ─────────────────── */
      .slide .ref-grid > *, .slide .cols-2 > *, .slide .cols-3 > *,
      .slide .split-codigo > *, .slide .taller > *, .slide .siguientes-items > *,
      .slide .mosaico > *, .slide .guion li, .slide .pie-row,
      .slide .pyr-level, .slide .vt-item, .slide .stat-card,
      .slide .leyenda-fig > * {
        opacity: 0;
      }
      .slide.is-active .ref-grid > *, .slide.is-active .cols-2 > *,
      .slide.is-active .cols-3 > *, .slide.is-active .split-codigo > *,
      .slide.is-active .taller > *, .slide.is-active .siguientes-items > *,
      .slide.is-active .mosaico > *, .slide.is-active .guion li,
      .slide.is-active .pie-row, .slide.is-active .pyr-level,
      .slide.is-active .vt-item, .slide.is-active .stat-card,
      .slide.is-active .leyenda-fig > * {
        animation: mSubir 620ms var(--ease-enter, cubic-bezier(0.22, 0.8, 0.28, 1)) both;
      }
      /* el escalonado sale del orden del elemento, sin marcarlo en el HTML */
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(1) { animation-delay: 0.26s; }
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(2) { animation-delay: 0.36s; }
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(3) { animation-delay: 0.46s; }
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(4) { animation-delay: 0.56s; }
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(5) { animation-delay: 0.66s; }
      .slide.is-active :is(.ref-grid, .cols-2, .cols-3, .split-codigo, .taller,
        .siguientes-items, .mosaico, .guion, .pie-legend, .pyramid, .leyenda-fig) > *:nth-child(n + 6) { animation-delay: 0.76s; }

      /* las fichas de herramienta entran después de su columna */
      .slide .taller .herr { opacity: 0; }
      .slide.is-active .taller .herr { animation: mSubir 560ms var(--ease-enter) both; }
      .slide.is-active .taller .herr:nth-child(2) { animation-delay: 0.62s; }
      .slide.is-active .taller .herr:nth-child(3) { animation-delay: 0.74s; }

      /* ── 2 · Barras: crecen desde la base ─────────────────────────────── */
      .slide .bar-fill { transform-origin: bottom center; transform: scaleY(0); }
      .slide.is-active .bar-fill { animation: mCrecerAlto 760ms var(--ease-enter) both; }
      .slide.is-active .bar-col:nth-child(1) .bar-fill { animation-delay: 0.30s; }
      .slide.is-active .bar-col:nth-child(2) .bar-fill { animation-delay: 0.42s; }
      .slide.is-active .bar-col:nth-child(3) .bar-fill { animation-delay: 0.54s; }
      .slide.is-active .bar-col:nth-child(4) .bar-fill { animation-delay: 0.66s; }
      .slide.is-active .bar-col:nth-child(5) .bar-fill { animation-delay: 0.78s; }
      .slide .bar-val, .slide .bar-x-label { opacity: 0; }
      .slide.is-active .bar-val { animation: mAparecer 500ms ease both; animation-delay: 0.9s; }
      .slide.is-active .bar-x-label { animation: mAparecer 500ms ease both; animation-delay: 0.5s; }
      .slide .chart-baseline { transform-origin: left center; transform: scaleX(0); }
      .slide.is-active .chart-baseline { animation: mCrecerAncho 700ms var(--ease-enter) both; animation-delay: 0.2s; }

      /* ── 3 · Dona: el arco se dibuja ──────────────────────────────────── */
      .slide .pie-donut circle + circle, .slide .dona-valor { stroke-dasharray: 100; }
      .slide.is-active .pie-donut { animation: mEscala 700ms var(--ease-enter) both; animation-delay: 0.25s; }

      /* ── 4 · Espina de la línea de tiempo vertical ────────────────────── */
      .slide .vt-spine { transform-origin: top center; transform: scaleY(0); }
      .slide.is-active .vt-spine { animation: mCrecerAlto 900ms var(--ease-enter) both; animation-delay: 0.25s; }

      /* ── 5 · SVG: cajas, flechas y puntos ─────────────────────────────── */
      /* cajas de los diagramas portados */
      .slide .d-caja, .slide .flujo-caja, .slide .lth-hito { opacity: 0; }
      .slide.is-active .d-caja, .slide.is-active .flujo-caja,
      .slide.is-active .lth-hito { animation: mSubir 560ms var(--ease-enter) both; }
      .slide.is-active .d-caja:nth-of-type(1), .slide.is-active .flujo-caja:nth-of-type(1) { animation-delay: 0.30s; }
      .slide.is-active .d-caja:nth-of-type(2), .slide.is-active .flujo-caja:nth-of-type(2) { animation-delay: 0.42s; }
      .slide.is-active .d-caja:nth-of-type(3), .slide.is-active .flujo-caja:nth-of-type(3) { animation-delay: 0.54s; }
      .slide.is-active .d-caja:nth-of-type(4), .slide.is-active .flujo-caja:nth-of-type(4) { animation-delay: 0.66s; }
      .slide.is-active .d-caja:nth-of-type(n + 5) { animation-delay: 0.78s; }
      .slide .d-cap { opacity: 0; }
      .slide.is-active .d-cap { animation: mAparecer 520ms ease both; animation-delay: 0.22s; }

      /* flechas y conectores: se dibujan.
         dasharray 200 cubre de sobra cualquier tramo de estos diagramas, así
         que sirve como "largo normalizado" sin tener que medir cada línea. */
      .slide .d-flecha, .slide .d-conector, .slide .flujo-linea {
        stroke-dasharray: 200; stroke-dashoffset: 200;
      }
      .slide.is-active .d-flecha, .slide.is-active .d-conector,
      .slide.is-active .flujo-linea {
        animation: mDibujar 900ms ease-out both; animation-delay: 0.62s;
      }
      .slide.is-active .d-conector { animation-duration: 1200ms; animation-delay: 0.95s; }

      /* puntos del plano cartesiano: aparecen uno a uno */
      .slide .punto-propio, .slide .punto-lit { opacity: 0; transform-origin: center; transform-box: fill-box; }
      .slide.is-active .punto-propio, .slide.is-active .punto-lit {
        animation: mEscala 520ms var(--ease-enter) both;
      }
      .slide.is-active .punto-lit:nth-of-type(1) { animation-delay: 0.40s; }
      .slide.is-active .punto-lit:nth-of-type(2) { animation-delay: 0.50s; }
      .slide.is-active .punto-lit:nth-of-type(3) { animation-delay: 0.60s; }
      .slide.is-active .punto-lit:nth-of-type(4) { animation-delay: 0.70s; }
      .slide.is-active .punto-propio:nth-of-type(1) { animation-delay: 0.80s; }
      .slide.is-active .punto-propio:nth-of-type(2) { animation-delay: 0.92s; }
      .slide.is-active .punto-propio:nth-of-type(3) { animation-delay: 1.00s; }
      .slide.is-active .punto-propio:nth-of-type(4) { animation-delay: 1.08s; }
      /* la banda "sin ensayo" se despliega a lo ancho */
      .slide .banda-sin-dato, .slide .banda-sin-dato-borde { transform-origin: left center; transform: scaleX(0); }
      .slide.is-active .banda-sin-dato, .slide.is-active .banda-sin-dato-borde {
        animation: mCrecerAncho 800ms var(--ease-enter) both; animation-delay: 0.55s;
      }
      .slide .banda-label { opacity: 0; }
      .slide.is-active .banda-label { animation: mAparecer 500ms ease both; animation-delay: 1.15s; }

      /* series del gráfico de líneas: se dibujan y luego aparecen los puntos */
      .slide .serie-a, .slide .serie-b { stroke-dasharray: 1400; stroke-dashoffset: 1400; }
      .slide.is-active .serie-a { animation: mDibujar 1500ms ease-out both; animation-delay: 0.35s; }
      .slide.is-active .serie-b { animation: mDibujar 1500ms ease-out both; animation-delay: 0.55s; }
      .slide .serie-area { opacity: 0; }
      .slide.is-active .serie-area { animation: mAparecer 900ms ease both; animation-delay: 1.1s; }
      .slide .serie-punto { opacity: 0; }
      .slide.is-active .serie-punto { animation: mEscala 420ms var(--ease-enter) both; animation-delay: 1.25s; }

      /* red de nodos y ejes de las figuras propias */
      .slide .fig-eje, .slide .lth-eje { stroke-dasharray: 1200; stroke-dashoffset: 1200; }
      .slide.is-active .fig-eje, .slide.is-active .lth-eje {
        animation: mDibujar 1000ms ease-out both; animation-delay: 0.2s;
      }
      .slide .fig-guia { opacity: 0; }
      .slide.is-active .fig-guia { animation: mAparecer 700ms ease both; animation-delay: 0.45s; }

      /* ── 6 · Pulso continuo, solo donde marca la idea central ─────────── */
      .slide.is-active .lth-hito.actual circle,
      .slide.is-active .bar-fill.accent {
        transform-origin: center;
      }
      .slide.is-active .lth-hito.actual circle {
        animation: mSubir 560ms var(--ease-enter) both,
                   mPulso 3s ease-in-out 1.2s infinite;
        transform-box: fill-box;
      }

      /* ── 7 · Respeto por quien pide menos movimiento ──────────────────── */
      @media (prefers-reduced-motion: reduce) {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
      }

      /* ── 8 · En el PDF todo tiene que estar quieto y visible ──────────── */
      @media print {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
      }
"""

assert html.count("    </style>") == 1
html = html.replace("    </style>", CSS + "    </style>")
f.write_text(html, encoding="utf-8")
print("capa de movimiento agregada ·", len(html), "bytes")
