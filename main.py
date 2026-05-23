from dotenv import load_dotenv
load_dotenv()

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from auth import registrar_usuario, iniciar_sesion
from clima import obtener_clima, mostrar_clima
from historial import guardar_consulta, ver_historial_personal, estadisticas_globales
from ia import obtener_consejo_ia
from utils import console, limpiar_pantalla, imprimir_banner, input_no_vacio, pausar


# Muestra el menú de acceso (login o registro) y devuelve el nombre del usuario
def menu_acceso():
    while True:
        limpiar_pantalla()
        imprimir_banner()

        menu = (
            "  [bold]1.[/bold] Iniciar sesión\n"
            "  [bold]2.[/bold] Registrarse\n"
            "  [bold]3.[/bold] Salir"
        )
        console.print(Panel(menu, title="[bold cyan]MENÚ PRINCIPAL[/bold cyan]", border_style="cyan", padding=(1, 2)))

        opcion = console.input("  [bold cyan]Opción:[/bold cyan] ").strip()

        # Opción 1: iniciar sesión con usuario existente
        if opcion == "1":
            limpiar_pantalla()
            imprimir_banner()
            usuario = iniciar_sesion()
            if usuario:
                pausar()
                return usuario
            else:
                pausar()
        # Opción 2: crear una cuenta nueva
        elif opcion == "2":
            limpiar_pantalla()
            imprimir_banner()
            usuario = registrar_usuario()
            if usuario:
                pausar()
                return usuario
            else:
                pausar()
        # Opción 3: salir del programa
        elif opcion == "3":
            console.print(Panel(
                "[bold cyan]  ¡Hasta pronto! 🌤[/bold cyan]",
                border_style="cyan",
                padding=(0, 2),
            ))
            return None
        else:
            console.print("[yellow]  Opción inválida. Elegí 1, 2 o 3.[/yellow]")
            pausar()


# Pide una ciudad, obtiene el clima y guarda la consulta en el historial
def flujo_consultar_clima(usuario):
    limpiar_pantalla()
    imprimir_banner()
    console.print(Panel("[bold cyan]CONSULTAR CLIMA[/bold cyan]", border_style="cyan", padding=(0, 2)))

    ciudad = input_no_vacio("Nombre de la ciudad")
    datos = obtener_clima(ciudad)
    if datos:
        console.print()
        mostrar_clima(datos)
        guardar_consulta(usuario, datos)
        console.print("\n[green]  ✓ Consulta guardada en el historial.[/green]")
    pausar()
    return datos


# Muestra el historial de consultas del usuario para una ciudad específica
def flujo_historial(usuario):
    limpiar_pantalla()
    imprimir_banner()
    console.print(Panel("[bold cyan]HISTORIAL PERSONAL[/bold cyan]", border_style="cyan", padding=(0, 2)))

    ciudad = input_no_vacio("Ciudad a consultar en el historial")
    limpiar_pantalla()
    imprimir_banner()
    ver_historial_personal(usuario, ciudad)
    pausar()


