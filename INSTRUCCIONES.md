# Instrucciones — qué va en cada diapositiva

Convención de los placeholders:

- `[entre corchetes]` → **reemplazar** por tu contenido.
- Texto sin corchetes → es la **instrucción** de qué escribir ahí (bórrala al escribir).

Las 33 diapositivas son independientes: borra las que no uses, duplica las que necesites repetir.
Cada una es un `<section class="slide …">` completo.

---

## Cómo elegir

No uses las 33. Un deck bueno usa entre 8 y 14. Elige por **lo que tienes que decir**, no por lo
que se ve bonito:

| Si necesitas… | Usa la diapositiva |
|---|---|
| Abrir con peso | `cover` (1) o **portada con foto** (25) |
| Separar dos partes del argumento | `chapter` (2) |
| Dejar una frase instalada | `statement` (3, 11) |
| Explicar algo con apoyo visual | `split` (4) |
| Mostrar 3 cifras clave | `stats` (5) |
| Citar a alguien | `quote` (6) |
| Enumerar principios | `list` (7) |
| Contrastar antes/después | `compare` (8) |
| Contar una secuencia densa | `editorial` (9) |
| Argumentar a fondo dos posturas | `dense` (10) |
| Comparar magnitudes | `chart` (13) |
| Explicar un proceso lineal | `diagram` (14) |
| Mostrar una composición | `pie` (15) |
| Ordenar por prioridad | `pyramid` (16) |
| Contar una historia en el tiempo | `vtimeline` (17) u **horizontal** (21) |
| Mostrar un ciclo que se repite | `cycle` (18) o **ciclo del deck CA** (29) |
| **Mostrar resultados de ensayos** | **plano cartesiano** (19) |
| Explicar un criterio con ramas | **diagrama de flujo** (20) |
| Comparar dos series en el tiempo | **gráfico de líneas** (22) |
| Mostrar varias fotos | **mosaico** (23) |
| Una foto que es evidencia | **foto con leyenda** (24) |
| Plantear la pregunta de investigación | **dos columnas de pregunta** (26) |
| Situar tu trabajo en la literatura | **grilla de referencias** (27) |
| Explicar la arquitectura de un sistema | **diagrama de arquitectura** (28) |
| Mostrar código como evidencia | **reglas con código** (30) |
| Guiar una demo en vivo | **guion de demo** (31) |
| Mostrar tu flujo de herramientas | **columnas de herramientas** (32) |
| Justificar lo que decidiste NO hacer | **tarjetas de criterio** (33) |
| Cerrar | `end` (12) |

---

## Qué pide cada espacio

### Portadas (1 y 25)

| Espacio | Qué va |
|---|---|
| Antetítulo | Curso o contexto · Institución · Tipo de entrega. Va en mayúsculas, es metadato. |
| Título | El nombre del proyecto. Corto. Si no cabe en dos líneas, es largo. |
| Bajada | Qué es y para qué sirve, en una o dos líneas. **No** un resumen del deck. |
| Pie | Autoría y contexto (tesis, curso, encargo). |

La 25 lleva foto de fondo: reemplaza `img/lapislazuli-portada.jpg` por la tuya. El degradado
oscurece la izquierda para que el texto se lea — si tu foto es clara, sube la opacidad del
degradado en `.slide--ca-portada::after`.

### Métricas (5)

Tres cifras, no más. Cada una lleva: el número grande, una descripción de **qué significa** (no
qué es), y debajo la fuente o el método. Si no puedes citar de dónde sale una cifra, no la pongas.

### Grilla de referencias (27)

Una tarjeta por fuente. Cada una: autor y año / el dato con su unidad / qué midió y qué implica.
La primera tiene borde verde: úsala para **tu propio dato**, así se distingue de la literatura de
un vistazo. Si tu dato todavía no existe, dilo en el detalle en vez de omitirlo.

### Plano cartesiano de ensayos (19)

Cada punto es **un ensayo**, no un promedio. Tres marcas distintas:

- Relleno dorado → medición propia.
- Círculo vacío → literatura citada.
- Banda inferior → muestras **sin ensayo todavía**: van en su posición real en el eje X, sin
  inventarles un valor en Y.

Esa banda es el punto de la diapositiva: hace visible lo que falta en vez de esconderlo. Si
pusieras esas muestras en cero, estarías afirmando que valen cero.

Para mover los puntos: edita `cx`/`cy` en el SVG. `cx` va de 90 (izquierda) a 960 (derecha),
`cy` de 40 (arriba) a 330 (abajo). La banda está en `cy≈377`.

### Reglas con código (30)

Cuatro bloques, cada uno con:

- **Nombre de la regla** — corto, memorable.
- **entra** / **sale** — qué recibe y qué produce. Esto es lo que se lee en dos segundos.
- Una frase de por qué existe: qué se rompería sin ella.
- Dos o tres líneas de código real. **No** la función completa: solo lo que prueba el punto.

### Diagrama de flujo (20)

El rombo es el punto de decisión. Las dos ramas deben terminar en algo, incluso la del "no" —
si una rama muere sin registro, el diagrama está mintiendo sobre el proceso.

### Tarjetas de criterio (33)

Lo que decidiste **no** hacer, con su razón. Cada tarjeta: qué se evaluó, por qué se descartó y
qué se ganó al descartarlo. Es la diapositiva que más credibilidad da, porque muestra criterio en
vez de entusiasmo.

### Mosaico (23) y foto con leyenda (24)

Reemplaza los bloques por `<img src="img/tu-foto.jpg" alt="…">`. La leyenda no es decorativa:
di qué se está viendo, en qué condiciones se registró y qué hay que mirar. Una imagen sin pie no
es evidencia.

---

## Utilidades

| Acción | Cómo |
|---|---|
| Avanzar / retroceder | Flechas, rueda del mouse, swipe, o los puntos de abajo |
| Ir al inicio / final | `Home` / `End` |
| **Descargar PDF** | Botón abajo a la izquierda, o tecla `P` |
| Previsualizar en 4:3 | Botón arriba a la derecha (proyectores antiguos) |
| Notas de orador | Tecla `N` |

Para agregar una nota de orador a una diapositiva, pon dentro de su `<section>`:

```html
<div class="notas"><b>0:40</b> Qué decir acá, y en cuánto tiempo.</div>
```

Solo se ve al presionar `N`. Nunca sale en el PDF.

### El PDF

"Descargar PDF" abre el diálogo de impresión del navegador; elige **Guardar como PDF**. Sale una
página por diapositiva, en 16:9 (960×540), con los fondos y colores intactos.

Si el PDF sale en blanco o sin fondos, revisa que en el diálogo de impresión esté activado
**"Gráficos de fondo"** y que los márgenes estén en **Ninguno**.

---

## Cambiar los colores

Todos los colores viven en `:root`, al principio del `<style>` de `index.html`. Cambiar esos
valores re-tematiza las 33 diapositivas:

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

## Regla de fondo

La plantilla está hecha para que **no puedas esconder lo que falta**: hay una banda para las
muestras sin ensayar, un color distinto para lo propio frente a lo citado, y una diapositiva
entera para lo que decidiste no hacer.

Si un dato no existe, dilo. Si una fuente no la leíste completa, no la cites. La plantilla no
sirve de nada si el contenido no es honesto.
