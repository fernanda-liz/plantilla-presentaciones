#!/usr/bin/env python3
"""Segunda pasada: los strings que ocupan varias líneas en el HTML.
Se buscan normalizando los espacios en blanco, así la indentación real
del archivo no importa. Conserva la indentación original al reemplazar."""
import pathlib, re

BASE = pathlib.Path(__file__).parent
f = BASE / "index.html"
html = f.read_text(encoding="utf-8")

T = {
    "A short description of the deck, its purpose, and the decision it supports.":
        "Una descripción breve del deck, su propósito y la decisión que respalda.",
    "A brief setup sentence that explains what this section covers and why it matters.":
        "Una frase breve que explica qué cubre esta sección y por qué importa.",
    "Use this sentence to introduce the list and clarify how the points should be read.":
        "Usa esta frase para introducir la lista y aclarar cómo deben leerse los puntos.",
    "Describe the current approach, the friction it creates, and why it needs to change.":
        "Describe el enfoque actual, la fricción que genera y por qué necesita cambiar.",
    "Describe the improved approach, the behavior it enables, and the outcome it supports.":
        "Describe el enfoque mejorado, lo que habilita y el resultado al que apunta.",
    "Fourth event adds context. A key pattern holds across the data.":
        "El cuarto evento agrega contexto. Un patrón clave se sostiene en todos los datos.",
    "Fifth event confirms part of the hypothesis and challenges another assumption.":
        "El quinto evento confirma parte de la hipótesis y pone en duda otro supuesto.",
    "Final event closes the sequence and clarifies the next question.":
        "El evento final cierra la secuencia y aclara la siguiente pregunta.",
    "Use this analysis line to synthesize the sequence above. Explain what changed, why it matters, and what decision should follow.":
        "Usa esta línea de análisis para sintetizar la secuencia de arriba: qué cambió, por qué importa y qué decisión debería seguir.",
    "Include one emphasized phrase when a key idea needs extra weight.":
        "Incluye una frase enfatizada cuando una idea clave necesita más peso.",
    "Add a second paragraph with supporting evidence, operational detail, or a short example that strengthens the case.":
        "Agrega un segundo párrafo con evidencia de apoyo, detalle operativo o un ejemplo corto que refuerce el caso.",
    "Close the column with the implication. Make the logic clear enough that the reader understands the recommended action.":
        "Cierra la columna con la implicancia. Que la lógica quede lo bastante clara para que se entienda la acción recomendada.",
    "Highlight the contrasting principle with an emphasized phrase.":
        "Destaca el principio contrario con una frase enfatizada.",
    "Add a second paragraph with supporting detail. This column should feel like a deliberate counterweight to the first column.":
        "Agrega un segundo párrafo con detalle de apoyo. Esta columna debería sentirse como un contrapeso deliberado de la primera.",
    "Close with the practical takeaway, linking the argument back to the decision the deck is meant to support.":
        "Cierra con la conclusión práctica, conectando el argumento con la decisión que el deck busca respaldar.",
    "Briefly describe the first step in the workflow.":
        "Describe brevemente el primer paso del flujo.",
    "Briefly describe the second step in the workflow.":
        "Describe brevemente el segundo paso del flujo.",
    "Briefly describe the third step in the workflow.":
        "Describe brevemente el tercer paso del flujo.",
    "Briefly describe the fourth step in the workflow.":
        "Describe brevemente el cuarto paso del flujo.",
    "Highest-order principle or decision criterion":
        "Principio de mayor orden o criterio de decisión",
    "Use this paragraph for the core explanation. Keep it short, specific, and easy to scan.":
        "Usa este párrafo para la explicación central: corto, específico y fácil de escanear.",
    "A concise statement that frames the main argument in one memorable sentence.":
        "Una afirmación concisa que enmarca el argumento principal en una sola frase memorable.",
    "A second statement slide can reinforce the argument with a sharper closing line.":
        "Una segunda diapositiva de afirmación puede reforzar el argumento con un cierre más filoso.",
    "Describe the decision point and the criteria used to move forward.":
        "Describe el punto de decisión y los criterios usados para avanzar.",
}

hechos, faltantes = 0, []
for en, es in T.items():
    # patrón que acepta cualquier whitespace (incl. saltos de línea) entre palabras
    patron = re.compile(r"\s+".join(re.escape(w) for w in en.split()))
    nuevo, n = patron.subn(es, html)
    if n:
        html = nuevo
        hechos += n
    else:
        faltantes.append(en[:60])

f.write_text(html, encoding="utf-8")
print(f"traducidos: {hechos}")
for x in faltantes:
    print("  NO:", x)
