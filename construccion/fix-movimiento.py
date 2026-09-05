import pathlib

p = pathlib.Path("/Users/fcabezas/Documents/GitHub/plantilla-presentaciones-demo/index.html")
t = p.read_text(encoding="utf-8")

# ── 1 · dasharray demasiado corto ──────────────────────────────────────────
# Medido en el deck: las líneas del flujo llegan a 1227 y el conector del
# ciclo a 771. Con dasharray 200 el patrón se repetía (200 visible / 200
# invisible) y los trazos largos salían cortados, con las flechas separadas
# del final del trazo. 2000 cubre el trazo más largo con holgura.
viejo_dash = """      .slide .d-flecha, .slide .d-conector, .slide .flujo-linea {
        stroke-dasharray: 200; stroke-dashoffset: 200;
      }"""
nuevo_dash = """      /* 2000 y no 200: el trazo más largo de estos diagramas mide 1227
         (la vuelta de "siguiente iteración"). Si el dasharray es menor que
         el trazo, el patrón se repite y la línea sale cortada en trozos,
         con la punta de flecha separada del final visible. */
      .slide .d-flecha, .slide .d-conector, .slide .flujo-linea {
        stroke-dasharray: 2000; stroke-dashoffset: 2000;
      }"""
assert viejo_dash in t, "no encontré la regla de dasharray"
t = t.replace(viejo_dash, nuevo_dash)

# ── 2 · animaciones que pisaban una opacidad final parcial ─────────────────
# mAparecer termina en opacity:1, así que convertía el velo del área (0.09)
# en un dorado sólido y las guías (0.7) en líneas duras.
viejo_kf = """      @keyframes mAparecer { from { opacity: 0; } to { opacity: 1; } }"""
nuevo_kf = """      @keyframes mAparecer { from { opacity: 0; } to { opacity: 1; } }
      /* variantes para elementos cuya opacidad final NO es 1: si se animaran
         con mAparecer terminarían opacos y matarían la jerarquía visual
         (el área bajo la curva es un velo, no un relleno). */
      @keyframes mVelo { from { opacity: 0; } to { opacity: 0.09; } }
      @keyframes mGuia { from { opacity: 0; } to { opacity: 0.7; } }"""
assert viejo_kf in t
t = t.replace(viejo_kf, nuevo_kf)

viejo_area = """      .slide .serie-area { opacity: 0; }
      .slide.is-active .serie-area { animation: mAparecer 900ms ease both; animation-delay: 1.1s; }"""
nuevo_area = """      .slide .serie-area { opacity: 0; }
      .slide.is-active .serie-area { animation: mVelo 900ms ease both; animation-delay: 1.1s; }"""
assert viejo_area in t
t = t.replace(viejo_area, nuevo_area)

viejo_guia = """      .slide .fig-guia { opacity: 0; }
      .slide.is-active .fig-guia { animation: mAparecer 700ms ease both; animation-delay: 0.45s; }"""
nuevo_guia = """      .slide .fig-guia { opacity: 0; }
      .slide.is-active .fig-guia { animation: mGuia 700ms ease both; animation-delay: 0.45s; }"""
assert viejo_guia in t
t = t.replace(viejo_guia, nuevo_guia)

# ── 3 · en impresión, respetar también esas opacidades parciales ───────────
# El override de print pone opacity:1 !important en todo; hay que exceptuar
# los dos elementos que son velo/guía, o el PDF sale con el área sólida.
viejo_print = """      @media print {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
      }"""
nuevo_print = """      @media print {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
        /* excepciones: estos dos son velo y guía, no elementos sólidos */
        .slide .serie-area, .slide.is-active .serie-area { opacity: 0.09 !important; }
        .slide .fig-guia, .slide.is-active .fig-guia { opacity: 0.7 !important; }
        .slide .banda-sin-dato, .slide.is-active .banda-sin-dato { opacity: 0.55 !important; }
      }"""
assert viejo_print in t
t = t.replace(viejo_print, nuevo_print)

# lo mismo para prefers-reduced-motion
viejo_rm = """      @media (prefers-reduced-motion: reduce) {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
      }"""
nuevo_rm = """      @media (prefers-reduced-motion: reduce) {
        .slide *, .slide.is-active * {
          animation: none !important;
          opacity: 1 !important;
          transform: none !important;
          stroke-dashoffset: 0 !important;
        }
        .slide .serie-area, .slide.is-active .serie-area { opacity: 0.09 !important; }
        .slide .fig-guia, .slide.is-active .fig-guia { opacity: 0.7 !important; }
        .slide .banda-sin-dato, .slide.is-active .banda-sin-dato { opacity: 0.55 !important; }
      }"""
assert viejo_rm in t
t = t.replace(viejo_rm, nuevo_rm)

p.write_text(t, encoding="utf-8")
print("corregido: dasharray 200 -> 2000, y opacidades finales de velo/guía")