# Obtiene y muestra las estadísticas globales de todas las consultas
def flujo_estadisticas():
    limpiar_pantalla()
    imprimir_banner()

    stats = estadisticas_globales()
    # Si no hay datos todavía, mostramos un mensaje informativo
    if not stats:
        console.print(Panel(
            "[yellow]  Aún no hay consultas registradas.[/yellow]",
            title="[bold cyan]ESTADÍSTICAS GLOBALES[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        ))
    else:
        # Construimos la tabla con los datos calculados
        table = Table(show_header=False, border_style="cyan", padding=(0, 2))
        table.add_column("campo", style="bold white", no_wrap=True)
        table.add_column("valor", style="white")

        table.add_row("🏙  Ciudad más consultada", f"[bold]{stats['ciudad_mas_consultada']}[/bold]")
        table.add_row("📊 Total de consultas", f"[bold yellow]{stats['total_consultas']}[/bold yellow]")
        if stats["temperatura_promedio"] is not None:
            table.add_row("🌡  Temperatura promedio", f"[bold yellow]{stats['temperatura_promedio']} °C[/bold yellow]")

        console.print(Panel(
            table,
            title="[bold cyan]ESTADÍSTICAS GLOBALES[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        ))

    pausar()


# Pide consejo de vestimenta a la IA usando el último clima consultado
def flujo_consejo_ia(usuario, ultimo_clima):
    limpiar_pantalla()
    imprimir_banner()
    console.print(Panel("[bold cyan]CONSEJO DE VESTIMENTA (IA)[/bold cyan]", border_style="cyan", padding=(0, 2)))

    # Si no hay clima reciente en esta sesión, avisamos al usuario
    if not ultimo_clima:
        console.print(Panel(
            "[yellow]  No tenés una consulta de clima reciente en esta sesión.\n"
            "  Consultá el clima primero para obtener un consejo personalizado.[/yellow]",
            border_style="yellow",
            padding=(1, 2),
        ))
        pausar()
        return

    # Mostramos el resumen del clima antes del consejo
    resumen = Text()
    resumen.append("  Clima actual: ", style="white")
    resumen.append(f"{ultimo_clima['temperatura']}°C", style="bold yellow")
    resumen.append(f", {ultimo_clima['descripcion']}", style="white")
    console.print(resumen)
    console.print()

    # Llamamos a la IA y mostramos el consejo si se obtuvo correctamente
    consejo = obtener_consejo_ia(ultimo_clima)
    if consejo:
        console.print(Panel(
            f"[white]{consejo}[/white]",
            title="[bold cyan]🤖 Consejo de Vestimenta[/bold cyan]",
            border_style="green",
            padding=(1, 2),
        ))
    pausar()


# Muestra información sobre la aplicación y las APIs que usa
def mostrar_acerca_de():
    limpiar_pantalla()
    imprimir_banner()

    info = Text()
    info.append("Aplicación de consulta climática con inteligencia artificial\n", style="white")
    info.append("desarrollada como proyecto académico en el ITBA.\n\n", style="white")
    info.append("Características:\n", style="bold white")
    info.append("  🌤 Consulta del clima en tiempo real\n", style="white")
    info.append("  📊 Historial personal de consultas\n", style="white")
    info.append("  🤖 Consejos de vestimenta con IA (Gemini)\n", style="white")
    info.append("  👥 Sistema de usuarios con registro seguro\n\n", style="white")
    info.append("APIs utilizadas:\n", style="bold white")
    info.append("  • OpenWeatherMap — datos meteorológicos\n", style="cyan")
    info.append("  • Google Gemini   — inteligencia artificial\n\n", style="cyan")
    info.append("Proyecto ITBA — 2024", style="dim white")

    console.print(Panel(
        info,
        title="[bold cyan]ACERCA DE  GuardiánClima ITBA[/bold cyan]",
        border_style="cyan",
        padding=(1, 4),
    ))
    pausar()


# Menú principal que aparece después de iniciar sesión
def menu_principal(usuario):
    # Guardamos el último clima consultado para poder usarlo en el consejo de IA
    ultimo_clima = None

    while True:
        limpiar_pantalla()
        imprimir_banner()

        saludo = Text()
        saludo.append("  Hola, ", style="white")
        saludo.append(usuario, style="bold cyan")
        saludo.append(" 👋", style="white")
        console.print(saludo)
        console.print()

        menu = (
            "  [bold]1.[/bold] Consultar clima\n"
            "  [bold]2.[/bold] Ver historial personal\n"
            "  [bold]3.[/bold] Estadísticas globales\n"
            "  [bold]4.[/bold] Consejo de vestimenta (IA)\n"
            "  [bold]5.[/bold] Acerca De\n"
            "  [bold]6.[/bold] Cerrar sesión"
        )
        console.print(Panel(menu, title="[bold cyan]MENÚ PRINCIPAL[/bold cyan]", border_style="cyan", padding=(1, 2)))

        opcion = console.input("  [bold cyan]Opción:[/bold cyan] ").strip()

        # Ejecutamos la acción correspondiente a la opción elegida
        if opcion == "1":
            datos = flujo_consultar_clima(usuario)
            if datos:
                ultimo_clima = datos
        elif opcion == "2":
            flujo_historial(usuario)
        elif opcion == "3":
            flujo_estadisticas()
        elif opcion == "4":
            flujo_consejo_ia(usuario, ultimo_clima)
        elif opcion == "5":
            mostrar_acerca_de()
        elif opcion == "6":
            console.print(Panel(
                f"[bold cyan]  ¡Hasta pronto, {usuario}! 🌤[/bold cyan]",
                border_style="cyan",
                padding=(0, 2),
            ))
            break
        else:
            console.print("[yellow]  Opción inválida. Elegí entre 1 y 6.[/yellow]")
            pausar()


# Punto de entrada del programa: maneja el ciclo de sesiones de usuario
def main():
    while True:
        usuario = menu_acceso()
        if usuario is None:
            break
        menu_principal(usuario)


if __name__ == "__main__":
    main()
