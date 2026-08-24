"""Typer CLI interface for DPX-Go."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pattern_detector.adapters.outbound.persistence.llm_report_formatter import LlmReportFormatter
from pattern_detector.bootstrap.container import Container, create_container
from pattern_detector.domain.detection import Detection, DetectionReport
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.rules import DEFAULT_RULES
from pattern_detector.domain.value_objects import ConfidenceLevel, PatternCategory
from pattern_detector.ports.inbound import ScanOptions

app = typer.Typer(
    name="dpx-go",
    help="🐹 Hexagonal Pattern Scanner & Architecture Detector for Go (Golang 1.18 - 1.24+).",
    no_args_is_help=True,
)
console = Console()


@app.command()
def scan(
    path: Annotated[
        str,
        typer.Argument(
            help="Path to a Go source file (.go) or directory containing a Go module / package.",
        ),
    ] = ".",
    min_confidence: Annotated[
        ConfidenceLevel,
        typer.Option(
            "--min-confidence",
            "-c",
            help="Minimum confidence threshold for reporting patterns.",
        ),
    ] = ConfidenceLevel.LOW,
    pattern: Annotated[
        list[str] | None,
        typer.Option(
            "--pattern",
            "-p",
            help="Filter for specific pattern type(s) by name (e.g. 'functional_options', 'worker_pool', 'pipeline').",
        ),
    ] = None,
    json_output: Annotated[
        str | None,
        typer.Option(
            "--json-output",
            "-J",
            help="Export findings to a JSON file.",
        ),
    ] = None,
    html_output: Annotated[
        str | None,
        typer.Option(
            "--html-output",
            "-H",
            help="Export interactive HTML dashboard.",
        ),
    ] = None,
    markdown_output: Annotated[
        str | None,
        typer.Option(
            "--markdown-output",
            "-M",
            help="Export findings to a Markdown report.",
        ),
    ] = None,
    sarif_output: Annotated[
        str | None,
        typer.Option(
            "--sarif-output",
            "-S",
            help="Export OASIS SARIF v2.1.0 file for GitHub Security / Code Scanning.",
        ),
    ] = None,
    llm: Annotated[
        bool,
        typer.Option(
            "--llm",
            help="Output structured AI architectural prompt context.",
        ),
    ] = False,
    no_principles: Annotated[
        bool,
        typer.Option(
            "--no-principles",
            help="Exclude SOLID principles and clean code rules from the report (GoF, Concurrency & Idioms only).",
        ),
    ] = False,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "--exclude",
            "-e",
            help="Directory name(s) or relative paths to exclude from scanning (e.g. -e test -e benchmarks -e examples -e vendor).",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose logging.",
        ),
    ] = False,
) -> None:
    """Scan a Go project or source file for design patterns, concurrency idioms, and architecture smells."""
    target_path = str(Path(path).resolve())
    container = create_container()
    options = ScanOptions(
        min_confidence=min_confidence,
        enabled_patterns=pattern or [],
        output_json_path=json_output,
        output_html_path=html_output,
        output_markdown_path=markdown_output,
        output_sarif_path=sarif_output,
        include_principles=not no_principles,
        exclude_dirs=exclude or [],
        verbose=verbose,
    )


    if llm:
        scanner = container.get_scanner()
        report = scanner.scan_path(target_path, options=options)
        formatter = LlmReportFormatter()
        print(formatter.format(report))
    else:
        _handle_terminal_scan(container, path, target_path, options)


def _handle_terminal_scan(
    container: Container,
    display_path: str,
    target_path: str,
    options: ScanOptions,
) -> None:
    scanner = container.get_scanner()
    report = scanner.scan_path(target_path, options=options)

    # 1. Header Banner
    header = Panel.fit(
        f"[bold white]🐹 DPX-Go: Pattern Scanner & Detector • Hexagonal Architecture[/bold white]\n"
        f"[dim]Scanned: {report.scanned_files_count} file(s) in {report.elapsed_seconds:.3f}s | Found: {report.total_detections_count} pattern instance(s)[/dim]",
        border_style="bright_green",
    )
    console.print(header)

    if not report.detections:
        console.print("[yellow]No patterns detected matching the criteria.[/yellow]")
        return

    # 2. Category Summary Table
    table = Table(title="📊 Detection Summary by Category", header_style="bold green")
    table.add_column("Pattern Category", style="cyan")
    table.add_column("Detections", justify="right", style="green")
    table.add_column("Confidence Breakdown", style="dim")

    for cat in PatternCategory:
        cat_dets = [d for d in report.detections if d.pattern_category == cat]
        if cat_dets:
            vh = sum(1 for d in cat_dets if d.level == ConfidenceLevel.VERY_HIGH)
            h = sum(1 for d in cat_dets if d.level == ConfidenceLevel.HIGH)
            m = sum(1 for d in cat_dets if d.level == ConfidenceLevel.MEDIUM)
            l = sum(1 for d in cat_dets if d.level == ConfidenceLevel.LOW)
            breakdown = f"{vh} VERY HIGH, {h} HIGH, {m} MED, {l} LOW"
            table.add_row(cat.value.upper(), str(len(cat_dets)), breakdown)

    console.print(table)
    console.print()

    # 3. Print Detection Cards
    console.print("[bold]📋 Identified Design Patterns & Idioms:[/bold]\n")
    for idx, d in enumerate(report.detections, 1):
        color = _get_confidence_color(d.level)
        loc = f"📍 Location: [cyan]{d.primary_location}[/cyan]" if d.primary_location else "📍 Location: [dim]N/A[/dim]"
        header_text = f"[bold cyan]#{idx} {d.pattern_type.value.upper()}[/bold cyan] on [bold]{d.target_kind}[/bold] '[yellow]{d.target_name}[/yellow]'"

        lines = [
            header_text,
            f"├── {loc}",
            f"├── 🎯 Confidence: [{color}]{d.confidence.percentage_str} [{d.level.value.upper()}][/{color}]",
            f"├── 📝 Summary: {d.summary}",
            f"└── 🔎 Evidence Trail ({len(d.evidences)} heuristics):",
        ]
        for i, ev in enumerate(d.evidences):
            is_last = i == len(d.evidences) - 1
            connector = "    └──" if is_last else "    ├──"
            ev_loc = f" → [cyan]{ev.location}[/cyan]" if ev.location else ""
            lines.append(f"{connector} [green]+{int(ev.weight * 100)}%[/green] ([dim]{ev.rule_code}[/dim]) {ev.description}{ev_loc}")

        console.print("\n".join(lines))
        console.print()


def _get_confidence_color(level: ConfidenceLevel) -> str:
    if level == ConfidenceLevel.VERY_HIGH:
        return "bright_green"
    if level == ConfidenceLevel.HIGH:
        return "green"
    if level == ConfidenceLevel.MEDIUM:
        return "yellow"
    return "red"


@app.command()
def rules() -> None:
    """List all supported software design patterns, Go concurrency idioms, and architecture rules."""
    table = Table(title="🐹 Supported Patterns & Rules in DPX-Go", header_style="bold green")
    table.add_column("Rule Name", style="bold cyan")
    table.add_column("Type", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Description", style="dim")

    for r in sorted(DEFAULT_RULES, key=lambda x: (x.pattern_category.value, x.name)):
        table.add_row(r.name, r.pattern_type.value, r.pattern_category.value.upper(), r.description[:65] + "...")

    console.print(table)


@app.command()
def catalog() -> None:
    """Alias for rules list."""
    rules()


@app.command()
def info() -> None:
    """Display DPX-Go architecture, version, and grammar engine details."""
    panel = Panel(
        """[bold green]🐹 DPX-Go • Design Pattern & Architecture Scanner[/bold green]
[dim]Multi-Paradigm Hexagonal Pattern Detector & Go AST Engine[/dim]

• [bold]Target Language:[/bold] Go (Golang 1.18 - 1.24+ edition)
• [bold]Architecture:[/bold] Hexagonal Ports & Adapters + Domain-Driven Design (DDD)
• [bold]Rules Supported:[/bold] 40 Rules (GoF, Functional Options, Concurrency Pipelines, Worker Pools, sync.Once, SOLID, Leak Guard)
• [bold]Outputs:[/bold] Rich Terminal, JSON, Markdown, OASIS SARIF v2.1.0, Interactive Dark Semantic UI HTML Dashboard
""",
        title="ℹ️ System Information",
        border_style="bright_green",
    )
    console.print(panel)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
