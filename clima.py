import os

import requests
from rich.table import Table

from utils import console

API_BASE = "https://api.openweathermap.org/data/2.5/weather"


# Devuelve el emoji que mejor representa la condición climática recibida
def _emoji_condicion(descripcion):
    desc = descripcion.lower()
    # Verificamos cada categoría buscando palabras clave en la descripción
    for w in ["tormenta", "trueno", "eléctrica"]:
        if w in desc:
            return "⛈"
    for w in ["lluvia", "llovizna", "chubasco", "aguacero"]:
        if w in desc:
            return "🌧"
    for w in ["nieve", "granizo", "nevada"]:
        if w in desc:
            return "❄️"
    for w in ["niebla", "neblina", "bruma"]:
        if w in desc:
            return "🌫"
    for w in ["nublado", "cubierto"]:
        if w in desc:
            return "☁️"
    for w in ["nubes", "parcial"]:
        if w in desc:
            return "⛅"
    for w in ["despejado", "soleado", "claro"]:
        if w in desc:
            return "☀️"
    return "🌤"


# Consulta la API de OpenWeatherMap y devuelve los datos del clima como diccionario
def obtener_clima(ciudad):
    # Leemos la API key del archivo .env
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
    if not api_key:
        console.print("[red]  ✗ Error: OPENWEATHERMAP_API_KEY no configurada en el archivo .env[/red]")
        return None

    # Parámetros de la consulta a la API
    params = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es",
    }

    resp = None
    # Hacemos la solicitud HTTP y capturamos posibles errores de red
    try:
        with console.status("[bold cyan]  Consultando clima...[/bold cyan]", spinner="dots"):
            resp = requests.get(API_BASE, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        console.print("[red]  ✗ Error de conexión. Verificá tu acceso a internet.[/red]")
        return None
    except requests.exceptions.Timeout:
        console.print("[red]  ✗ La solicitud tardó demasiado. Intentá de nuevo.[/red]")
        return None

    # Verificamos el código de respuesta HTTP para detectar errores
    if resp.status_code == 401:
        console.print("[red]  ✗ API key inválida. Revisá OPENWEATHERMAP_API_KEY en tu .env[/red]")
        return None
    if resp.status_code == 404:
        console.print(f"[red]  ✗ Ciudad '[bold]{ciudad}[/bold]' no encontrada. Verificá el nombre.[/red]")
        return None
    if resp.status_code != 200:
        console.print(f"[red]  ✗ Error inesperado del servidor ({resp.status_code}).[/red]")
        return None

    # Extraemos los datos relevantes del JSON de respuesta
    data = resp.json()
    viento_ms = data.get("wind", {}).get("speed", 0)

    return {
        "ciudad": data["name"],
        "pais": data["sys"]["country"],
        "temperatura": round(data["main"]["temp"], 1),
        "sensacion_termica": round(data["main"]["feels_like"], 1),
        "humedad": data["main"]["humidity"],
        "descripcion": data["weather"][0]["description"].capitalize(),
        "viento": round(viento_ms * 3.6, 1),
    }


# Muestra los datos del clima en una tabla visual con emojis
def mostrar_clima(datos):
    emoji = _emoji_condicion(datos["descripcion"])

    # Construimos la tabla con cada campo del clima
    table = Table(
        title=f"📍 [bold cyan]{datos['ciudad']}, {datos['pais']}[/bold cyan]",
        show_header=False,
        border_style="cyan",
        padding=(0, 2),
        title_style="bold",
    )
    table.add_column("campo", style="bold white", no_wrap=True)
    table.add_column("valor", style="white")

    table.add_row("🌡  Temperatura", f"[bold yellow]{datos['temperatura']} °C[/bold yellow]")
    table.add_row("🤔 Sensación térmica", f"{datos['sensacion_termica']} °C")
    table.add_row("💧 Humedad", f"{datos['humedad']} %")
    table.add_row("🌬  Viento", f"{datos['viento']} km/h")
    table.add_row(f"{emoji}  Condición", f"[italic]{datos['descripcion']}[/italic]")

    console.print(table)
