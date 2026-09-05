#!/usr/bin/env python3
"""Convierte las diapositivas 25–33 (portadas del deck de Computación Avanzada)
en plantilla de verdad: el contenido real de la tesis se reemplaza por
sugerencias de qué va en cada espacio.

Regla de escritura de los placeholders:
  [Entre corchetes] = reemplazar por contenido propio
  Texto sin corchetes = instrucción de qué escribir ahí
"""
import pathlib, re

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

T = {
    # ── 25 · portada con foto ─────────────────────────────────────────────
    "COMPUTACIÓN AVANZADA · MCD UAI · PROYECTO FINAL":
        "[CURSO O CONTEXTO] · [INSTITUCIÓN] · [TIPO DE ENTREGA]",
    "Bitácora de probetas": "[Título del proyecto]",
    "Un sistema de apoyo a la decisión experimental de la tesis, desarrollado con inteligencia artificial como herramienta de trabajo.":
        "[Una frase que diga qué es y para qué sirve. Dos líneas como máximo: en la portada nadie lee un párrafo.]",
    "Fernanda Liz Cabezas G. · Valeska López S.": "[Autora] · [Coautora]",
    "Tesis: biocompuesto de merma de lapislázuli": "[Contexto: tesis, curso, encargo]",

    # ── 26 · dos preguntas ────────────────────────────────────────────────
    "01 · Pregunta": "01 · [Sección]",
    "Dos preguntas, no una": "[Titular que contrapone dos ideas]",
    "La de la tesis": "[Primer ángulo]",
    "¿Qué combinación de carga, matriz y proceso conviene ensayar a continuación?":
        "[La primera pregunta, completa y en una sola frase.]",
    "La del curso": "[Segundo ángulo]",
    "¿Qué puede hacer hoy una administradora pública y una diseñadora con IA y un flujo de trabajo ordenado?":
        "[La segunda pregunta. Debe sonar distinta a la primera, no una variante.]",

    # ── 27 · grilla de referencias ────────────────────────────────────────
    "02 · Contexto y referencias": "02 · [Sección]",
    "La literatura da el rango. El lapislázuli no está en ella.":
        "[Titular que diga qué cubre la literatura y qué queda fuera]",
    "LAZULform Ev. 3 · propio": "[Tu fuente] · propio",
    "7–11 wt%": "[dato]",
    "Khan et al. (2023)": "[Autor et al. (año)]",
    "93,25 MPa": "[valor]",
    "Al-Mazrouei et al. (2026)": "[Autor et al. (año)]",
    "91,6 MPa": "[valor]",
    "Coppola et al. (2018)": "[Autor et al. (año)]",
    "185–215 °C": "[rango]",

    # ── 28 · diagrama de arquitectura ─────────────────────────────────────
    "03 · Propuesta y arquitectura": "03 · [Sección]",
    "Una bitácora viva: input → reglas → estado → output":
        "[Titular del sistema: entrada → reglas → estado → salida]",
    "INPUT · 3 ETAPAS": "ENTRADA",
    "Materia prima": "[Entrada 1]",
    "%wt · granulometría · reposo": "[qué se registra]",
    "Fabricación": "[Entrada 2]",
    "parámetros de impresión": "[qué se registra]",
    "Banco de pruebas": "[Entrada 3]",
    "tracción · flexión · módulos": "[qué se registra]",
    "ausencia ≠ cero": "[Regla 1]",
    "checkpoint por etapa": "[Regla 2]",
    "estimación por distancia": "[Regla 3]",
    "alerta de proximidad": "[Regla 4]",
    "probetas.json": "[archivo de estado]",
    "el repositorio git": "[dónde vive]",
    "es la base de datos": "[y por qué ahí]",
    "OUTPUT · 6 VISTAS": "SALIDA",
    "Galería": "[Vista 1]",
    "Ranking": "[Vista 3]",
    "Explorador": "[Vista 4]",
    "Nueva ficha": "[Vista 5]",

    # ── 29 · diagrama de ciclo ────────────────────────────────────────────
    "04 · Flujo de trabajo": "04 · [Sección]",
    "Un ciclo que se repite en cada probeta nueva":
        "[Titular del ciclo: qué se repite y cada cuánto]",
    "Fabricar filamento": "[Etapa 1]",
    "mezcla + extrusión": "[qué se hace]",
    "Imprimir probeta": "[Etapa 2]",
    "FDM, posición, temp.": "[qué se hace]",
    "Ensayar": "[Etapa 3]",
    "flexión, tracción": "[qué se hace]",
    "Escribir ficha": "[Etapa 4]",
    "Publicar": "[Etapa 5]",
    "commit, push, Pages": "[qué se hace]",
    "Explorar y decidir": "[Etapa 6]",
    "galería, plano, IDW": "[qué se hace]",
    "FABRICAR Y ENSAYAR": "[GRUPO A]",
    "REGISTRAR Y DECIDIR": "[GRUPO B]",

    # ── 30 · reglas con código ────────────────────────────────────────────
    "05 · Reglas principales": "05 · [Sección]",
    "Cuatro decisiones que sostienen todo el sistema":
        "[Titular: las decisiones que sostienen el sistema]",
    "1 — ausencia ≠ cero": "1 — [nombre de la regla]",
    "2 — estimación explicable": "2 — [nombre de la regla]",
    "3 — el estado es por etapa": "3 — [nombre de la regla]",
    "4 — el sistema recuerda": "4 — [nombre de la regla]",

    # ── 31 · demo ─────────────────────────────────────────────────────────
    "06 · Demo": "06 · [Sección]",
    "El artefacto, en vivo": "[Titular de la demostración en vivo]",
    "fernanda-liz.github.io/MCD-computaci-n-avanzada-3/project/":
        "[url-de-tu-artefacto.ejemplo]",
    "SI EL PROYECTO CONTINÚA": "[SIGUIENTES PASOS]",

    # ── 32 · taller de herramientas ───────────────────────────────────────
    "07 · Cómo se construyó": "07 · [Sección]",
    "El taller invisible detrás del artefacto":
        "[Titular: el trabajo que no se ve en el resultado]",
    "CAPTURAR": "[FASE 1]",
    "PENSAR": "[FASE 2]",
    "CONSTRUIR": "[FASE 3]",
    "PUBLICAR": "[FASE 4]",

    # ── 33 · criterio ─────────────────────────────────────────────────────
    "08 · Criterio": "08 · [Sección]",
    "Usar IA bien es, sobre todo, saber cuándo no usarla":
        "[Titular sobre lo que se decidió NO hacer]",
    "No inventamos datos": "[No hicimos X]",
    "No instalamos ECC": "[No hicimos Y]",
    "No dependemos del computador local": "[No hicimos Z]",
}

