#!/usr/bin/env python3
"""Agrega 6 layouts nuevos al template, siguiendo el sistema de "signal":
misma estructura (slide-chrome / slide-body / slide-foot), mismas clases
tipográficas (.h2 .lead .caption .label .muted) y mismo sistema de animación
(data-anim + data-delay). Los colores salen todos de las variables de :root,
así que respetan la marca automáticamente.

  19. plano cartesiano de ensayos (dispersión XY con banda "sin ensayo")
  20. diagrama de flujo con decisión (rombo + ramas sí/no)
  21. línea de tiempo horizontal
  22. gráfico de líneas (dos series)
  23. mosaico de fotos
  24. foto grande con leyenda destacada
"""
import pathlib

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

# ── CSS de los layouts nuevos ───────────────────────────────────────────────
CSS = """
      /* ═══════════════════════════════════════════════════════════════════
         LAYOUTS AÑADIDOS · plano cartesiano, flujo, timeline horizontal,
         líneas, mosaico y foto con leyenda.
         Todo hereda las variables de :root, así que siguen la marca.
         ═══════════════════════════════════════════════════════════════════ */

      /* Los SVG de datos comparten estilos de eje y tipografía */
      .fig { width: 100%; height: auto; max-height: 56vh; display: block; }
      .fig-eje { stroke: var(--c-border); stroke-width: 1; }
      .fig-guia { stroke: var(--c-border); stroke-width: 0.5; stroke-dasharray: 3 4; opacity: 0.7; }
      .fig-tick { fill: var(--c-fg-3); font-family: var(--f-mono); font-size: 11px; }
      .fig-eje-label { fill: var(--c-fg-2); font-family: var(--f-mono); font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; }

      /* ── 19 · Plano cartesiano de ensayos ─────────────────────────────
         Réplica del "Plano" de la Bitácora de probetas: cada punto es una
         probeta; las que aún no tienen ensayo mecánico caen en una banda
         inferior explícita en vez de dibujarse en cero (ausencia ≠ cero). */
      .punto-propio { fill: var(--c-accent); }
      .punto-lit { fill: none; stroke: var(--c-fg-2); stroke-width: 1.5; }
      .banda-sin-dato { fill: var(--c-bg-alt); opacity: 0.55; }
      .banda-sin-dato-borde { stroke: var(--c-fg-3); stroke-width: 1; stroke-dasharray: 4 4; fill: none; }
      .banda-label { fill: var(--c-fg-3); font-family: var(--f-mono); font-size: 10.5px; letter-spacing: 0.08em; text-transform: uppercase; }
      .leyenda-fig { display: flex; gap: 2.2vw; margin-top: 1.4vh; }
      .leyenda-fig span { display: flex; align-items: center; gap: 0.55em; font-family: var(--f-mono); font-size: var(--sz-caption); color: var(--c-fg-2); }
      .leyenda-mark { width: 0.62em; height: 0.62em; border-radius: 50%; }
      .leyenda-mark.propio { background: var(--c-accent); }
      .leyenda-mark.lit { border: 1.5px solid var(--c-fg-2); }
      .leyenda-mark.sindato { border: 1px dashed var(--c-fg-3); border-radius: 2px; width: 1.1em; }

      /* ── 20 · Diagrama de flujo con decisión ──────────────────────────── */
      .flujo-caja rect, .flujo-caja polygon { fill: var(--c-bg-alt); stroke: var(--c-border); stroke-width: 1.2; }
      .flujo-caja.acento rect, .flujo-caja.acento polygon { stroke: var(--c-accent); }
      .flujo-t { fill: var(--c-fg); font-family: var(--f-body); font-size: 13px; text-anchor: middle; }
      .flujo-s { fill: var(--c-fg-2); font-family: var(--f-body); font-size: 11px; text-anchor: middle; }
      .flujo-linea { stroke: var(--c-fg-3); stroke-width: 1.2; fill: none; }
      .flujo-rama { fill: var(--c-accent); font-family: var(--f-mono); font-size: 10.5px; letter-spacing: 0.08em; }

      /* ── 21 · Línea de tiempo horizontal ──────────────────────────────── */
      .lth-eje { stroke: var(--c-border); stroke-width: 2; }
      .lth-hito circle { fill: var(--c-bg); stroke: var(--c-accent); stroke-width: 2; }
      .lth-hito.actual circle { fill: var(--c-accent); }
      .lth-anio { fill: var(--c-accent); font-family: var(--f-mono); font-size: 11px; letter-spacing: 0.1em; text-anchor: middle; }
      .lth-t { fill: var(--c-fg); font-family: var(--f-display); font-size: 15px; text-anchor: middle; }
      .lth-s { fill: var(--c-fg-2); font-family: var(--f-body); font-size: 11.5px; text-anchor: middle; }

      /* ── 22 · Gráfico de líneas ───────────────────────────────────────── */
      .serie-a { fill: none; stroke: var(--c-accent); stroke-width: 2.2; stroke-linejoin: round; stroke-linecap: round; }
      .serie-b { fill: none; stroke: var(--c-fg-2); stroke-width: 1.8; stroke-dasharray: 5 4; stroke-linejoin: round; }
      .serie-punto { fill: var(--c-accent); }
      .serie-area { fill: var(--c-accent); opacity: 0.09; }

      /* ── 23 · Mosaico de fotos ────────────────────────────────────────── */
      .mosaico {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, 1fr);
        gap: 0.9vw;
        height: 52vh;
      }
      .mos {
        background: var(--c-bg-alt);
        border: 1px solid var(--c-border);
        position: relative;
        overflow: hidden;
        display: flex; align-items: center; justify-content: center;
      }
      .mos img { width: 100%; height: 100%; object-fit: cover; display: block; }
      .mos-ph { font-family: var(--f-mono); font-size: var(--sz-label); color: var(--c-fg-3); letter-spacing: 0.1em; text-transform: uppercase; }
      .mos-cap {
        position: absolute; left: 0; right: 0; bottom: 0;
        background: linear-gradient(transparent, rgba(6, 9, 18, 0.92));
        color: var(--c-fg); font-family: var(--f-mono); font-size: var(--sz-label);
        letter-spacing: 0.06em; padding: 1.6em 0.9em 0.7em;
      }
      .mos-grande { grid-column: span 2; grid-row: span 2; }
      .mos-ancha { grid-column: span 2; }

      /* ── 24 · Foto con leyenda destacada ──────────────────────────────── */
      .foto-leyenda { display: grid; grid-template-columns: 1.55fr 1fr; gap: 2.6vw; align-items: center; height: 100%; }
      .foto-marco { background: var(--c-bg-alt); border: 1px solid var(--c-border); height: 54vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
      .foto-marco img { width: 100%; height: 100%; object-fit: cover; }
      .foto-num { font-family: var(--f-display); font-size: 3.4vw; color: var(--c-accent); line-height: 1; margin-bottom: 0.4vh; }
      .foto-dato { border-top: 1px solid var(--c-border); padding-top: 0.9vh; margin-top: 1.4vh; }
      .foto-dato dt { font-family: var(--f-mono); font-size: var(--sz-label); color: var(--c-fg-3); letter-spacing: 0.08em; text-transform: uppercase; }
      .foto-dato dd { margin: 0.2em 0 0; font-family: var(--f-body); font-size: var(--sz-body); color: var(--c-fg); }
"""

