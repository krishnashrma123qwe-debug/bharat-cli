import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

# Force UTF-8 safe console handling
console = Console(legacy_windows=False)

def print_banner():
    banner_text = Text()
    banner_text.append("Bharat", style="bold cyan")
    banner_text.append("Code ", style="bold dark_orange")
    banner_text.append("CLI  ", style="bold white")
    banner_text.append("v1.0.0", style="dim cyan")
    banner_text.append(" | Open-Source AI Coding Harness for India", style="italic")

    panel = Panel(
        banner_text,
        border_style="cyan",
        subtitle="[dim]Powered by Qwen 3.8 27B (256k Context)[/dim]",
        subtitle_align="right",
        padding=(0, 1)
    )
    console.print(panel)

def print_markdown(content: str):
    md = Markdown(content)
    console.print(md)

def print_code(code: str, language: str = "python"):
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)

def print_review_summary(file_name: str, score: int, critical_issues: int, warnings: int):
    table = Table(title=f"Code Review Summary: [bold cyan]{file_name}[/bold cyan]", border_style="cyan")
    table.add_column("Metric", style="bold white")
    table.add_column("Status / Score", justify="center")

    score_color = "green" if score >= 80 else ("yellow" if score >= 60 else "red")
    table.add_row("Overall Quality Score", f"[{score_color}]{score}/100[/{score_color}]")
    table.add_row("Critical Vulnerabilities", f"[red]{critical_issues}[/red]" if critical_issues else "[green]0[/green]")
    table.add_row("Code Smell & Warnings", f"[yellow]{warnings}[/yellow]" if warnings else "[green]0[/green]")
    table.add_row("Model Inference Engine", "[cyan]BharatCode Qwen 3.8 27B[/cyan]")

    console.print(table)

def print_success(msg: str):
    console.print(f"[bold green][OK][/bold green] {msg}")

def print_error(msg: str):
    console.print(f"[bold red][ERROR][/bold red] {msg}")

def print_info(msg: str):
    console.print(f"[bold cyan][INFO][/bold cyan] {msg}")
