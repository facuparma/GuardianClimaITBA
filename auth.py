import csv
import re
from pathlib import Path
from typing import Optional

from rich.panel import Panel
from rich.table import Table

from utils import console, input_no_vacio

USUARIOS_CSV = "usuarios_simulados.csv"
HEADERS_USUARIOS = ["username", "password_simulada"]

_REGLAS_PASSWORD = [
    ("Mínimo 8 caracteres", lambda p: len(p) >= 8),
    ("Al menos una mayúscula (A-Z)", lambda p: bool(re.search(r"[A-Z]", p))),
    ("Al menos una minúscula (a-z)", lambda p: bool(re.search(r"[a-z]", p))),
    ("Al menos un número (0-9)", lambda p: bool(re.search(r"\d", p))),
    ("Al menos un carácter especial (!@#$%^&*...)", lambda p: bool(re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>?/\\|`~]", p))),
]


def _asegurar_csv():
    path = Path(USUARIOS_CSV)
    if not path.exists() or path.stat().st_size == 0:
        with open(USUARIOS_CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=HEADERS_USUARIOS).writeheader()


def _leer_usuarios() -> list[dict]:
    _asegurar_csv()
    with open(USUARIOS_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _usuario_existe(username: str) -> bool:
    return any(u["username"].lower() == username.lower() for u in _leer_usuarios())


def _guardar_usuario(username: str, password: str):
    with open(USUARIOS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=HEADERS_USUARIOS).writerow(
            {"username": username, "password_simulada": password}
        )


def _mostrar_reglas_password(password: str) -> bool:
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("estado", no_wrap=True)
    table.add_column("regla", style="white")

    todas_pasan = True
    for desc, validar in _REGLAS_PASSWORD:
        pasa = validar(password)
        if not pasa:
            todas_pasan = False
        icono = "[bold green]  ✓[/bold green]" if pasa else "[bold red]  ✗[/bold red]"
        table.add_row(icono, desc)

    console.print(table)
    return todas_pasan


def registrar_usuario() -> Optional[str]:
    console.print(Panel(
        "[bold cyan]REGISTRO DE NUEVO USUARIO[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    username = input_no_vacio("Nombre de usuario")
    if _usuario_existe(username):
        console.print(f"[red]  ✗ El usuario '[bold]{username}[/bold]' ya existe. Elegí otro nombre.[/red]")
        return None

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


def iniciar_sesion() -> Optional[str]:
    console.print(Panel(
        "[bold cyan]INICIAR SESIÓN[/bold cyan]",
        border_style="cyan",
        padding=(0, 2),
    ))

    username = input_no_vacio("Usuario")
    password = input_no_vacio("Contraseña", password=True)

    usuarios = _leer_usuarios()
    for u in usuarios:
        if u["username"].lower() == username.lower() and u["password_simulada"] == password:
            console.print(f"\n[green]  ✓ Bienvenido/a, [bold]{u['username']}[/bold]![/green]")
            return u["username"]

    console.print("[red]  ✗ Usuario o contraseña incorrectos.[/red]")
    return None
