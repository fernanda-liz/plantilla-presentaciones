#!/usr/bin/env python3
"""
Toma templates/signal de la librería beautiful-html-templates y le agrega las
utilidades que NO trae: exportar a PDF (botón + reglas @media print que deshacen
la tira horizontal), vista previa 4:3 y notas de orador.

Se ejecuta una sola vez para generar index.html; después se edita index.html a mano.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).parent
origen = BASE / "signal-base.html"
destino = BASE / "index.html"

html = origen.read_text(encoding="utf-8")

# ── 1. CSS de utilidades + impresión, justo antes de </style> ────────────────
CSS = """
      /* ═══════════════════════════════════════════════════════════════════
         UTILIDADES AÑADIDAS (no vienen en el template original "signal")
         Exportar a PDF · vista previa 4:3 · notas de orador
         ═══════════════════════════════════════════════════════════════════ */

      .util-btn {
        position: fixed;
        z-index: 60;
        font-family: var(--f-mono);
        font-size: 0.7vw;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        background: rgba(14, 20, 36, 0.72);
        border: 1px solid var(--c-border);
        color: var(--c-fg-2);
        padding: 0.7em 1.3em;
        border-radius: 2em;
        cursor: pointer;
        backdrop-filter: blur(8px);
        transition: color 0.2s ease, border-color 0.2s ease;
      }
      .util-btn:hover { color: var(--c-accent); border-color: var(--c-accent); }
      #btn-pdf { left: 2vw; bottom: 2.6vh; }

      .formato-conmutador { position: fixed; top: 2.6vh; right: 2vw; z-index: 60; display: flex; gap: 0.4em; }
      .formato-btn.activo { color: var(--c-accent); border-color: var(--c-accent); }

      /* Notas de orador: tecla N. Ocultas por defecto y siempre fuera del PDF. */
      .notas { display: none; }
      body.con-notas .slide.is-active .notas {
        display: block;
        position: fixed;
        left: 0; right: 0; bottom: 0;
        background: #0e1424;
        border-top: 1px solid var(--c-border);
        color: var(--c-fg-2);
        font-family: var(--f-body);
        font-size: 0.85vw;
        line-height: 1.5;
        padding: 1.4vh 2vw;
        z-index: 55;
      }
      body.con-notas .slide.is-active .notas b { color: var(--c-accent); font-weight: 500; }

      /* Vista previa 4:3: el mismo deck dentro de un iframe a 1024x768 reales
         (no un zoom aproximado — adentro, cada vw calcula contra esa resolución). */
      .simulador-4-3 {
        position: fixed; inset: 0; z-index: 70;
        background: rgba(6, 9, 18, 0.94);
        display: flex; align-items: center; justify-content: center;
      }
      .simulador-4-3.oculto { display: none; }
      .simulador-4-3 iframe {
        width: 1024px; height: 768px; border: none;
        background: var(--c-bg); transform-origin: center center;
        box-shadow: 0 2rem 6rem rgba(0, 0, 0, 0.6);
      }
      #btn-cerrar-simulador { top: 2.6vh; right: 2vw; z-index: 71; }

      /* ── Exportar a PDF ────────────────────────────────────────────────
         El deck normalmente es UNA tira horizontal de N×100vw movida con
         translateX. Para imprimir hay que deshacer eso y poner las
         diapositivas una debajo de otra, cada una en su propia página.
         El ancho y el transform los pone el JS como estilo inline, así que
         acá sí hacen falta !important para poder pisarlos.
         print-color-adjust es obligatorio: sin él Chrome descarta el fondo
         navy y el deck sale en blanco con el texto claro ilegible. */
      @media print {
        @page { size: 1280px 720px; margin: 0; }
        html, body { overflow: visible !important; height: auto !important; width: auto !important; }
        #deck {
          display: block !important;
          width: auto !important;
          height: auto !important;
          transform: none !important;
          transition: none !important;
        }
        .slide {
          width: 100% !important;
          height: 100vh !important;
          flex: none !important;
          page-break-after: always;
          break-after: page;
          overflow: hidden;
        }
        .slide:last-child { page-break-after: auto; break-after: auto; }
        /* las animaciones dejan los elementos en opacity:0 hasta que la
           diapositiva se activa — al imprimir hay que mostrarlos todos */
        [data-anim] { opacity: 1 !important; animation: none !important; transform: none !important; }
        #nav-dots, #slide-counter, .util-btn, .formato-conmutador,
        .simulador-4-3, .notas { display: none !important; }
        * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
      }
