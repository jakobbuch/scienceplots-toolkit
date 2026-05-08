"""SciencePlots Toolkit - Publication-quality Matplotlib plotting utilities.

A toolkit for creating consistent, publication-quality scientific plots
using Matplotlib with SciencePlots styles and LaTeX typesetting.

Example usage:
    >>> from scienceplots_toolkit import configure_matplotlib_style, save_plot
    >>> from scienceplots_toolkit.utils import configure_24h_axis
    >>>
    >>> configure_matplotlib_style(use_latex=True)
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3], [4, 5, 6])
    >>> configure_24h_axis(ax)
    >>> save_plot(fig, "my_plot")
"""

from scienceplots_toolkit.analysis import (
    generate_profile_grid,
    plot_profile_with_quantiles,
)
from scienceplots_toolkit.cli import BaseOrchestrator, create_cli_parser, plot_function
from scienceplots_toolkit.latex import PreambleManager
from scienceplots_toolkit.style import (
    DEFAULT_QUAL_CMAP_NAME,
    configure_matplotlib_style,
    qual_cmap,
)
from scienceplots_toolkit.utils import (
    OUTPUT_DIR,
    add_stats_box,
    check_system_requirements,
    configure_24h_axis,
    save_plot,
)

__version__ = "0.1.0"
__author__ = "Jakob Buchmeier"
__email__ = "jakob.buchmeier@tuwien.ac.at"

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Style configuration
    "configure_matplotlib_style",
    "qual_cmap",
    "DEFAULT_QUAL_CMAP_NAME",
    # Utilities
    "save_plot",
    "configure_24h_axis",
    "add_stats_box",
    "OUTPUT_DIR",
    # Analysis
    "plot_profile_with_quantiles",
    "generate_profile_grid",
    # LaTeX preamble
    "PreambleManager",
    # CLI
    "BaseOrchestrator",
    "plot_function",
    "create_cli_parser",
]
