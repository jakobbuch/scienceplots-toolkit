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
    """Return the qualitative cmap of the given name (cmap.Colormap instance). Default is 'seaborn:tab10_new', more https://cmap-docs.readthedocs.io/en/latest/catalog/qualitative/seaborn%3Atab10_new/."""
    return Colormap(cmap_name)


def configure_matplotlib_style(
    styles: list[str] | str = ["science", "ieee", "grid"],
    grid_linewidth: float = 3,
    lines_linewidth: float = 4,
    fontsize: float = 26,
    figsize: tuple[float, float] = (12, 6),
    font: Literal["serif", "sans-serif"] | str = "serif",
    sans_serif_math: bool = False,
    cmap_name: str = DEFAULT_QUAL_CMAP_NAME,
    use_latex: bool = False,
    grid: bool = True,
    legend_framealpha: float = 1.0,
    legend_shadow: bool = True,
) -> None:
    """Configures matplotlib style and register the default qualitative colormap.

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
    if sans_serif_math:
        # Switch both text and math to sans-serif in LaTeX
        preamble += (
            r"\usepackage{sansmath}\sansmath\renewcommand{\familydefault}{\sfdefault}"
        )

    # reference: https://matplotlib.org/stable/users/explain/customizing.html
    rc: dict = {
        "font.size": fontsize,  # The font.size property is the default font size for text, given in points.
        "text.usetex": use_latex,  # use latex for all text handling.
        "text.latex.preamble": preamble,  # text.latex.preamble is a single line of LaTeX code that will be passed on to the LaTeX system.
        "font.family": font,  # The font.family property can take either a single or multiple entries of any combination of concrete font names
        "axes.titlesize": fontsize + 4,  # font size of the axes title
        "axes.labelsize": fontsize + 2,  # font size of the x and y labels
        "axes.axisbelow": False,  # draw axis gridlines and ticks: below patches (True), above patches but below lines ('line'), above all (False)
        # Do not set "axes.grid" here when grid is True; leave it to the applied style.
        "axes.prop_cycle": cycler(
            "color", default_colors
        ),  # colour cycle for plot lines as list of string colour specs: single letter, long name, or web-style hex
        "grid.linewidth": grid_linewidth,  # in points
        "lines.linewidth": lines_linewidth,  # line width in points
        "legend.handlelength": 1.5,  # the length of the legend lines
        "legend.shadow": legend_shadow,  # if True, give background a shadow effect
        "legend.framealpha": legend_framealpha,  # legend patch transparency
        "figure.titlesize": fontsize
        + 4,  # size of the figure title (``Figure.suptitle()``)
        "figure.labelsize": fontsize
        + 2,  # size of the figure label (``Figure.sup[x|y]label()``)
        "figure.figsize": figsize,  # figure size in inches
        "figure.constrained_layout.use": True,  # When True, automatically make plot elements fit on the figure, is the new and improved tight_layout
    }

    # Only explicitly disable the axes grid if the user requested grid=False.
    # If grid is True, we don't modify 'axes.grid' here so the style rules remain in effect.
    if grid is False:
        rc["axes.grid"] = False

    plt.rcParams.update(rc)
