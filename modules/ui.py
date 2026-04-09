from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.table import Table
from rich.align import Align
import config

console = Console()

BANNER = r"""
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝"""


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def show_banner():
    banner_text = Text(BANNER, style="bold cyan")
    panel = Panel(
        Align.center(banner_text),
        border_style="bright_yellow",
        title="[bold bright_yellow]AI Voice Assistant[/]",
        subtitle="[dim]v1.0[/]",
        padding=(1, 2),
    )
    console.print()
    console.print(panel)
    console.print()


def show_system_info():
    table = Table(show_header=False, box=None, padding=(0, 2), expand=False)
    table.add_column(style="bold bright_yellow", justify="right")
    table.add_column(style="white")
    table.add_row("Model", config.GROQ_MODEL)
    table.add_row("Wake Word", f'"{config.WAKE_WORD_MODEL}"')
    table.add_row("Whisper", config.WHISPER_MODEL)
    table.add_row("Sample Rate", f"{config.SAMPLE_RATE} Hz")

    panel = Panel(
        Align.center(table),
        border_style="dim",
        title="[dim]System Config[/]",
        padding=(0, 1),
    )
    console.print(panel)
    console.print()


def show_initializing(label):
    return console.status(
        f"[bold cyan]  {label}[/]",
        spinner="dots",
        spinner_style="cyan",
    )


def show_online():
    console.print()
    console.print(Align.center(Text("SYSTEM ONLINE", style="bold green")))
    console.print()
    console.print(Rule(style="dim"))
    console.print()


def show_wake_waiting():
    return console.status(
        "[dim cyan]  Waiting for wake word...[/]  [dim]say \"Hey JARVIS\"[/]",
        spinner="dots",
        spinner_style="cyan",
    )


def show_wake_detected():
    console.print(f"  [bold cyan]>> Wake word detected![/]  [dim]{timestamp()}[/]")
    console.print()


def show_listening():
    return console.status(
        "[bold yellow]  Recording audio...[/]",
        spinner="dots12",
        spinner_style="yellow",
    )


def show_transcribing():
    return console.status(
        "[bold blue]  Transcribing speech...[/]",
        spinner="dots8Bit",
        spinner_style="blue",
    )


def show_thinking():
    return console.status(
        "[bold magenta]  Processing with AI...[/]",
        spinner="dots",
        spinner_style="magenta",
    )


def show_user_message(text):
    panel = Panel(
        Text(text, style="white"),
        border_style="cyan",
        title="[bold cyan]YOU[/]",
        title_align="left",
        subtitle=f"[dim]{timestamp()}[/]",
        subtitle_align="right",
        padding=(0, 2),
    )
    console.print(panel)


def show_jarvis_message(text):
    panel = Panel(
        Text(text, style="white"),
        border_style="bright_yellow",
        title="[bold bright_yellow]JARVIS[/]",
        title_align="left",
        subtitle=f"[dim]{timestamp()}[/]",
        subtitle_align="right",
        padding=(0, 2),
    )
    console.print(panel)


def show_no_input():
    console.print("  [dim yellow]No speech detected. Try again.[/]")
    console.print()


def show_error(message):
    panel = Panel(
        Text(message, style="bold red"),
        border_style="red",
        title="[bold red]ERROR[/]",
        padding=(0, 2),
    )
    console.print(panel)


def show_separator():
    console.print()
    console.print(Rule(style="dim"))
    console.print()


def show_shutdown():
    console.print()
    console.print(Rule(style="red"))
    console.print(Align.center(Text("SYSTEM OFFLINE", style="bold red")))
    console.print(Rule(style="red"))
    console.print()