# textos largos (multilínea en el HTML): se buscan normalizando espacios
LARGOS = {
    "Cada probeta cuesta molienda, impresión y banco de pruebas. El espacio de parámetros es enorme y los ensayos que fallan hoy se pierden en un cuaderno.":
        "[Por qué esta pregunta importa: qué cuesta, qué se pierde o qué riesgo corre si no se responde.]",
    "El artefacto es el caso. Lo que realmente se muestra es <strong>cómo se construyó</strong>: qué herramientas, qué disciplina, qué límites.":
        "[Qué se muestra realmente con este ángulo, y qué queda fuera a propósito.]",
    "Rango viable por dos mecanismos distintos: opacidad UV en SLA, encapsulado en FDM. <strong>Sin ensayo mecánico aún.</strong>":
        "[Qué aporta esta fuente y, sobre todo, qué le falta todavía.]",
    "PLA + pizarra. Óptimo flexural a 10 wt%; a 15 wt% ya cae.":
        "[Qué midió y con qué método.]",
    "PLA + piedra volcánica, compresión. Techo de referencia.":
        "[Qué midió y por qué sirve de referencia.]",
    "La temperatura de impresión cambia el módulo: el proceso pesa tanto como la carga.":
        "[Qué variable controla y qué implica para tu caso.]",
    "Nuestras probetas aún no tienen ensayo mecánico. <strong>Ese hueco es el objeto del sistema.</strong>":
        "[La frase que conecta el vacío de la literatura con tu objeto de estudio.]",
    "13 probetas hoy · 3 checkpoints cada una · registra lo que falló igual que lo que funcionó · <strong>cero valores inventados</strong>.":
        "[Estado actual en cifras · qué garantiza el sistema · <strong>la promesa que no se rompe</strong>.]",
    "El diagrama anterior describe los datos; este describe el trabajo. Cada casilla es una tarea real, y el ciclo se repite hasta resolver la pregunta de la tesis.":
        "[Qué distingue este diagrama del anterior y hasta cuándo se repite el ciclo.]",
    "Una probeta sin medir no vale cero MPa: <strong>no está medida</strong>. Ponerla en cero sería inventar.":
        "[Por qué existe esta regla, en una frase. Lo que se rompería si no estuviera.]",
    "Pondera por <code>1/distancia²</code>. A 11 wt% estima <strong>93,2 MPa</strong> (92% de SP10).":
        "[Cómo funciona, con el número concreto que la hace verificable.]",
    "PC falla en materia prima pero <strong>pasa</strong> fabricación: un estado global perdería eso.":
        "[El caso concreto que obliga a esta regla.]",
    'Al escribir 25 wt%: <span class="rojo">"ya probaste ~26,5 — no funcionó"</span>.':
        '[Qué ve la persona usuaria: <span class="rojo">el aviso concreto, tal como aparece</span>.]',
    "Los datos de Khan et al. que aparecen en el ranking se extrajeron directamente de la Tabla 2 del PDF y quedaron <strong>citados en la ficha correspondiente</strong>, no reproducidos de memoria.":
        "[La nota al pie que respalda el rigor: de dónde salió cada dato y cómo se puede verificar.]",
    'Cada "no" está registrado en el repositorio y en la wiki de tesis, con su razón. <strong>Las decisiones también son dato.</strong>':
        "[Dónde queda registrada cada decisión y por qué eso importa.]",
    "Evaluamos inventar valores para que la demo se viera más completa. Lo descartamos y usamos 4 valores reales publicados: un dato falso sin marcar rompe la garantía de todo el resto.":
        "[Qué se evaluó, por qué se descartó y qué se ganó con descartarlo.]",
    "Teníamos disponible un framework con 68 agentes y 286 skills. No se usó: el curso evalúa claridad, no cantidad de tecnología. Habría sumado complejidad sin sumar respuesta.":
        "[Qué se evaluó, por qué se descartó y qué se ganó con descartarlo.]",
    "La idea de conectar cámara y sensores en vivo quedó como siguiente paso: el artefacto tiene que abrir en cualquier navegador, también en incógnito.":
        "[Qué se evaluó, por qué se descartó y qué se ganó con descartarlo.]",
    "<strong>Plano</strong> — la banda inferior: el hueco que la tesis debe llenar.":
        "<strong>[Paso 1]</strong> — [qué mostrar en pantalla y qué decir mientras].",
    "<strong>Explorador</strong> — mover a 11 wt%: 93,2 MPa, y de qué probetas sale.":
        "<strong>[Paso 2]</strong> — [la interacción concreta, con el valor que va a aparecer].",
    '<strong>Nueva ficha</strong> — escribir 25 wt%: <span class="rojo">"ya probaste ~26,5 — no funcionó"</span>.':
        '<strong>[Paso 3]</strong> — [cierra con lo más vistoso: <span class="rojo">el mensaje que sorprende</span>].',
    "Poblarlo con las 30–50 probetas reales de lapislázuli": "[Siguiente paso 1]",
    "Visión por computador en la extrusión: grumos y diámetro": "[Siguiente paso 2]",
    "Granulometría (25/50/100 µm) como segundo eje de cruce": "[Siguiente paso 3]",
}

