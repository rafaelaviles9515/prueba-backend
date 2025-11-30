from openai import OpenAI
import os
import json
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
Eres un analista de datos experto. Recibirás información sobre un DataFrame:

Columnas: {columns}
Tipos de datos: {dtypes}
Resumen estadístico: {describe}

Debes generar entre 3 y 5 visualizaciones útiles del dataset.
Responde SOLO un JSON EN ESTE FORMATO:

[
  {{
    "title": "Título del gráfico",
    "chart_type": "bar|line|pie|scatter",
    "parameters": {{
      "x_axis": "",
      "y_axis": ""
    }},
    "insight": "Descripción corta del hallazgo."
  }}
]
"""

def ask_ai_for_suggestions(summary):
    prompt = PROMPT_TEMPLATE.format(
        columns=summary["columns"],
        dtypes=summary["dtypes"],
        describe=summary["describe"]
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    # <- CAMBIADO
    content = response.choices[0].message.content

    # Limpieza y validación de JSON
    try:
        return json.loads(content)
    except Exception:
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        else:
            raise ValueError("La IA no devolvió JSON válido: " + content)
