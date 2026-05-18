import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.table import Table

from utils import console

HISTORIAL_CSV = "historial_global.csv"
HEADERS_HISTORIAL = [
    "NombreDeUsuario",
    "Ciudad",
    "FechaHora",
    "Temperatura_C",
    "Condicion_Clima",
    "Humedad_Porcentaje",
    "Viento_kmh",
]


def _asegurar_csv():
    path = Path(HISTORIAL_CSV)
    if not path.exists() or path.stat().st_size == 0:
        with open(HISTORIAL_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS_HISTORIAL).writeheader()


def _leer_historial() -> list[dict]:
    _asegurar_csv()
    with open(HISTORIAL_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_consulta(username: str, weather_data: dict):
    _asegurar_csv()
    fila = {
        "NombreDeUsuario": username,
        "Ciudad": f"{weather_data['ciudad']}, {weather_data['pais']}",
        "FechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temperatura_C": weather_data["temperatura"],
        "Condicion_Clima": weather_data["descripcion"],
        "Humedad_Porcentaje": weather_data["humedad"],
        "Viento_kmh": weather_data["viento"],
    }
    with open(HISTORIAL_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS_HISTORIAL).writerow(fila)


def ver_historial_personal(username: str, ciudad: str):
    filas = _leer_historial()
    ciudad_lower = ciudad.lower()
    filtradas = [
        r for r in filas
        if r["NombreDeUsuario"].lower() == username.lower()
        and ciudad_lower in r["Ciudad"].lower()
    ]

    console.print(Panel(
        f"[bold cyan]HISTORIAL: {username} — {ciudad.title()}[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    if not filtradas:
        console.print(f"[yellow]  Sin consultas registradas para '[bold]{ciudad}[/bold]'.[/yellow]")
        return

    filtradas.sort(key=lambda r: r["FechaHora"])

    table = Table(
        border_style="cyan",
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("📅 Fecha y Hora", style="dim white", no_wrap=True)
    table.add_column("🌡 Temp.", style="bold yellow", justify="right")
    table.add_column("☁️  Condición", style="white")
    table.add_column("💧 Humedad", style="cyan", justify="right")
    table.add_column("🌬 Viento", style="cyan", justify="right")

    for r in filtradas:
        table.add_row(
            r["FechaHora"],
            f"{r['Temperatura_C']} °C",
            r["Condicion_Clima"],
            f"{r['Humedad_Porcentaje']} %",
            f"{r['Viento_kmh']} km/h",
        )

    console.print(table)
    console.print(f"\n[bold green]  Total: {len(filtradas)} consulta(s)[/bold green]")


def estadisticas_globales() -> Optional[dict]:
    filas = _leer_historial()
    if not filas:
        return None

    ciudades = Counter(r["Ciudad"] for r in filas)
    ciudad_top = ciudades.most_common(1)[0][0]

    temps = []
    for r in filas:
        try:
            temps.append(float(r["Temperatura_C"]))
        except ValueError:
            pass

    return {
        "ciudad_mas_consultada": ciudad_top,
        "total_consultas": len(filas),
        "temperatura_promedio": round(sum(temps) / len(temps), 1) if temps else None,
    }


def get_ultima_consulta(username: str) -> Optional[dict]:
    filas = _leer_historial()
    del_usuario = [r for r in filas if r["NombreDeUsuario"].lower() == username.lower()]
    if not del_usuario:
        return None
    del_usuario.sort(key=lambda r: r["FechaHora"])
    return del_usuario[-1]
