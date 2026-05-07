"""Specialized functions for time-series visualization and analysis."""

from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


def plot_profile_with_quantiles(
    ax: Axes,
    x: np.ndarray,
    mean: np.ndarray,
    q10: np.ndarray,
    q90: np.ndarray,
    label: str,
    color: str | None = None,
) -> None:
    """Plot mean with 10%–90% quantile shading.

    Args:
        ax: Axes to plot on.
        x: X-axis values (usually 0-24).
        mean: Mean profile data.
        q10: 10th percentile profile data.
        q90: 90th percentile profile data.
        label: Legend label for the mean line.
        color: Optional fixed color for line and shading.

    """
    line = ax.plot(x, mean, label=label, color=color, linewidth=2.5)
    c = line[0].get_color()
    ax.fill_between(
        x, q10, q90, alpha=0.2, color=c, edgecolor="none", label=r"10%--90% Quantile"
    )


def generate_profile_grid(
    n_rows: int,
    n_cols: int,
    figsize: tuple[float, float] = (16, 10),
    sharey: Literal["row", "col", "all"] | bool = "row",
) -> tuple[plt.Figure, list[Axes]]:
    """Generate multi-panel grids of 24h profiles with standard axis sharing.

    Args:
        n_rows: Number of rows in the grid.
        n_cols: Number of columns in the grid.
        figsize: Size of the complete figure.
        sharey: Axis sharing mode (default 'row').

    Returns:
        A tuple containing (figure, list of axes).

    """
    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=figsize,
        sharex=True,
        sharey=sharey,
    )

    # Flatten axes if needed
    if n_rows * n_cols > 1:
        axes_list = axes.flatten()
    else:
        axes_list = [axes]

    return fig, axes_list
