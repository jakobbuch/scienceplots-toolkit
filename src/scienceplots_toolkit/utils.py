"""Utility functions for saving and configuring plots."""

import logging
from pathlib import Path

from matplotlib.axes import Axes
from matplotlib.figure import Figure

# Constants
OUTPUT_DIR = Path("output")
logger = logging.getLogger(__name__)


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
        rf"$\text{{Avg}}: {avg:.1f}\ {unit}$"
        "\n"
        rf"$\text{{Peak}}: {peak:.1f}\ {unit}$"
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