assert html.count("    </style>") == 1
html = html.replace("    </style>", CSS + "    </style>")

# ── Markup de las 6 diapositivas nuevas ─────────────────────────────────────
SLIDES = """
      <!-- ═══════ 19 · PLANO CARTESIANO DE ENSAYOS ════════════════════════ -->
      <section class="slide dark slide--scatter">
        <header class="slide-chrome">
          <span class="label muted">[Ensayos] · [Dispersión]</span>
          <span class="label muted">19</span>
        </header>
        <div class="slide-body">
          <h2 class="h2" data-anim="fade-up" data-delay="0">
            Cada punto es un ensayo, no un promedio
          </h2>
          <svg class="fig" viewBox="0 0 1000 420" role="img"
               aria-label="Plano cartesiano: carga de filler contra resistencia; las muestras sin ensayo aparecen en una banda inferior"
               data-anim="fade-up" data-delay="1">
            <!-- guías horizontales -->
            <line class="fig-guia" x1="90" y1="80" x2="960" y2="80"/>
            <line class="fig-guia" x1="90" y1="150" x2="960" y2="150"/>
            <line class="fig-guia" x1="90" y1="220" x2="960" y2="220"/>
            <line class="fig-guia" x1="90" y1="290" x2="960" y2="290"/>
            <!-- ejes -->
            <line class="fig-eje" x1="90" y1="40" x2="90" y2="330"/>
            <line class="fig-eje" x1="90" y1="330" x2="960" y2="330"/>
            <!-- ticks eje Y -->
            <text class="fig-tick" x="78" y="84" text-anchor="end">100</text>
            <text class="fig-tick" x="78" y="154" text-anchor="end">75</text>
            <text class="fig-tick" x="78" y="224" text-anchor="end">50</text>
            <text class="fig-tick" x="78" y="294" text-anchor="end">25</text>
            <!-- ticks eje X -->
            <text class="fig-tick" x="90" y="350" text-anchor="middle">0</text>
            <text class="fig-tick" x="308" y="350" text-anchor="middle">5</text>
            <text class="fig-tick" x="526" y="350" text-anchor="middle">10</text>
            <text class="fig-tick" x="744" y="350" text-anchor="middle">15</text>
            <text class="fig-tick" x="960" y="350" text-anchor="middle">20</text>
            <!-- etiquetas de eje -->
            <text class="fig-eje-label" x="525" y="378" text-anchor="middle">Carga de filler · % en peso</text>
            <text class="fig-eje-label" x="-185" y="26" transform="rotate(-90)" text-anchor="middle">Resistencia · MPa</text>
            <!-- banda "sin ensayo": la ausencia se dibuja, no se pone en cero -->
            <rect class="banda-sin-dato" x="91" y="386" width="869" height="30"/>
            <rect class="banda-sin-dato-borde" x="91" y="386" width="869" height="30"/>
            <text class="banda-label" x="102" y="405">Sin ensayo mecánico todavía</text>
            <!-- puntos con ensayo -->
            <circle class="punto-lit" cx="90"  cy="176" r="6"/>
            <circle class="punto-lit" cx="308" cy="140" r="6"/>
            <circle class="punto-lit" cx="526" cy="96"  r="6"/>
            <circle class="punto-lit" cx="744" cy="132" r="6"/>
            <circle class="punto-propio" cx="613" cy="112" r="6.5"/>
            <!-- muestras propias todavía sin ensayo, en su carga real -->
            <circle class="punto-propio" cx="395" cy="401" r="5.5"/>
            <circle class="punto-propio" cx="482" cy="401" r="5.5"/>
            <circle class="punto-propio" cx="570" cy="401" r="5.5"/>
          </svg>
          <div class="leyenda-fig" data-anim="fade-in" data-delay="3">
            <span><i class="leyenda-mark propio"></i> Medición propia</span>
            <span><i class="leyenda-mark lit"></i> Literatura citada</span>
            <span><i class="leyenda-mark sindato"></i> Sin ensayo — posición real en X, sin inventar Y</span>
          </div>
        </div>
        <div class="slide-foot">
          <span class="label muted">[Institución] · [Periodo]</span>
          <span class="label muted">19 / 24</span>
        </div>
      </section>

      <!-- ═══════ 20 · DIAGRAMA DE FLUJO CON DECISIÓN ═════════════════════ -->
      <section class="slide dark slide--flow">
        <header class="slide-chrome">
          <span class="label muted">[Protocolo]</span>
          <span class="label muted">20</span>
        </header>
        <div class="slide-body">
          <h2 class="h2" data-anim="fade-up" data-delay="0">
            El criterio de decisión, explícito
          </h2>
          <svg class="fig" viewBox="0 0 1000 400" role="img"
               aria-label="Diagrama de flujo con un punto de decisión y dos ramas"
               data-anim="fade-up" data-delay="1">
            <defs>
              <marker id="flechaFlujo" viewBox="0 0 10 10" refX="9" refY="5"
                      markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M1 1L9 5L1 9" fill="none" stroke="#5b6480" stroke-width="1.4"
                      stroke-linecap="round" stroke-linejoin="round"/>
              </marker>
            </defs>
            <!-- entrada -->
            <g class="flujo-caja">
              <rect x="30" y="150" width="190" height="66" rx="3"/>
              <text class="flujo-t" x="125" y="180">Muestra preparada</text>
              <text class="flujo-s" x="125" y="199">entrada del protocolo</text>
            </g>
            <line class="flujo-linea" x1="222" y1="183" x2="292" y2="183" marker-end="url(#flechaFlujo)"/>
            <!-- decisión -->
            <g class="flujo-caja acento">
              <polygon points="420,120 540,183 420,246 300,183"/>
              <text class="flujo-t" x="420" y="178">¿Cumple el</text>
              <text class="flujo-t" x="420" y="196">criterio?</text>
            </g>
            <!-- rama sí -->
            <line class="flujo-linea" x1="542" y1="183" x2="612" y2="183" marker-end="url(#flechaFlujo)"/>
            <text class="flujo-rama" x="556" y="172">SÍ</text>
            <g class="flujo-caja">
              <rect x="614" y="150" width="190" height="66" rx="3"/>
              <text class="flujo-t" x="709" y="180">Pasa a ensayo</text>
              <text class="flujo-s" x="709" y="199">se registra la ficha</text>
            </g>
            <!-- rama no -->
            <path class="flujo-linea" d="M420,248 L420,330 L612,330" marker-end="url(#flechaFlujo)"/>
            <text class="flujo-rama" x="432" y="282">NO</text>
            <g class="flujo-caja">
              <rect x="614" y="297" width="190" height="66" rx="3"/>
              <text class="flujo-t" x="709" y="327">Se documenta el fallo</text>
              <text class="flujo-s" x="709" y="346">con la misma rigurosidad</text>
            </g>
            <!-- retorno -->
            <path class="flujo-linea" d="M806,330 L900,330 L900,60 L125,60 L125,148" marker-end="url(#flechaFlujo)"/>
            <text class="flujo-rama" x="470" y="50">SIGUIENTE ITERACIÓN</text>
          </svg>
          <p class="caption muted" data-anim="fade-in" data-delay="3">
            Las dos ramas terminan en registro: el fallo también es dato.
          </p>
        </div>
        <div class="slide-foot">
          <span class="label muted">[Institución] · [Periodo]</span>
          <span class="label muted">20 / 24</span>
        </div>
      </section>

      <!-- ═══════ 21 · LÍNEA DE TIEMPO HORIZONTAL ═════════════════════════ -->
      <section class="slide dark slide--htimeline">
        <header class="slide-chrome">
          <span class="label muted">[Cronología]</span>
          <span class="label muted">21</span>
        </header>
        <div class="slide-body">
          <h2 class="h2" data-anim="fade-up" data-delay="0">
            Cinco hitos en una sola línea
          </h2>
          <svg class="fig" viewBox="0 0 1000 300" role="img"
               aria-label="Línea de tiempo horizontal de cinco hitos"
               data-anim="fade-up" data-delay="1">
            <line class="lth-eje" x1="70" y1="160" x2="930" y2="160"/>
            <g class="lth-hito">
              <circle cx="90" cy="160" r="7"/>
              <text class="lth-anio" x="90" y="118">[FASE 01]</text>
              <text class="lth-t" x="90" y="196">Hito uno</text>
              <text class="lth-s" x="90" y="216">qué se estableció</text>
            </g>
            <g class="lth-hito">
              <circle cx="300" cy="160" r="8"/>
              <text class="lth-anio" x="300" y="228">[FASE 02]</text>
              <text class="lth-t" x="300" y="128">Hito dos</text>
              <text class="lth-s" x="300" y="108">qué cambió</text>
            </g>
            <g class="lth-hito">
              <circle cx="510" cy="160" r="9"/>
              <text class="lth-anio" x="510" y="118">[FASE 03]</text>
              <text class="lth-t" x="510" y="196">Hito tres</text>
              <text class="lth-s" x="510" y="216">qué se midió</text>
            </g>
            <g class="lth-hito">
              <circle cx="720" cy="160" r="10"/>
              <text class="lth-anio" x="720" y="228">[FASE 04]</text>
              <text class="lth-t" x="720" y="128">Hito cuatro</text>
              <text class="lth-s" x="720" y="108">qué se decidió</text>
            </g>
            <g class="lth-hito actual">
              <circle cx="910" cy="160" r="12"/>
              <text class="lth-anio" x="910" y="112">[HOY]</text>
              <text class="lth-t" x="910" y="200">Estado actual</text>
              <text class="lth-s" x="910" y="220">dónde estamos</text>
            </g>
          </svg>
          <p class="caption muted" data-anim="fade-in" data-delay="3">
            El círculo crece en cada hito: comunica avance sin una barra de progreso aparte.
          </p>
        </div>
        <div class="slide-foot">
          <span class="label muted">[Institución] · [Periodo]</span>
          <span class="label muted">21 / 24</span>
        </div>
      </section>

      <!-- ═══════ 22 · GRÁFICO DE LÍNEAS (DOS SERIES) ═════════════════════ -->
      <section class="slide dark slide--line">
        <header class="slide-chrome">
          <span class="label muted">§ [Series]</span>
          <span class="label muted">22</span>
        </header>
        <div class="slide-body">
          <h2 class="h2" data-anim="fade-up" data-delay="0">
            Dos series, una comparación
          </h2>
          <svg class="fig" viewBox="0 0 1000 380" role="img"
               aria-label="Gráfico de líneas con dos series comparadas"
               data-anim="fade-up" data-delay="1">
            <line class="fig-guia" x1="80" y1="70" x2="960" y2="70"/>
            <line class="fig-guia" x1="80" y1="140" x2="960" y2="140"/>
            <line class="fig-guia" x1="80" y1="210" x2="960" y2="210"/>
            <line class="fig-eje" x1="80" y1="40" x2="80" y2="280"/>
            <line class="fig-eje" x1="80" y1="280" x2="960" y2="280"/>
            <text class="fig-tick" x="70" y="74" text-anchor="end">[alto]</text>
            <text class="fig-tick" x="70" y="214" text-anchor="end">[bajo]</text>
            <!-- área bajo la serie principal -->
            <path class="serie-area" d="M80,240 L256,196 L432,150 L608,120 L784,96 L960,78 L960,280 L80,280 Z"/>
            <!-- serie A (acento) -->
            <path class="serie-a" d="M80,240 L256,196 L432,150 L608,120 L784,96 L960,78"/>
            <circle class="serie-punto" cx="80" cy="240" r="4"/>
            <circle class="serie-punto" cx="256" cy="196" r="4"/>
            <circle class="serie-punto" cx="432" cy="150" r="4"/>
            <circle class="serie-punto" cx="608" cy="120" r="4"/>
            <circle class="serie-punto" cx="784" cy="96" r="4"/>
            <circle class="serie-punto" cx="960" cy="78" r="5.5"/>
            <!-- serie B (comparación) -->
            <path class="serie-b" d="M80,252 L256,238 L432,226 L608,214 L784,206 L960,198"/>
            <text class="fig-tick" x="80" y="300" text-anchor="middle">[T1]</text>
            <text class="fig-tick" x="256" y="300" text-anchor="middle">[T2]</text>
            <text class="fig-tick" x="432" y="300" text-anchor="middle">[T3]</text>
            <text class="fig-tick" x="608" y="300" text-anchor="middle">[T4]</text>
            <text class="fig-tick" x="784" y="300" text-anchor="middle">[T5]</text>
            <text class="fig-tick" x="960" y="300" text-anchor="middle">[T6]</text>
            <text class="fig-eje-label" x="520" y="330" text-anchor="middle">[Eje temporal o variable independiente]</text>
          </svg>
          <div class="leyenda-fig" data-anim="fade-in" data-delay="3">
            <span><i class="leyenda-mark propio"></i> [Serie principal]</span>
            <span><i class="leyenda-mark lit"></i> [Serie de comparación]</span>
          </div>
        </div>
        <div class="slide-foot">
          <span class="label muted">Fuente: [Fuente] · [Periodo]</span>
          <span class="label muted">22 / 24</span>
        </div>
      </section>

      <!-- ═══════ 23 · MOSAICO DE FOTOS ═══════════════════════════════════ -->
      <section class="slide dark slide--mosaic">
        <header class="slide-chrome">
          <span class="label muted">[Registro visual]</span>
          <span class="label muted">23</span>
        </header>
        <div class="slide-body">
          <h2 class="h2" data-anim="fade-up" data-delay="0">
            Tamaños distintos, no una grilla pareja
          </h2>
          <div class="mosaico" data-anim="fade-up" data-delay="1">
            <div class="mos mos-grande">
              <span class="mos-ph">imagen principal</span>
              <div class="mos-cap">[Leyenda de la imagen principal]</div>
            </div>
            <div class="mos"><span class="mos-ph">imagen 2</span><div class="mos-cap">[Detalle]</div></div>
            <div class="mos"><span class="mos-ph">imagen 3</span><div class="mos-cap">[Detalle]</div></div>
            <div class="mos mos-ancha"><span class="mos-ph">imagen 4</span><div class="mos-cap">[Comparación lado a lado]</div></div>
          </div>
        </div>
        <div class="slide-foot">
          <span class="label muted">Reemplaza cada bloque por &lt;img src="…"&gt;</span>
          <span class="label muted">23 / 24</span>
        </div>
      </section>

      <!-- ═══════ 24 · FOTO CON LEYENDA DESTACADA ═════════════════════════ -->
      <section class="slide dark slide--photo">
        <header class="slide-chrome">
          <span class="label muted">[Evidencia]</span>
          <span class="label muted">24</span>
        </header>
        <div class="slide-body">
          <div class="foto-leyenda">
            <div class="foto-marco" data-anim="scale-in" data-delay="0">
              <span class="mos-ph">fotografía a página completa</span>
            </div>
            <div>
              <p class="foto-num" data-anim="fade-up" data-delay="1">01</p>
              <h3 class="h3" data-anim="fade-up" data-delay="2">
                La leyenda importa tanto como la foto
              </h3>
              <p class="body" data-anim="fade-up" data-delay="3">
                Una imagen sin pie no es evidencia: es decoración. Di qué se está
                viendo, en qué condiciones se registró y qué hay que mirar.
              </p>
              <dl class="foto-dato" data-anim="fade-in" data-delay="4">
                <dt>Condición</dt>
                <dd>[Parámetro · valor · unidad]</dd>
              </dl>
              <dl class="foto-dato" data-anim="fade-in" data-delay="5">
                <dt>Registro</dt>
                <dd>[Fecha · equipo · aumento]</dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="slide-foot">
          <span class="label muted">[Institución] · [Periodo]</span>
          <span class="label muted">24 / 24</span>
        </div>
      </section>
"""

CIERRE = "    </div>\n    <!-- /deck -->"
assert html.count(CIERRE) == 1, "no encontré el cierre del deck"
html = html.replace(CIERRE, SLIDES + CIERRE)

f.write_text(html, encoding="utf-8")
print("agregadas 6 diapositivas ·", len(html), "bytes")