# fichas de herramientas: nombre + descripción
HERR = {
    "Zotero": "[Herramienta 1]", "raw/ + script propio": "[Herramienta 2]",
    "Obsidian": "[Herramienta 3]", "CLAUDE.md + skills": "[Herramienta 4]",
    "Claude Code": "[Herramienta 5]", "MCP · navegador": "[Herramienta 6]",
    "git + GitHub Pages": "[Herramienta 7]", "Drive compartido": "[Herramienta 8]",
    "fuente de verdad para citar: metadatos + PDF enlazado": "[para qué sirve, en una frase]",
    "cada PDF → texto por página + imágenes deduplicadas, sin resumir": "[para qué sirve, en una frase]",
    "wiki de tesis: fuentes, conceptos, análisis, bitácora de hitos": "[para qué sirve, en una frase]",
    "el flujo de trabajo escrito como instrucción reutilizable": "[para qué sirve, en una frase]",
    "leer papers, extraer datos citables, escribir y probar el código": "[para qué sirve, en una frase]",
    "abrir el sitio, hacer clic, leer errores, corregir y repetir": "[para qué sirve, en una frase]",
    "el repo es la base de datos; el historial, el cuaderno de laboratorio": "[para qué sirve, en una frase]",
    "respaldo accesible para la dirección de tesis": "[para qué sirve, en una frase]",
}

# ── aplicar solo dentro del bloque de las diapositivas portadas ────────────
marca = "portado del deck de Computación Avanzada"
inicio = html.index(marca) - 400
fin = html.index("    </div>\n    <!-- /deck -->")
bloque = html[inicio:fin]

n = 0
for viejo, nuevo in {**T, **HERR}.items():
    if viejo in bloque:
        bloque = bloque.replace(viejo, nuevo)
        n += 1
for viejo, nuevo in LARGOS.items():
    patron = re.compile(r"\s+".join(re.escape(w) for w in viejo.split()))
    bloque, c = patron.subn(nuevo, bloque)
    n += c

# el código de ejemplo también es placeholder
bloque = re.sub(
    r"<pre><code>.*?</code></pre>",
    "<pre><code>// el fragmento real que implementa la regla\n// (dos o tres líneas, no la función completa)</code></pre>",
    bloque, flags=re.S,
)

html = html[:inicio] + bloque + html[fin:]
f.write_text(html, encoding="utf-8")
print("reemplazos:", n)
