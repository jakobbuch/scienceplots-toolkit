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


def get_figsize(
    n_rows: int = 1, n_cols: int = 1, base_size: tuple[float, float] = (16, 10)
) -> tuple[float, float]:
    """Calculate appropriate figure size based on subplot grid dimensions.

    Uses a smart scaling algorithm that:
    - Scales width proportionally to number of columns (max 2x base width)
    - Scales height proportionally to number of rows (max 2x base height)
    - Applies minimum scaling to avoid overly small figures
    - Uses 75% of base size for single plots (1x1)

    Args:
        n_rows: Number of rows of subplots.
        n_cols: Number of columns of subplots.
        base_size: Base figure size (width, height) in inches. Default (16, 10).

    Returns:
        Tuple of (width, height) scaled appropriately for the subplot grid.

    Examples:
        >>> get_figsize(1, 1)  # Single plot - 75% of base
        (12.0, 7.5)
        >>> get_figsize(2, 2)  # 2x2 grid - base size
        (16, 10)
        >>> get_figsize(1, 3)  # 1x3 horizontal
        (16, 6.0)
        >>> get_figsize(3, 1)  # 3x1 vertical
        (11.2, 10)
    """
    base_width, base_height = base_size
    total_plots = n_rows * n_cols

    # For single plots, use 75% of base size
    if total_plots == 1:
        return (base_width * 0.75, base_height * 0.75)

    # For grids, scale based on dimensions
    # Width scales with columns (cap at 2x for very wide grids)
    # Height scales with rows (cap at 2x for very tall grids)
    width_scale = min(n_cols, 2) / 2.0
    height_scale = min(n_rows, 2) / 2.0

    # Ensure minimum reasonable size (don't go below 50% of base)
    width_scale = max(width_scale, 0.5)
    height_scale = max(height_scale, 0.5)

    return (base_width * width_scale, base_height * height_scale)


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
    legend_shadow: bool = False,  # Changed default to False (no black border)
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
            (transparent) to 1.0 (opaque). Default 1.0 for solid background.
        legend_shadow: If True, draw a shadow behind the legend frame.
            Default is False to avoid black border appearance.

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
        "legend.shadow": legend_shadow,  # Default False - no black border
        "legend.edgecolor": 'black',  # Explicit black edge for legend
        "legend.fancybox": True,  # Rounded corners on legend
        "figure.figsize": figsize,
        "figure.constrained_layout.use": True,
        "figure.facecolor": 'white',  # Explicit white figure background
        "figure.edgecolor": 'white',  # No black border on figure
        "axes.facecolor": 'white',  # Explicit white axes background
        "axes.edgecolor": 'black',  # Black axes border (standard)
    }

    # Only explicitly disable the axes grid if the user requested grid=False.
    # If grid is True, we don't modify 'axes.grid' here so the style rules remain in effect.
    if grid is False:
        rc["axes.grid"] = False

    plt.rcParams.update(rc)
