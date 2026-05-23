import csv
import os
import re

from rich.panel import Panel
from rich.table import Table

from utils import console, input_no_vacio

USUARIOS_CSV = "usuarios_simulados.csv"
HEADERS_USUARIOS = ["username", "password_simulada"]


# Funciones de validación para cada regla de contraseña
def _regla_longitud(p):
    return len(p) >= 8

def _regla_mayuscula(p):
    return bool(re.search(r"[A-Z]", p))

def _regla_minuscula(p):
    return bool(re.search(r"[a-z]", p))

def _regla_numero(p):
    return bool(re.search(r"\d", p))

def _regla_especial(p):
    return bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", p))


# Lista de reglas: cada una tiene una descripción y su función de validación
_REGLAS_PASSWORD = [
    ("Mínimo 8 caracteres", _regla_longitud),
    ("Al menos una mayúscula (A-Z)", _regla_mayuscula),
    ("Al menos una minúscula (a-z)", _regla_minuscula),
    ("Al menos un número (0-9)", _regla_numero),
    ("Al menos un carácter especial (!@#$%^&*...)", _regla_especial),
]


# Crea el archivo CSV de usuarios si no existe o está vacío
def _asegurar_csv():
    if not os.path.exists(USUARIOS_CSV) or os.path.getsize(USUARIOS_CSV) == 0:
        with open(USUARIOS_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS_USUARIOS).writeheader()


# Lee todos los usuarios del CSV y los devuelve como lista de diccionarios
def _leer_usuarios():
    _asegurar_csv()
    with open(USUARIOS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# Verifica si ya existe un usuario con ese nombre (sin importar mayúsculas)
def _usuario_existe(username):
    for u in _leer_usuarios():
        if u["username"].lower() == username.lower():
            return True
    return False


# Agrega un nuevo usuario al archivo CSV
def _guardar_usuario(username, password):
    with open(USUARIOS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS_USUARIOS).writerow(
            {"username": username, "password_simulada": password}
        )


# Muestra una tabla con el estado de cada regla de contraseña (✓ o ✗)
def _mostrar_reglas_password(password):
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("estado", no_wrap=True)
    table.add_column("regla", style="white")

    todas_pasan = True
    # Recorremos cada regla y verificamos si la contraseña la cumple
    for desc, validar in _REGLAS_PASSWORD:
        pasa = validar(password)
        if not pasa:
            todas_pasan = False
        icono = "[bold green]  ✓[/bold green]" if pasa else "[bold red]  ✗[/bold red]"
        table.add_row(icono, desc)

    console.print(table)
    return todas_pasan


# Registra un nuevo usuario pidiendo nombre y contraseña válida
def registrar_usuario():
    console.print(Panel(
        "[bold cyan]REGISTRO DE NUEVO USUARIO[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    # Verificamos que el nombre de usuario no esté ya en uso
    username = input_no_vacio("Nombre de usuario")
    if _usuario_existe(username):
        console.print(f"[red]  ✗ El usuario '[bold]{username}[/bold]' ya existe. Elegí otro nombre.[/red]")
        return None

    # Pedimos contraseña en un bucle hasta que cumpla todas las reglas
    while True:
        password = input_no_vacio("Contraseña", password=True)
        console.print("\n[bold white]  Requisitos de la contraseña:[/bold white]")
        todas_pasan = _mostrar_reglas_password(password)
        if todas_pasan:
            _guardar_usuario(username, password)
            console.print(f"\n[green]  ✓ Usuario '[bold]{username}[/bold]' registrado exitosamente.[/green]")
            console.print("[white]  Iniciando sesión automáticamente...[/white]")
            return username
        else:
            console.print(
                "\n[yellow]  ⚠ Tip: usá una frase como [italic]'MiGato#Salta2024'[/italic] "
                "para cumplir todos los requisitos.[/yellow]\n"
            )


# Verifica el usuario y contraseña contra el CSV y devuelve el nombre si son correctos
def iniciar_sesion():
    console.print(Panel(
        "[bold cyan]INICIAR SESIÓN[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    username = input_no_vacio("Usuario")
    password = input_no_vacio("Contraseña", password=True)

    # Buscamos el usuario en la lista y comparamos la contraseña
    usuarios = _leer_usuarios()
    for u in usuarios:
        if u["username"].lower() == username.lower() and u["password_simulada"] == password:
            console.print(f"\n[green]  ✓ Bienvenido/a, [bold]{u['username']}[/bold]![/green]")
            return u["username"]

    console.print("[red]  ✗ Usuario o contraseña incorrectos.[/red]")
    return None
