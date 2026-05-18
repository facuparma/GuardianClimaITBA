import getpass
import os
import platform

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def limpiar_pantalla():
    os.system("cls" if platform.system() == "Windows" else "clear")


def imprimir_banner():
    contenido = Text(justify="center")
    contenido.append("🌤  GuardiánClima ITBA  🌤\n", style="bold cyan")
    contenido.append("Tu asistente climático con IA", style="white")
    console.print(Panel(Align.center(contenido), border_style="cyan", padding=(1, 6)))


def imprimir_separador():
    console.rule(style="cyan dim")


def input_no_vacio(prompt_text: str, password: bool = False) -> str:
    while True:
        if password:
            valor = getpass.getpass(f"  {prompt_text}: ").strip()
        else:
            valor = console.input(f"  [bold white]{prompt_text}:[/bold white] ").strip()
        if valor:
            return valor
        console.print("[yellow]  Este campo no puede estar vacío.[/yellow]")


def pausar():
    console.input("\n[dim]  Presioná Enter para continuar...[/dim]")
