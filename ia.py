import os
from typing import Optional

from utils import console

MODELOS_PREFERIDOS = ["gemini-pro", "gemini-1.5-flash"]


def _construir_prompt(weather_data: dict) -> str:
    return (
        f"Soy un asistente de moda climática. El clima actual es: "
        f"{weather_data['temperatura']}°C, sensación térmica {weather_data['sensacion_termica']}°C, "
        f"{weather_data['descripcion']}, humedad {weather_data['humedad']}%, "
        f"viento {weather_data['viento']} km/h. "
        "Dame un consejo breve, práctico y amigable sobre cómo vestirse hoy. "
        "Máximo 5 oraciones."
    )


def obtener_consejo_ia(weather_data: dict) -> Optional[str]:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        console.print("[red]  ✗ GEMINI_API_KEY no configurada en el archivo .env[/red]")
        return None

    try:
        import google.generativeai as genai
    except ImportError:
        console.print(
            "[red]  ✗ Librería 'google-generativeai' no instalada.[/red]\n"
            "[yellow]  Ejecutá: pip install google-generativeai[/yellow]"
        )
        return None

    genai.configure(api_key=api_key)
    prompt = _construir_prompt(weather_data)
    ultimo_error = None

    for modelo in MODELOS_PREFERIDOS:
        try:
            with console.status(
                "[bold cyan]  Generando consejo con IA...[/bold cyan]",
                spinner="dots",
            ):
                model = genai.GenerativeModel(modelo)
                respuesta = model.generate_content(prompt)
            return respuesta.text.strip()
        except Exception as e:
            ultimo_error = str(e)
            continue

    console.print(f"[red]  ✗ No se pudo obtener consejo de IA: {ultimo_error}[/red]")
    return None