"""

assert html.count("    </style>") == 1, "no encontré el cierre de <style>"
html = html.replace("    </style>", CSS + "    </style>")

# ── 2. Markup de los controles, después del contador ────────────────────────
MARKUP = """    <div id="slide-counter"></div>

    <!-- Utilidades añadidas -->
    <div class="formato-conmutador" id="formato-conmutador" role="group" aria-label="Formato de proyección">
      <button type="button" id="btn-formato-169" class="util-btn formato-btn activo" style="position:static" aria-pressed="true">16:9</button>
      <button type="button" id="btn-formato-43" class="util-btn formato-btn" style="position:static" aria-pressed="false">4:3</button>
    </div>
    <button type="button" id="btn-pdf" class="util-btn">↓ Descargar PDF</button>
    <div id="simulador-4-3" class="simulador-4-3 oculto">
      <button type="button" id="btn-cerrar-simulador" class="util-btn">✕ volver a 16:9</button>
      <iframe id="iframe-4-3" title="Vista previa en 4:3" src="about:blank"></iframe>
    </div>
"""

assert html.count("    <div id=\"slide-counter\"></div>\n") == 1, "no encontré el contador"
html = html.replace("    <div id=\"slide-counter\"></div>\n", MARKUP)

# ── 3. JS de las utilidades, después del motor original ─────────────────────
JS = """
    <script>
      /* ══════════════════════════════════════════════════════════════════════
         UTILIDADES AÑADIDAS — PDF, vista previa 4:3, notas de orador.
         Va aparte del motor original para poder actualizar el template base
         sin perder esto (y viceversa).
         ══════════════════════════════════════════════════════════════════════ */
      (function () {
        "use strict";

        /* Descargar PDF = diálogo de impresión del navegador ("Guardar como
           PDF"). No hay conversión propia: las reglas @media print ya dejan
           una diapositiva por página. */
        var btnPdf = document.getElementById("btn-pdf");
        if (btnPdf) btnPdf.addEventListener("click", function () { window.print(); });

        /* Notas de orador */
        document.addEventListener("keydown", function (e) {
          if (e.metaKey || e.ctrlKey || e.altKey) return;
          if (e.key === "n" || e.key === "N") document.body.classList.toggle("con-notas");
          if (e.key === "p" || e.key === "P") window.print();
        });

        /* Vista previa 4:3 */
        var embebido = new URLSearchParams(location.search).get("embed") === "1";
        var conmutador = document.getElementById("formato-conmutador");
        if (embebido) {
          /* adentro del iframe sobra todo el chrome de utilidades */
          if (conmutador) conmutador.remove();
          if (btnPdf) btnPdf.remove();
          var dots = document.getElementById("nav-dots");
          if (dots) dots.style.display = "none";
          return;
        }

        var btn169 = document.getElementById("btn-formato-169");
        var btn43 = document.getElementById("btn-formato-43");
        var sim = document.getElementById("simulador-4-3");
        var iframe = document.getElementById("iframe-4-3");
        var btnCerrar = document.getElementById("btn-cerrar-simulador");

        function escalar() {
          var margen = 0.9;
          var escala = Math.min(
            (window.innerWidth * margen) / 1024,
            (window.innerHeight * margen) / 768
          );
          iframe.style.transform = "scale(" + escala + ")";
        }
        function abrir() {
          iframe.src = "index.html?embed=1";
          sim.classList.remove("oculto");
          escalar();
          btn43.classList.add("activo"); btn43.setAttribute("aria-pressed", "true");
          btn169.classList.remove("activo"); btn169.setAttribute("aria-pressed", "false");
        }
        function cerrar() {
          sim.classList.add("oculto");
          iframe.src = "about:blank";
          btn169.classList.add("activo"); btn169.setAttribute("aria-pressed", "true");
          btn43.classList.remove("activo"); btn43.setAttribute("aria-pressed", "false");
        }
        if (btn43) btn43.addEventListener("click", abrir);
        if (btn169) btn169.addEventListener("click", cerrar);
        if (btnCerrar) btnCerrar.addEventListener("click", cerrar);
        window.addEventListener("resize", function () {
          if (sim && !sim.classList.contains("oculto")) escalar();
        });
      })();
    </script>
  </body>
"""

assert html.count("  </body>") == 1, "no encontré el cierre de <body>"
html = html.replace("  </body>", JS)

destino.write_text(html, encoding="utf-8")
print("escrito:", destino, len(html), "bytes")
