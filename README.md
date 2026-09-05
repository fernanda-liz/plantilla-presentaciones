# Plantilla de presentaciones

**→ [Ver la plantilla en vivo](https://fernanda-liz.github.io/plantilla-presentaciones/)** ·
[PDF de ejemplo](./ejemplo-exportado.pdf) · [Instrucciones de uso](./INSTRUCCIONES.md)

33 diapositivas en español, navy + dorado, cada una con un **layout distinto**. No es un diseño:
es un vocabulario de formas de mostrar información, imágenes y datos. Se exporta a PDF con una
página por diapositiva.

Hecha para trabajo académico y de investigación: hay layouts para resultados de ensayos, para
situar tu trabajo en la literatura, para mostrar código como evidencia y para justificar lo que
decidiste **no** hacer.

---

## Empezar

```bash
git clone https://github.com/fernanda-liz/plantilla-presentaciones.git
cd plantilla-presentaciones
python3 servidor.py
# abrir http://localhost:4180/
```

Usá `servidor.py` y no `python3 -m http.server`: manda `Cache-Control: no-store`, así el navegador
nunca te muestra una versión vieja después de editar.

Después, leé **[INSTRUCCIONES.md](./INSTRUCCIONES.md)**: tiene la tabla de qué diapositiva usar
según lo que necesitas decir, y qué pide cada espacio.

---

## Hacerlo con Claude

### Opción 1 — el comando

En cualquier conversación de Claude Code:

```
/slides
```

La skill vive en `~/.claude/skills/slides/SKILL.md`. Sabe dónde está la plantilla, qué layout
corresponde a cada tipo de contenido, y verifica el resultado en el navegador y en PDF antes de
darlo por terminado. También se activa sola si decís "hazme una presentación de X".

### Opción 2 — el prompt

Si estás en una conversación donde la skill no está disponible (Claude.ai, otro equipo), copiá
esto y pegalo:

```
Necesito armar una presentación usando mi plantilla propia, que está en:
https://github.com/fernanda-liz/plantilla-presentaciones

Antes de escribir nada, leé el index.html y el INSTRUCCIONES.md de ese repo para
entender los 33 layouts disponibles y qué pide cada espacio.

La presentación es sobre: [TEMA]
Para: [AUDIENCIA — comisión de tesis, curso, cliente]
Dura: [MINUTOS] minutos
Contenido de partida: [pegá acá el informe/notas, o decí "desde cero"]

Cómo quiero que trabajes:
1. Elegí los layouts según lo que hay que decir, no al revés. Un deck de N minutos
   son ~N diapositivas: borrá todas las que no se usen.
2. Reemplazá los placeholders [entre corchetes]. El texto sin corchetes es la
   instrucción de qué va ahí: borralo.
3. Actualizá los números de página en cada .slide-foot.
4. No inventes ningún dato, cifra ni cita. Si algo no existe todavía, usá los
   recursos que la plantilla tiene para mostrar esa ausencia (la banda "sin ensayo"
   del plano cartesiano, el detalle de la grilla de referencias). Nunca pongas un
   valor en cero para rellenar.
5. Distinguí siempre lo propio de lo citado (verde vs. terracota).
6. Verificá en el navegador que nada se corte, y generá el PDF para confirmar que
   sale una página por diapositiva en 16:9.

No cambies los colores: son mi marca.
```

---

## Los 33 layouts

**Base (1–18)** — `cover` · `chapter` · `statement` ×2 · `split` (texto + imagen) · `stats`
(3 métricas) · `quote` · `list` · `compare` (antes/después) · `editorial` (secuencia densa) ·
`dense` (dos columnas de argumentación) · `end` · `chart` (barras) · `diagram` (proceso) ·
`pie` (dona) · `pyramid` (jerarquía) · `vtimeline` · `cycle`

**Datos y evidencia (19–24)**

- **19 · Plano cartesiano de ensayos** — cada punto es un ensayo, no un promedio. Distingue
  medición propia de literatura, y tiene una banda explícita para las muestras **sin ensayar**:
  van en su carga real sobre el eje X, sin inventarles un valor en Y.
- **20 · Diagrama de flujo con decisión** — rombo con ramas sí/no. Las dos terminan en registro:
  el fallo también es dato.
- **21 · Línea de tiempo horizontal** · **22 · Gráfico de líneas** (dos series)
- **23 · Mosaico de fotos** · **24 · Foto con leyenda destacada**

**Investigación (25–33)**

- **25 · Portada con fotografía a sangre**
- **26 · Dos columnas de pregunta** — para plantear la pregunta de investigación
- **27 · Grilla de referencias** — verde para tu dato, terracota para la literatura
- **28 · Diagrama de arquitectura** · **29 · Diagrama de ciclo**
- **30 · Reglas con código** — entra / sale + el fragmento real
- **31 · Guion de demo** · **32 · Columnas de herramientas**
- **33 · Tarjetas de criterio** — lo que decidiste no hacer, con su razón

Las diapositivas alternan fondo navy y fondo crema: ese contraste es parte del sistema.

---

## Utilidades

| Acción | Cómo |
|---|---|
| Navegar | Flechas, rueda, swipe, o los puntos de abajo |
| **Descargar PDF** | Botón abajo a la izquierda, o tecla `P` |
| Previsualizar en 4:3 | Botón arriba a la derecha |
| Notas de orador | Tecla `N` |

### El PDF, que fue lo difícil

El deck es **una sola tira horizontal** de 33×100vw movida con `translateX`. Imprimirlo sin más da
una página gigante ilegible. Las reglas `@media print` deshacen eso:

- `#deck { display:block !important; width:auto !important; transform:none !important }` — con
  `!important` porque el ancho y el transform los pone el JS como estilo **inline**.
- Todo lo animado vuelve a `opacity:1` y `transform:none`: si no, las barras se exportarían en
  `scaleY(0)` y saldrían **invisibles**.
- `print-color-adjust: exact` — sin esto Chrome descarta el fondo navy y queda texto claro sobre
  blanco.
- `@page { size: 1280px 720px }` — fuerza 16:9 en vez de tamaño carta.

Verificado con Chrome headless: 33 páginas exactas, 960×540, colores intactos.

---

## Movimiento

Cada elemento tiene entrada propia, no solo la diapositiva: las tarjetas entran en cascada, las
barras crecen desde la base, las flechas se dibujan solas, los puntos del plano aparecen uno a uno
y la banda "sin ensayo" se despliega a lo ancho. Un solo pulso continuo, muy leve, en el hito
"actual" de la línea de tiempo.

Todo se aplica por selector, así que si copiás o agregás una diapositiva hereda el movimiento sola.
Respeta `prefers-reduced-motion` y se desactiva por completo al imprimir.

Dos detalles que costaron y quedaron documentados en `construccion/fix-movimiento.py`: el
`stroke-dasharray` de las flechas tiene que ser **mayor que el trazo más largo** (1227 en este
deck) o la línea sale cortada en trozos; y las animaciones de aparición de elementos con opacidad
parcial —el velo bajo la curva, las guías punteadas— deben terminar en **su** opacidad, no en 1.

---

## Cambiar los colores

Todos viven en `:root`, al principio del `<style>`. Cambiarlos re-tematiza las 33 diapositivas:

```css
--c-bg: #0a0e1c;        /* fondo oscuro */
--c-bg-light: #f2f0ea;  /* fondo de las diapositivas claras */
--c-accent: #d9b25a;    /* dorado: títulos y énfasis */
--c-fg: #eef0f5;        /* texto sobre oscuro */
--c-azul: #6478c2;      /* flechas y bordes */
--c-propio: #92b39c;    /* verde: dato propio */
--c-lit: #c98a6b;       /* terracota: literatura */
--c-fallida: #c9695f;   /* rojo: fallo o descarte */
```

---

## Créditos y licencia

El sistema visual y los layouts 1–18 vienen del template **`signal`** de
[beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) de Zara Zhang,
usado bajo licencia MIT (ver [LICENSE-signal-template](./LICENSE-signal-template)).
`signal-base.html` es el original sin modificar y `signal-design.md` su documentación de diseño.

Sobre esa base, en este repo son propios: la paleta (lapislázuli), la traducción al español, los
layouts 19–33, la capa de movimiento por elemento, y las utilidades de exportar a PDF, vista
previa 4:3 y notas de orador — que el template original no traía.

La carpeta `construccion/` tiene los scripts que hicieron cada uno de esos pasos, por si hay que
rehacerlos sobre una versión nueva del template base.
