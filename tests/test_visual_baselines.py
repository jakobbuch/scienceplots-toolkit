"""Visual baseline snapshot tests for SciencePlots Toolkit.

Tests use pytest-mpl to compare generated plots against reference images.
These are not unit tests -- they ensure visual consistency across changes.

Run with baseline generation:
    uv run pytest tests/test_visual_baselines.py --mpl-generate-path=tests/baseline -v

Run against baselines:
    uv run pytest tests/test_visual_baselines.py -v
"""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from scienceplots_toolkit import (
    configure_matplotlib_style,
    plot_profile_with_quantiles,
)
from scienceplots_toolkit.utils import (
    add_stats_box,
    configure_24h_axis,
    create_monthly_grid,
)


@pytest.fixture(autouse=True)
def _close_figures():
    """Close all matplotlib figures after each test."""
    yield
    plt.close("all")


def _mock_quantile_data(
    n: int = 24, seed: int = 42
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate deterministic mock quantile data.

    Returns:
        Tuple of (x, mean, q10, q90) arrays.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0, 24, n)
    mean = 3.0 + 7.0 * np.exp(-((x - 19) ** 2) / 20)
    q10 = mean * 0.85 + rng.normal(0, 0.5, n)
    q90 = mean * 1.15 + rng.normal(0, 0.5, n)
    return x, mean, q10, q90


# ---------------------------------------------------------------------------
# 1. Basic line plot
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image_compare
def test_basic_line_plot():
    """Basic line plot with sin and cos curves."""
    configure_matplotlib_style(use_latex=False)
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.linspace(0, 10, 400)
    ax.plot(x, np.sin(x), label=r"$\sin(x)$")
    ax.plot(x, np.cos(x), label=r"$\cos(x)$")
    ax.plot(x, np.sin(2 * x) * 0.6, label=r"$0.6\,\sin(2x)$")

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=3)

    return fig


# ---------------------------------------------------------------------------
# 2. 24h load profile with stats box and quantiles
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image_compare
def test_energy_profile_with_stats():
    """24-hour load profile with quantile shading and stats annotation."""
    configure_matplotlib_style(use_latex=False)
    fig, ax = plt.subplots(figsize=(10, 6))

    x, mean, q10, q90 = _mock_quantile_data(seed=42)

    plot_profile_with_quantiles(
        ax, x, mean, q10, q90, label=r"Household Load", color="C0"
    )
    configure_24h_axis(ax)
    add_stats_box(
        ax, avg=float(np.mean(mean)), peak=float(np.max(mean)), unit=r"\text{kW}"
    )

    ax.set_xlabel(r"Time of Day (h)")
    ax.set_ylabel(r"Power Consumption (kW)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=2)

    return fig


# ---------------------------------------------------------------------------
# 3. Quantile shading profile (no stats box, simple)
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image_compare
def test_quantile_shading_profile():
    """Simple mean profile with 10%-90% quantile shading."""
    configure_matplotlib_style(use_latex=False)
    fig, ax = plt.subplots(figsize=(12, 5))

    x = np.linspace(0, 24, 48)
    mean = 50 + 25 * np.sin(2 * np.pi * (x - 6) / 24)
    q10 = mean * 0.85
    q90 = mean * 1.15

    plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Forecast")

    configure_24h_axis(ax)
    ax.set_xlabel(r"Time (h)")
    ax.set_ylabel(r"Power (kW)")
    ax.legend(loc="upper right")

    return fig


# ---------------------------------------------------------------------------
# 4. Monthly grid -- 4x3 layout with mock data per month
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image_compare
def test_monthly_grid():
    """4x3 monthly grid with mock load data per month."""
    configure_matplotlib_style(use_latex=False)
    fig, axes = create_monthly_grid(figsize=(12, 16))

    rng = np.random.default_rng(99)
    for ax in axes:
        x = np.linspace(0, 24, 24)
        base = rng.uniform(2, 6)
        peak = rng.uniform(5, 12)
        mean = base + (peak - base) * np.exp(-((x - 18) ** 2) / 18)
        q10 = mean * 0.88
        q90 = mean * 1.12
        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="", color="C0")
        configure_24h_axis(ax)
        ax.set_ylim(0, 20)

    fig.legend(["Mean Load", r"10%--90% Quantile"], loc="lower center", ncol=2)

    return fig


# ---------------------------------------------------------------------------
# 5. Monthly grid without quantiles (outline style)
# ---------------------------------------------------------------------------


@pytest.mark.mpl_image_compare
def test_monthly_grid_outline():
    """4x3 monthly grid showing simple line outlines (no quantiles)."""
    configure_matplotlib_style(use_latex=False, grid=False)
    fig, axes = create_monthly_grid(figsize=(12, 16))

    rng = np.random.default_rng(7)
    for ax in axes:
        x = np.linspace(0, 24, 24)
        amplitude = rng.uniform(3, 8)
        base = rng.uniform(1, 4)
        out = base + amplitude * np.exp(-((x - 17) ** 2) / 20)
        ax.plot(x, out, color="C0", linewidth=2)
        configure_24h_axis(ax)
        ax.set_ylim(0, 20)

    return fig
