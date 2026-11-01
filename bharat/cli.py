import sys
from pathlib import Path

# Ensure root package directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click
from rich.prompt import Prompt

from bharat.client import BharatCodeClient
from bharat.ui import (
    console, print_banner, print_markdown, print_code,
    print_review_summary, print_success, print_error, print_info
)
from bharat.web_server import start_web_studio

@click.group()
@click.version_option("1.0.0", prog_name="bharat")
def cli():
    """BharatCode CLI — Open-Source AI Coding Harness powered by Qwen 3.8 27B."""
    pass

@cli.command()
@click.option("--key", prompt=True, hide_input=True, help="BharatCode API Key (bc_live_...)")
def auth(key):
    """Authenticate and configure your BharatCode API key."""
    print_banner()
    client = BharatCodeClient()
    client.save_key(key.strip())
    print_success("API Key successfully configured and saved to ~/.bharatcode/config.json!")

@cli.command()
def status():
    """Check BharatCode API connectivity and model status."""
    print_banner()
    client = BharatCodeClient()
    if not client.api_key:
        print_error("No API key configured. Run `bharat auth` first.")
        return

    print_info(f"Base URL: {client.base_url}")
    print_info(f"Configured Model: {client.model} (256k Context)")
    masked = client.api_key[:12] + "..." + client.api_key[-6:] if len(client.api_key) > 20 else "***"
    print_info(f"API Key: {masked}")

    try:
        with console.status("[bold cyan]Connecting to BharatCode Inference Lab...[/bold cyan]"):
            # Test model availability
            import requests
            r = requests.get(f"{client.base_url}/models", headers=client.get_headers(), timeout=10)
            if r.status_code == 200:
                print_success("Inference Gateway: ONLINE (HTTP 200 OK)")
            else:
                print_info(f"Inference Gateway status: {r.status_code}")
    except Exception as e:
        print_error(f"Could not reach API gateway: {e}")

@cli.command()
@click.argument("target", type=click.Path(exists=True))
@click.option("--security-only", is_flag=True, help="Focus exclusively on security vulnerabilities.")
def review(target, security_only):
    """Perform an automated AI code review on a file."""
    print_banner()
    client = BharatCodeClient()
    target_path = Path(target)

    if not target_path.is_file():
        print_error(f"Target '{target}' is not a file.")
        return

    content = target_path.read_text(encoding="utf-8", errors="ignore")
    if not content.strip():
        print_error("Target file is empty.")
        return

    print_info(f"Analyzing [bold cyan]{target_path.name}[/bold cyan] ({len(content.splitlines())} lines)...")

    focus = "SECURITY AUDIT: Look for SQL injections, XSS, unescaped queries, hardcoded secrets." if security_only else "COMPREHENSIVE CODE REVIEW: Look for bugs, anti-patterns, performance bottlenecks, and style improvements."
    prompt = f"""You are an elite code reviewer using Qwen 3.8 27B.
Review the following code file: `{target_path.name}`.
Focus: {focus}

Structure your response clearly with:
1. Executive Summary & Quality Score (out of 100)
2. Critical Bugs & Security Vulnerabilities (with line numbers if applicable)
3. Performance Optimizations
4. Recommended Refactored Implementation (in code block)

Code to review:
```{target_path.suffix.lstrip('.') or 'text'}
{content}
```
"""

    with console.status("[bold cyan]Reviewing code with BharatCode Qwen 3.8 27B...[/bold cyan]"):
        try:
            result = client.generate(prompt=prompt, system="You are an expert static code analysis and security auditing agent.")

            # Dynamic scoring based on code patterns detected
            code_lower = content.lower()
            critical = 0
            warnings = 0
            score = 95

            # Check for critical security issues
            security_patterns = [
                ("sql injection", ["f\"select", "f'select", '+ "select', "+ 'select", "execute(query", ".format(", "% ("]),
                ("hardcoded secret", ["password =", "secret =", "api_key =", "token ="]),
                ("dangerous exec", ["eval(", "exec(", "os.system(", "subprocess.call(", "__import__"]),
            ]
            for label, patterns in security_patterns:
                for p in patterns:
                    if p in code_lower:
                        critical += 1
                        score -= 12
                        break

            # Check for code smell warnings
            smell_patterns = [
                ("unclosed resource", ["open(", "connect("]),
                ("broad exception", ["except:", "except Exception:"]),
                ("magic number", [" == 0", " == 1", "range(100", "range(1000"]),
                ("no type hints", []),
            ]
            for label, patterns in smell_patterns:
                for p in patterns:
                    if p in code_lower:
                        warnings += 1
                        score -= 4
                        break

            # Check if 'with' statement is used (good practice reduces warnings)
            if "with open(" in code_lower:
                warnings = max(0, warnings - 1)
                score = min(100, score + 4)

            score = max(15, min(100, score))  # Clamp between 15-100

            print_review_summary(target_path.name, score=score, critical_issues=critical, warnings=warnings)
            console.print()
            print_markdown(result)
        except Exception as e:
            print_error(str(e))

@cli.command()
@click.argument("error_or_file", required=False)
def explain(error_or_file):
    """Diagnose an error message, stack trace, or crash log."""
    print_banner()
    client = BharatCodeClient()

    error_text = ""
    if error_or_file and Path(error_or_file).is_file():
        error_text = Path(error_or_file).read_text(encoding="utf-8", errors="ignore")
    elif error_or_file:
        error_text = error_or_file
    elif not sys.stdin.isatty():
        # Piped input: e.g. python script.py 2>&1 | bharat explain
        error_text = sys.stdin.read()
    else:
        error_text = Prompt.ask("[bold yellow]Paste the error traceback or log below[/bold yellow]")

    if not error_text.strip():
        print_error("No error input provided.")
        return

    prompt = f"""Analyze the following error / stack trace:
```
{error_text}
```
Explain:
1. Root Cause in 2 simple sentences
2. The exact file/line or variable responsible
3. The clean patch / code to fix it permanently
"""

    with console.status("[bold cyan]Diagnosing root cause with Qwen 3.8 27B...[/bold cyan]"):
        try:
            result = client.generate(prompt=prompt, system="You are a senior debugging assistant.")
            print_markdown(result)
        except Exception as e:
            print_error(str(e))

@cli.command()
@click.argument("prompt", nargs=-1, required=True)
@click.option("--out", "-o", type=click.Path(), help="Optional output file to write generated code.")
@click.option("--lang", default="python", help="Target programming language (default: python).")
def gen(prompt, out, lang):
    """Generate production-ready code from a natural language prompt."""
    print_banner()
    client = BharatCodeClient()
    user_prompt = " ".join(prompt)

    full_prompt = f"Write clean, idiomatic, well-tested {lang} code for the following task:\n{user_prompt}\nReturn ONLY the code block with comments."

    with console.status(f"[bold cyan]Generating {lang} code with BharatCode Qwen 3.8 27B...[/bold cyan]"):
        try:
            result = client.generate(prompt=full_prompt, system="You are an expert developer. Provide clean, secure, type-annotated code.")
            print_markdown(result)

            if out:
                Path(out).write_text(result, encoding="utf-8")
                print_success(f"Code saved to [bold cyan]{out}[/bold cyan]")
        except Exception as e:
            print_error(str(e))

@cli.command()
@click.option("--port", default=8484, help="Local port for the studio web workbench.")
def ui(port):
    """Launch the BharatCode Studio local web workbench."""
    print_banner()
    print_info(f"Starting BharatCode Studio UI on port {port}...")
    start_web_studio(port=port)

if __name__ == "__main__":
    cli()
