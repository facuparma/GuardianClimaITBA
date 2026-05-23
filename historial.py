import csv
import os
from datetime import datetime

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


# Crea el archivo CSV del historial si no existe o está vacío
def _asegurar_csv():
    if not os.path.exists(HISTORIAL_CSV) or os.path.getsize(HISTORIAL_CSV) == 0:
        with open(HISTORIAL_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS_HISTORIAL).writeheader()


# Lee todas las filas del historial y las devuelve como lista de diccionarios
def _leer_historial():
    _asegurar_csv()
    with open(HISTORIAL_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Función auxiliar para ordenar filas por fecha y hora
def _clave_fecha(r):
    return r["FechaHora"]


# Guarda una nueva fila en el historial con los datos del clima consultado
def guardar_consulta(username, weather_data):
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


# Muestra en una tabla las consultas del usuario para una ciudad dada
def ver_historial_personal(username, ciudad):
    filas = _leer_historial()
    ciudad_lower = ciudad.lower()
    # Filtramos las filas que corresponden al usuario y ciudad indicados
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

    # Ordenamos las filas por fecha y hora antes de mostrarlas
    filtradas.sort(key=_clave_fecha)

    # Construimos la tabla con todas las consultas encontradas
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


# Calcula estadísticas globales: ciudad más consultada, total y temperatura promedio
def estadisticas_globales():
    filas = _leer_historial()
    if not filas:
        return None

    # Contamos cuántas veces aparece cada ciudad usando un diccionario
    conteo_ciudades = {}
    for r in filas:
        ciudad = r["Ciudad"]
        if ciudad in conteo_ciudades:
            conteo_ciudades[ciudad] += 1
        else:
            conteo_ciudades[ciudad] = 1

    # Buscamos la ciudad con el conteo más alto
    ciudad_top = None
    max_conteo = 0
    for ciudad, conteo in conteo_ciudades.items():
        if conteo > max_conteo:
            max_conteo = conteo
            ciudad_top = ciudad

    # Calculamos la temperatura promedio ignorando valores que no sean números
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


# Devuelve la última consulta del usuario desde el historial
def get_ultima_consulta(username):
    filas = _leer_historial()
    # Filtramos solo las filas del usuario indicado
    del_usuario = [r for r in filas if r["NombreDeUsuario"].lower() == username.lower()]
    if not del_usuario:
        return None
    # Ordenamos por fecha y devolvemos la más reciente
    del_usuario.sort(key=_clave_fecha)
    return del_usuario[-1]
