"""Centralised Matplotlib styling and configuration for consistent plotting."""

from typing import Literal

import matplotlib.pyplot as plt
import scienceplots  # noqa: F401 - Required for matplotlib 'science' and 'ieee' styles
from cmap import Colormap
from cycler import cycler

# Default qualitative colormap used across plots
DEFAULT_QUAL_CMAP_NAME = "seaborn:tab10_new"

# https://cmap-docs.readthedocs.io/en/latest/catalog/qualitative/seaborn%3Atab10_new/
# tab10_new colour codes:
# blue  #4E79A7
# orange #F28E2B
# red   #E15759
# light blue  #76B7B2
# green #59A14E
# yellow  #EDC949
# lila #AF7AA1
# rosa #FF9DA7
# brown #9C755F
# grey #BAB0AB


def qual_cmap(cmap_name: str = DEFAULT_QUAL_CMAP_NAME) -> Colormap:
    """Return the qualitative cmap of the given name (cmap.Colormap instance).

    Default is 'seaborn:tab10_new'.
    See: https://cmap-docs.readthedocs.io/en/latest/catalog/qualitative/seaborn%3Atab10_new/
    """
    return Colormap(cmap_name)


def configure_matplotlib_style(
    styles: list[str] | str = ["science", "ieee", "grid"],
    grid_linewidth: float = 3,
    lines_linewidth: float = 4,
    fontsize: float = 26,
    figsize: tuple[float, float] = (16, 10),
    font: Literal["serif", "sans-serif"] | str = "serif",
    sans_serif_math: bool = False,
    cmap_name: str = DEFAULT_QUAL_CMAP_NAME,
    use_latex: bool = False,
    grid: bool = True,
    legend_framealpha: float = 1.0,
    legend_shadow: bool = True,
) -> None:
    """Configure matplotlib style and register the default qualitative colormap.

    Args:
        styles: list or single style name passed to plt.style.use, default
            ["science", "ieee"], enable grid with "grid" in the list.
        grid_linewidth: Width to use for grid lines.
        lines_linewidth: Width for plot lines.
        fontsize: Base font size.
        figsize: Figure size as (width, height) in inches.
        font: Font family to use (e.g., 'serif', 'sans-serif' or specific font
            e.g., 'Times', 'Helvetica').
            See: https://matplotlib.org/stable/users/explain/text/usetex.html
        sans_serif_math: If True, use sans-serif font for math text (default
            serif math in LaTeX).
        cmap_name: Name of the qualitative colormap to use for default colours.
            See: https://cmap-docs.readthedocs.io/en/latest/catalog/qualitative/seaborn%3Atab10_new/
        use_latex: If True, use LaTeX for text rendering. If False (default), use
            'no-latex' style and disable usetex.
        grid: Whether to enable axis gridlines by default (`axes.grid` rcParam).
            Disable for stuff like Heatmaps.
        legend_framealpha: Alpha (transparency) of the legend background, 0.0
            (transparent) to 1.0 (opaque). Default 1 because of legend_shadow.
        legend_shadow: If True (default), draw a shadow behind the legend frame.

    """
    # Reset to default matplotlib style before applying new styles
    plt.rcdefaults()

    # Get colors from the qualitative colormap
    cm = qual_cmap(cmap_name)
    default_colors = [
        cm(i / (9)) for i in range(10)
    ]  # 10 colors from the qualitative colormap

    # Handle no-latex logic
    if not use_latex:
        if isinstance(styles, list):
            styles = [s if s != "ieee" else "no-latex" for s in styles]
        elif styles == "ieee":
            styles = "no-latex"

    # Apply scienceplots style
    plt.style.use(styles)

    # Build LaTeX preamble
    preamble = (
        r"\usepackage{amsmath,amssymb,amsfonts}"
        r"\usepackage{textcomp}"
        r"\usepackage{gensymb}"
        r"\usepackage{siunitx}"
        r"\usepackage{graphicx}"
    )

    # Configure matplotlib rcParams
    rc = {
        "font.size": fontsize,
        "font.family": font,
        "font.serif": [
            "Times New Roman",
            "DejaVu Serif",
            "Bitstream Vera Serif",
        ],
        "font.sans-serif": [
            "Arial",
            "Helvetica",
            "DejaVu Sans",
            "Bitstream Vera Sans",
        ],
        "axes.prop_cycle": cycler(color=default_colors),
        "lines.linewidth": lines_linewidth,
        "axes.linewidth": grid_linewidth,
        "grid.linewidth": grid_linewidth,
        "legend.framealpha": legend_framealpha,
        "legend.shadow": legend_shadow,
        "mathtext.fontset": "custom" if not use_latex else "stix",
        "mathtext.rm": "Times New Roman",
        "mathtext.it": "Times New Roman:italic",
        "mathtext.bf": "Times New Roman:bold",
        "figure.figsize": figsize,  # figure size in inches
        "figure.constrained_layout.use": True,  # When True, automatically make plot elements fit on the figure, is the new and improved tight_layout
    }

    # Only explicitly disable the axes grid if the user requested grid=False.
    # If grid is True, we don't modify 'axes.grid' here so the style rules remain in effect.
    if grid is False:
        rc["axes.grid"] = False

    plt.rcParams.update(rc)


def get_figsize(
    n_rows: int = 1, n_cols: int = 1, base_size: tuple[float, float] = (16, 10)
) -> tuple[float, float]:
    """Calculate appropriate figure size based on number of subplots.

    Scales the base size to avoid overly large figures for single plots
    while maintaining good proportions for multi-panel layouts.

    Args:
        n_rows: Number of rows of subplots.
        n_cols: Number of columns of subplots.
        base_size: Base figure size (width, height) in inches. Default (16, 10).

    Returns:
        Tuple of (width, height) scaled appropriately for the subplot count.

    Examples:
        >>> get_figsize(1, 1)  # Single plot - smaller
        (8.0, 5.0)
        >>> get_figsize(2, 2)  # 2x2 grid - base size
        (16, 10)
        >>> get_figsize(1, 3)  # 1x3 horizontal
        (16, 5.0)
    """
    total_plots = n_rows * n_cols

    # Single plot: use half the base size (more reasonable for single panels)
    if total_plots == 1:
        return (base_size[0] * 0.5, base_size[1] * 0.5)
    elif n_rows == 1:
        # Single row: scale width by columns, keep height reasonable
        return (base_size[0] * min(n_cols * 0.5, 2), base_size[1] * 0.6)
    elif n_cols == 1:
        # Single column: scale height by rows, keep width reasonable
        return (base_size[0] * 0.7, base_size[1] * min(n_rows * 0.6, 1.2))
    else:
        # Grid: scale based on total area needed
        width_scale = min(n_cols, 2) * 0.5
        height_scale = min(n_rows, 2) * 0.5
        return (base_size[0] * width_scale, base_size[1] * height_scale)
