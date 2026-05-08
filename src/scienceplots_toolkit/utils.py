"""Utility functions for saving and configuring plots."""

import logging
import shutil
import subprocess
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# Constants
OUTPUT_DIR = Path("output")
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
logger = logging.getLogger(__name__)


def format_value(value: float, unit: str) -> str:
    """Format value based on unit type."""
    # kW, kWh → 1 decimal for values < 100, 0 decimals for >= 100
    if "kW" in unit or "kWh" in unit:
        return f"{value:.1f}" if value < 100 else f"{value:.0f}"
    # Temperature → 1 decimal
    elif "°C" in unit or "C" in unit:
        return f"{value:.1f}"
    # Percentages → 1 decimal
    elif "%" in unit:
        return f"{value:.1f}"
    # Default → 2 decimals
    else:
        return f"{value:.2f}"


def save_plot(
    fig: Figure, filename_base: str, output_dir: Path | None = None, dpi: int = 300
) -> None:
    """Save current figure to PNG and PDF.

    Args:
        fig: Figure to save.
        filename_base: Base filename (no extension).
        output_dir: Directory to save files. Defaults to OUTPUT_DIR.
        dpi: Resolution for the PNG output.

    """
    if output_dir is None:
        output_dir = OUTPUT_DIR

    # Ensure output_dir is a Path object
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    png_path = output_dir / f"{filename_base}.png"
    pdf_path = output_dir / f"{filename_base}.pdf"
    fig.savefig(png_path, dpi=dpi)
    fig.savefig(pdf_path, dpi=dpi)
    logger.info("Saved %s and %s", png_path, pdf_path)


def configure_24h_axis(ax: Axes) -> None:
    """Standardise 24-hour time axes (0-24h with 4h ticks).

    Args:
        ax: Axes to configure.

    """
    ax.set_xticks(range(0, 25, 4))
    ax.set_xlim(0, 24)


def add_stats_box(
    ax: Axes,
    avg: float,
    peak: float,
    unit: str = r"\text{kW}",
    loc: str = "upper left",
) -> None:
    """Add annotation boxes showing Average and Peak values.

    Args:
        ax: Axes to annotate.
        avg: Average value.
        peak: Peak value.
        unit: LaTeX unit string.
        loc: Position of the box (standard matplotlib loc strings).

    """
    stats_text = (
        rf"$\text{{Avg}}: {format_value(avg, unit)}\ {unit}$"
        "\n"
        rf"$\text{{Peak}}: {format_value(peak, unit)}\ {unit}$"
    )

    # Convert loc string to coordinates if needed, or use ax.text with transform
    props = dict(boxstyle="round", facecolor="white", alpha=0.8, edgecolor="gray")

    # Mapping standard locs to coordinates for simple implementation
    loc_map = {
        "upper left": (0.05, 0.95),
        "upper right": (0.95, 0.95),
        "upper center": (0.5, 0.95),
    }
    x, y = loc_map.get(loc, (0.05, 0.95))

    ha = "left" if "left" in loc else ("right" if "right" in loc else "center")
    va = "top" if "upper" in loc else "bottom"

    ax.text(
        x,
        y,
        stats_text,
        transform=ax.transAxes,
        verticalalignment=va,
        horizontalalignment=ha,
        bbox=props,
    )


def check_system_requirements() -> dict:
    """Check if LaTeX and required packages are available.

    Returns:
        Dict with keys: 'available' (bool), 'missing' (list), 'warnings' (list)

    Example:
        >>> result = check_system_requirements()
        >>> if not result['available']:
        ...     print(f"Missing: {result['missing']}")
    """
    result = {"available": True, "missing": [], "warnings": []}

    # Check executables
    for exe in ["latex", "pdflatex"]:
        if shutil.which(exe) is None:
            result["missing"].append(exe)
            result["available"] = False

    # Check required packages (simplified - just check if kpsewhich works)
    if result["available"]:
        required_packages = ["amsmath", "siunitx", "gensymb"]
        for pkg in required_packages:
            # Use kpsewhich to check if package is available
            check_result = subprocess.run(
                ["kpsewhich", f"{pkg}.sty"], capture_output=True, text=True
            )
            if check_result.returncode != 0:
                result["warnings"].append(f"Package {pkg} may not be installed")

    return result


def create_monthly_grid(
    figsize: tuple[float, float] = (12, 16),
    sharex: bool = False,
    sharey: bool = False,
) -> tuple[Figure, list[Axes]]:
    """Create a 4x3 grid of subplots for monthly profiles.

    Each subplot is labeled with a month name, arranged chronologically:
    Jan-Feb-Mar (row 1), Apr-May-Jun (row 2), Jul-Aug-Sep (row 3),
    Oct-Nov-Dec (row 4).

    Args:
        figsize: Figure size in inches (width, height). Defaults to (12, 16).
        sharex: Share x-axis across all subplots.
        sharey: Share y-axis across all subplots.

    Returns:
        Tuple of (Figure, list of Axes) for easy iteration.

    Example:
        >>> fig, axes = create_monthly_grid()
        >>> for ax in axes:
        ...     ax.plot([1, 2, 3])
    """
    fig, axes = plt.subplots(4, 3, figsize=figsize, sharex=sharex, sharey=sharey)
    axes_flat = axes.flatten()

    for ax, month in zip(axes_flat, MONTHS):
        ax.set_title(month)

    return fig, list(axes_flat)
