import os
from typing import Optional

import requests
from rich.table import Table

from utils import console

API_BASE = "https://api.openweathermap.org/data/2.5/weather"


def _emoji_condicion(descripcion: str) -> str:
    desc = descripcion.lower()
    if any(w in desc for w in ["tormenta", "trueno", "eléctrica"]):
        return "⛈"
    if any(w in desc for w in ["lluvia", "llovizna", "chubasco", "aguacero"]):
        return "🌧"
    if any(w in desc for w in ["nieve", "granizo", "nevada"]):
        return "❄️"
    if any(w in desc for w in ["niebla", "neblina", "bruma"]):
        return "🌫"
    if any(w in desc for w in ["nublado", "cubierto"]):
        return "☁️"
    if any(w in desc for w in ["nubes", "parcial"]):
        return "⛅"
    if any(w in desc for w in ["despejado", "soleado", "claro"]):
        return "☀️"
    return "🌤"


def obtener_clima(ciudad: str) -> Optional[dict]:
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "")
    if not api_key:
        console.print("[red]  ✗ Error: OPENWEATHERMAP_API_KEY no configurada en el archivo .env[/red]")
        return None

    params = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es",
    }

    resp = None
    try:
        with console.status("[bold cyan]  Consultando clima...[/bold cyan]", spinner="dots"):
            resp = requests.get(API_BASE, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        console.print("[red]  ✗ Error de conexión. Verificá tu acceso a internet.[/red]")
        return None
    except requests.exceptions.Timeout:
        console.print("[red]  ✗ La solicitud tardó demasiado. Intentá de nuevo.[/red]")
        return None

    if resp.status_code == 401:
        console.print("[red]  ✗ API key inválida. Revisá OPENWEATHERMAP_API_KEY en tu .env[/red]")
        return None
    if resp.status_code == 404:
        console.print(f"[red]  ✗ Ciudad '[bold]{ciudad}[/bold]' no encontrada. Verificá el nombre.[/red]")
        return None
    if resp.status_code != 200:
        console.print(f"[red]  ✗ Error inesperado del servidor ({resp.status_code}).[/red]")
        return None

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


def mostrar_clima(datos: dict):
    emoji = _emoji_condicion(datos["descripcion"])

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
