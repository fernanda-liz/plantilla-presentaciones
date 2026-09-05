#!/usr/bin/env python3
"""Re-tematiza el template con la marca personal de Fernanda: la misma paleta
lapislázuli del deck de Computación Avanzada (navy profundo + dorado + azul).

Solo toca los valores de las variables en :root — el sistema visual de "signal"
(tipografía, layouts, jerarquía) queda intacto.
"""
import pathlib, re

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

# valor original de signal -> valor de la marca (tomado de
# MCD-computaci-n-avanzada-3/presentacion/styles.css)
MARCA = {
    "#1c2644": "#0a0e1c",   # --c-bg          navy profundo de la marca
    "#232f55": "#161d38",   # --c-bg-alt      panel alto
    "#f0ece3": "#f2f0ea",   # --c-bg-light    crema (se conserva, apenas más neutra)
    "#e6e0d4": "#e6e2d8",   # --c-bg-light-alt
    "#e2dcd0": "#eef0f5",   # --c-fg          texto claro de la marca
    "#8a96a8": "#a7aec4",   # --c-fg-2        texto secundario de la marca
    "#4e5a6e": "#5b6480",   # --c-fg-3        terciario, subido para que se lea sobre el navy más oscuro
    "#1a2030": "#0a0e1c",   # --c-fg-light    texto sobre crema = mismo navy de marca
    "#c8a870": "#d9b25a",   # --c-accent      DORADO de la marca
    "#2e3d5c": "#263156",   # --c-border      línea de la marca
    "#cac4b4": "#c9c4b6",   # --c-border-light
}

cambios = 0
for viejo, nuevo in MARCA.items():
    # case-insensitive: el template mezcla mayúsculas/minúsculas en los hex
    patron = re.compile(re.escape(viejo), re.IGNORECASE)
    html, n = patron.subn(nuevo, html)
    cambios += n
    print(f"{viejo} -> {nuevo}: {n}")

f.write_text(html, encoding="utf-8")
print("total reemplazos:", cambios)
