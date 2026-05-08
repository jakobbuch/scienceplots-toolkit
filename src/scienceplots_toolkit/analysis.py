"""Specialized functions for time-series visualization and analysis."""

from dataclasses import dataclass
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes


@dataclass
class DailyStats:
    """Daily statistics calculated from time-series data.

    Attributes:
        mean: Mean value for each unique time of day.
        q10: 10th percentile for each unique time of day.
        q90: 90th percentile for each unique time of day.
        peak: Maximum value for each unique time of day.
        min: Minimum value for each unique time of day.
        timestamps: Unique timestamps (time of day) as numpy array.
    """

    mean: np.ndarray
    q10: np.ndarray
    q90: np.ndarray
    peak: np.ndarray
    min: np.ndarray
    timestamps: np.ndarray


def calculate_daily_stats(data: np.ndarray, timestamps: np.ndarray) -> DailyStats:
    """Calculate daily statistics grouped by time of day.

    Groups data by unique time-of-day values (hour:minute) and calculates
    mean, 10th percentile, 90th percentile, peak, and minimum for each group.

    Args:
        data: 1D array of time-series data values.
        timestamps: 1D array of timestamps corresponding to data values.
                   Should be in the same units as data (e.g., datetime or
                   numeric time representation).

    Returns:
        DailyStats object containing calculated statistics for each unique
        time of day.

    Raises:
        ValueError: If data or timestamps are empty, or if shapes don't match.

    Example:
        >>> data = np.array([1.0, 2.0, 1.5, 2.5, 3.0])
        >>> timestamps = np.array([0, 1, 0, 1, 2])  # hour groups
        >>> stats = calculate_daily_stats(data, timestamps)
        >>> stats.mean  # doctest: +SKIP
        array([1.25, 2.25, 3.0])
    """
    # Validate inputs
    if data.size == 0:
        raise ValueError("Data array is empty")
    if timestamps.size == 0:
        raise ValueError("Timestamps array is empty")
    if data.shape != timestamps.shape:
        raise ValueError(
            f"Data and timestamps must have the same shape. "
            f"Got data.shape={data.shape}, timestamps.shape={timestamps.shape}"
        )

    # Handle single value case
    if data.size == 1:
        return DailyStats(
            mean=data.copy(),
            q10=data.copy(),
            q90=data.copy(),
            peak=data.copy(),
            min=data.copy(),
            timestamps=timestamps.copy(),
        )

    # Get unique timestamps and sort them
    unique_timestamps = np.unique(timestamps)

    # Initialize arrays for statistics
    n_unique = len(unique_timestamps)
    means = np.zeros(n_unique)
    q10s = np.zeros(n_unique)
    q90s = np.zeros(n_unique)
    peaks = np.zeros(n_unique)
    mins = np.zeros(n_unique)

    # Calculate statistics for each unique timestamp
    for i, ts in enumerate(unique_timestamps):
        mask = timestamps == ts
        group_data = data[mask]

        means[i] = np.mean(group_data)
        q10s[i] = np.percentile(group_data, 10)
        q90s[i] = np.percentile(group_data, 90)
        peaks[i] = np.max(group_data)
        mins[i] = np.min(group_data)

    return DailyStats(
        mean=means,
        q10=q10s,
        q90=q90s,
        peak=peaks,
        min=mins,
        timestamps=unique_timestamps,
    )


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
