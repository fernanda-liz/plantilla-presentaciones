#!/usr/bin/env python3
"""Traduce el contenido placeholder del template al español. Idempotente:
si un string ya está traducido, simplemente no lo encuentra y sigue."""
import pathlib, sys

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

T = {
    # ── Chrome / etiquetas repetidas ──
    "[Organization] · [Period]": "[Institución] · [Periodo]",
    "[Kicker Label]": "[Antetítulo]",
    "[Slide Label]": "[Etiqueta]",
    "[Category] · [Topic]": "[Categoría] · [Tema]",
    "[Category] · [Metrics]": "[Categoría] · [Métricas]",
    "Source: [Source] · [Period]": "Fuente: [Fuente] · [Periodo]",
    "[Source] · [Date]": "[Fuente] · [Fecha]",
    "[Date]": "[Fecha]",
    "[Section]": "[Sección]",
    "[Framework]": "[Marco]",
    "[Perspective]": "[Perspectiva]",
    "[Deep Dive]": "[En profundidad]",
    "[Sequence]": "[Secuencia]",
    "[Key Readings]": "[Lecturas clave]",
    "[Analysis Label] · [Period]": "[Etiqueta de análisis] · [Periodo]",
    "[Organization]": "[Institución]",
    "[Deck Name] · [Period] ·": "[Nombre del deck] · [Periodo] ·",
    "[Review Label]": "[Etiqueta de revisión]",
    "[Issue]": "[Número]",
    "[Year]": "[Año]",
    "[Before] · [After]": "[Antes] · [Después]",
    "[Current State]": "[Estado actual]",
    "[Proposed State]": "[Estado propuesto]",
    "[Argument A]": "[Argumento A]",
    "[Argument B]": "[Argumento B]",
    "[Unit] · [Scope] · [Period]": "[Unidad] · [Alcance] · [Periodo]",
    "§ [Metrics]": "§ [Métricas]",
    "[Breakdown]": "[Desglose]",
    "[Hierarchy]": "[Jerarquía]",
    "Process": "Proceso",
    "PROCESS": "PROCESO",
    "[Method or source]": "[Método o fuente]",
    "[Benchmark]": "[Referencia]",
    "[Source Name]": "[Nombre de la fuente]",
    "[Source Role] · [Context]": "[Rol de la fuente] · [Contexto]",
    "[Author Name] · [Role]": "[Autora] · [Rol]",
    "[Version] · [Status] · [Period]": "[Versión] · [Estado] · [Periodo]",
    "[Period] · [Audience] · [Deck Type]": "[Periodo] · [Audiencia] · [Tipo de deck]",
    "[Author Name] · [email@example.com] · [website.example]":
        "[Autora] · [correo@ejemplo.com] · [sitio.ejemplo]",
    "Sources: [Source A] · [Source B] · [Source C] · [Source D]":
        "Fuentes: [Fuente A] · [Fuente B] · [Fuente C] · [Fuente D]",
    "Total: [N] · As of [Period]": "Total: [N] · Al [Periodo]",

    # ── Portada ──
    "[Presentation]": "[Título de la]",
    "Title": "Presentación",
    "A short description of the deck, its purpose, and the decision it\n              supports.":
        "Una descripción breve del deck, su propósito y la decisión que\n              respalda.",

    # ── Capítulo ──
    "Section headline with one emphasized idea":
        "Título de sección con una idea enfatizada",
    "A brief setup sentence that explains what this section covers and why\n            it matters.":
        "Una frase breve que explica qué cubre esta sección y por qué\n            importa.",

    # ── Statement ──
    "A concise statement that frames the main argument in one\n              memorable sentence.":
        "Una afirmación concisa que enmarca el argumento principal en una\n              sola frase memorable.",
    "A second statement slide can reinforce the argument with a\n              sharper closing line.":
        "Una segunda diapositiva de afirmación puede reforzar el argumento con\n              un cierre más filoso.",

    # ── Split ──
    "Main headline for a split-layout slide":
        "Título principal para una diapositiva partida",
    "Use this paragraph for the core explanation. Keep it short,\n              specific, and easy to scan.":
        "Usa este párrafo para la explicación central. Que sea corto,\n              específico y fácil de escanear.",
    "First supporting point with concise context": "Primer punto de apoyo, con contexto conciso",
    "Second supporting point with concise context": "Segundo punto de apoyo, con contexto conciso",
    "Third supporting point with concise context": "Tercer punto de apoyo, con contexto conciso",
    "Image Placeholder": "Espacio para imagen",
    "[Caption for image]": "[Pie de imagen]",

    # ── Stats ──
    "Three metrics that summarize the current state":
        "Tres métricas que resumen el estado actual",
    "Short description of the first metric and its meaning":
        "Descripción breve de la primera métrica y su significado",
    "Short description of the second metric and its meaning":
        "Descripción breve de la segunda métrica y su significado",
    "Short description of the third metric and its meaning":
        "Descripción breve de la tercera métrica y su significado",

    # ── Quote ──
    "A short pull quote or highlighted observation can sit here.":
        "Acá puede ir una cita destacada o una observación subrayada.",

    # ── Lista ──
    "Five principles that shape the recommended approach":
        "Cinco principios que dan forma al enfoque recomendado",
    "Use this sentence to introduce the list and clarify how the\n            points should be read.":
        "Usa esta frase para introducir la lista y aclarar cómo deben\n            leerse los puntos.",
    "First principle written as a complete sentence": "Primer principio, escrito como frase completa",
    "Second principle written as a complete sentence": "Segundo principio, escrito como frase completa",
    "Third principle written as a complete sentence": "Tercer principio, escrito como frase completa",
    "Fourth principle written as a complete sentence": "Cuarto principio, escrito como frase completa",
    "Fifth principle written as a complete sentence": "Quinto principio, escrito como frase completa",

    # ── Compare ──
    "Headline describing the current state": "Título que describe el estado actual",
    "Headline describing the proposed approach": "Título que describe el enfoque propuesto",
    "Describe the current approach, the friction it creates, and why it\n                needs to change.":
        "Describe el enfoque actual, la fricción que genera y por qué\n                necesita cambiar.",
    "Describe the improved approach, the behavior it enables, and the\n                outcome it supports.":
        "Describe el enfoque mejorado, lo que habilita y el resultado\n                al que apunta.",
    "Current limitation or source of friction": "Limitación actual o fuente de fricción",
    "Expected improvement or capability": "Mejora esperada o capacidad nueva",

    # ── Editorial ──
    "Editorial headline with one accented word for emphasis.":
        "Título editorial con una palabra acentuada para dar énfasis.",
    "First event or observation appears.": "Aparece el primer evento u observación.",
    "Second event or observation appears.": "Aparece el segundo evento u observación.",
    "Third event or observation appears.": "Aparece el tercer evento u observación.",
    "Fourth event adds context. A key pattern holds\n                    across the data.":
        "El cuarto evento agrega contexto. Un patrón clave se sostiene\n                    en todos los datos.",
    "Fifth event confirms part of the hypothesis and challenges\n                    another assumption.":
        "El quinto evento confirma parte de la hipótesis y pone en duda\n                    otro supuesto.",
    "Final event closes the sequence and clarifies the\n                    next question.":
        "El evento final cierra la secuencia y aclara la\n                    siguiente pregunta.",
    "Short implication.": "Implicancia breve.",
    "Metric label · [Segment] · [Period]": "Etiqueta de métrica · [Segmento] · [Periodo]",
    "Metric label vs. comparison period": "Etiqueta de métrica vs. periodo de comparación",
    "Metric label · [Segment]": "Etiqueta de métrica · [Segmento]",
    "Net change across selected group": "Cambio neto en el grupo seleccionado",
    "Use this analysis line to synthesize the sequence above. Explain what\n              changed, why it matters, and what decision should follow.":
        "Usa esta línea de análisis para sintetizar la secuencia de arriba. Explica qué\n              cambió, por qué importa y qué decisión debería seguir.",

    # ── Dense ──
    "Long-form headline that frames the central tradeoff":
        "Título extenso que enmarca el trade-off central",
    "Use this paragraph to explain the first side of the argument.":
        "Usa este párrafo para explicar el primer lado del argumento.",
    "Include one emphasized phrase when a key idea needs\n                extra weight.":
        "Incluye una frase enfatizada cuando una idea clave necesita\n                más peso.",
    "Add a second paragraph with supporting evidence, operational\n                detail, or a short example that strengthens the case.":
        "Agrega un segundo párrafo con evidencia de apoyo, detalle\n                operativo o un ejemplo corto que refuerce el caso.",
    "Close the column with the implication. Make the logic clear\n                enough that the reader understands the recommended action.":
        "Cierra la columna con la implicancia. Que la lógica quede lo\n                bastante clara para que se entienda la acción recomendada.",
    "Use this paragraph to explain the second side of the argument.":
        "Usa este párrafo para explicar el segundo lado del argumento.",
    "Highlight the contrasting principle with an\n                emphasized phrase.":
        "Destaca el principio contrario con una\n                frase enfatizada.",
    "Add a second paragraph with supporting detail. This column should\n                feel like a deliberate counterweight to the first column.":
        "Agrega un segundo párrafo con detalle de apoyo. Esta columna debería\n                sentirse como un contrapeso deliberado de la primera.",
    "Close with the practical takeaway, linking the argument back to\n                the decision the deck is meant to support.":
        "Cierra con la conclusión práctica, conectando el argumento con\n                la decisión que el deck busca respaldar.",

    # ── Cierre ──
    "Closing headline with one emphasized phrase.":
        "Título de cierre con una frase enfatizada.",

    # ── Chart / diagrama / dona / pirámide ──
    "Chart headline with emphasis": "Título del gráfico, con énfasis",
    "Four-step process with emphasis": "Proceso de cuatro pasos, con énfasis",
    "Step One": "Paso uno",
    "Step Two": "Paso dos",
    "Step Three": "Paso tres",
    "Step Four": "Paso cuatro",
    "Briefly describe the first step\n                in the workflow.": "Describe brevemente el primer paso\n                del flujo.",
    "Briefly describe the second\n                step in the workflow.": "Describe brevemente el segundo\n                paso del flujo.",
    "Briefly describe the third step\n                in the workflow.": "Describe brevemente el tercer paso\n                del flujo.",
    "Briefly describe the fourth\n                step in the workflow.": "Describe brevemente el cuarto\n                paso del flujo.",
    "Breakdown by category": "Desglose por categoría",
    "Category A": "Categoría A",
    "Category B": "Categoría B",
    "Category C": "Categoría C",
    "Category D": "Categoría D",
    "The priority hierarchy": "La jerarquía de prioridades",
    "Level One": "Nivel uno",
    "Level Two": "Nivel dos",
    "Level Three": "Nivel tres",
    "Level Four": "Nivel cuatro",
    "Level Five": "Nivel cinco",
    "Highest-order principle or\n                  decision criterion": "Principio de mayor orden o\n                  criterio de decisión",
    "Second-order principle or decision criterion": "Principio de segundo orden o criterio de decisión",
    "Third-order principle or decision criterion": "Principio de tercer orden o criterio de decisión",
    "Supporting layer or operating standard": "Capa de apoyo o estándar operativo",
    "Foundation layer or ongoing practice": "Capa base o práctica permanente",
    "Describe the decision point and the criteria used to move\n                forward.":
        "Describe el punto de decisión y los criterios usados para\n                avanzar.",
}

hechos, faltantes = 0, []
for en, es in T.items():
    if en in html:
        html = html.replace(en, es)
        hechos += 1
    else:
        faltantes.append(en[:60])

f.write_text(html, encoding="utf-8")
print(f"traducidos: {hechos}/{len(T)}")
if faltantes:
    print("no encontrados (revisar a mano):")
    for x in faltantes:
        print("  -", x)
