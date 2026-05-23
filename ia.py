import os

from utils import console

MODELOS_PREFERIDOS = ["gemini-2.0-flash"]


# Arma el texto del prompt que se le envía a Gemini con los datos del clima
def _construir_prompt(weather_data):
    return (
        f"Soy un asistente de moda climática. El clima actual es: "
        f"{weather_data['temperatura']}°C, sensación térmica {weather_data['sensacion_termica']}°C, "
        f"{weather_data['descripcion']}, humedad {weather_data['humedad']}%, "
        f"viento {weather_data['viento']} km/h. "
        "Dame un consejo breve, práctico y amigable sobre cómo vestirse hoy. "
        "Máximo 5 oraciones."
    )


# Llama a la API de Gemini y devuelve el consejo de vestimenta generado por IA
def obtener_consejo_ia(weather_data):
    # Verificamos que la API key de Gemini esté configurada
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        console.print("[red]  ✗ GEMINI_API_KEY no configurada en el archivo .env[/red]")
        return None

    # Intentamos importar la librería de Google GenAI
    try:
        from google import genai
    except ImportError:
        console.print(
            "[red]  ✗ Librería 'google-genai' no instalada.[/red]\n"
            "[yellow]  Ejecutá: pip install google-genai[/yellow]"
        )
        return None

    client = genai.Client(api_key=api_key)
    prompt = _construir_prompt(weather_data)
    ultimo_error = None

    # Probamos cada modelo en orden hasta que uno funcione
    for modelo in MODELOS_PREFERIDOS:
        try:
            with console.status(
                "[bold cyan]  Generando consejo con IA...[/bold cyan]",
                spinner="dots",
            ):
                response = client.models.generate_content(model=modelo, contents=prompt)
            return response.text.strip()
        except Exception as e:
            ultimo_error = str(e)
            continue

    console.print(f"[red]  ✗ No se pudo obtener consejo de IA: {ultimo_error}[/red]")
    return None
