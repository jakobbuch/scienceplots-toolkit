"""Generate analysis-related example plots using SciencePlots Toolkit.

This script demonstrates advanced analysis utilities:
- calculate_daily_stats() for grouping time-series data by time of day
- create_monthly_grid() for 12-month comparative layouts
- add_stats_box() with auto-formatting for different units
- check_system_requirements() for LaTeX availability

Run with:
    uv run example_analysis.py          # Without LaTeX (mathtext)
    uv run example_analysis.py --latex  # With LaTeX rendering
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

from scienceplots_toolkit import (
    configure_matplotlib_style,
    plot_profile_with_quantiles,
    save_plot,
)
from scienceplots_toolkit.analysis import DailyStats, calculate_daily_stats
from scienceplots_toolkit.utils import (
    add_stats_box,
    check_system_requirements,
    configure_24h_axis,
    create_monthly_grid,
)


def generate_hourly_timeseries(
    n_days: int, base: float = 5.0, amplitude: float = 4.0
) -> tuple[np.ndarray, np.ndarray]:
    """Generate mock hourly time-series data across multiple days.

    Args:
        n_days: Number of days of data to generate.
        base: Base load level.
        amplitude: Peak-to-base amplitude.

    Returns:
        Tuple of (data, timestamps) arrays.
        Timestamps are numeric hours within the day (0-23).
    """
    rng = np.random.default_rng(42)
    hours_per_day = 24
    total_points = n_days * hours_per_day

    # Create timestamps: cyclic hour-of-day across multiple days
    timestamps = np.resize(np.arange(hours_per_day), total_points)

    # Generate sinusoidal daily profile with some noise and day-to-day variation
    day_offsets = rng.uniform(-1.0, 1.0, n_days)
    data = np.zeros(total_points)
    for day in range(n_days):
        start = day * hours_per_day
        for h in range(hours_per_day):
            idx = start + h
            daily_pattern = base + amplitude * np.exp(-((h - 19) ** 2) / 18)
            data[idx] = daily_pattern + day_offsets[day] + rng.normal(0, 0.3)

    return data, timestamps


def section_basic_daily_stats(use_latex: bool) -> None:
    """Section 1: Calculate and plot daily statistics from multi-day data.

    Args:
        use_latex: If True, enable LaTeX rendering.
    """
    configure_matplotlib_style(use_latex=use_latex)

    print("=== Section 1: Daily Statistics ===")

    # Generate multi-day hourly data (7 days)
    data, timestamps = generate_hourly_timeseries(n_days=7, base=5.0, amplitude=4.0)

    # Calculate statistics grouped by hour of day
    stats: DailyStats = calculate_daily_stats(data, timestamps)

    print(f"  Unique hours in data: {len(stats.timestamps)}")
    print(f"  Mean range: [{stats.mean.min():.1f}, {stats.mean.max():.1f}]")
    print(f"  Peak range: [{stats.peak.min():.1f}, {stats.peak.max():.1f}]")

    # Plot the daily profile with quantiles and stats box
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_profile_with_quantiles(
        ax,
        stats.timestamps,
        stats.mean,
        stats.q10,
        stats.q90,
        label="Mean Load",
        color="C0",
    )

    configure_24h_axis(ax)
    add_stats_box(ax, avg=stats.mean.mean(), peak=stats.peak.max(), unit=r"\text{kW}")

    ax.set_xlabel(r"Time of Day (h)")
    ax.set_ylabel(r"Power Consumption (kW)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=2)

    save_plot(fig, "analysis_daily_stats")
    plt.close(fig)
    print("  Saved: analysis_daily_stats")


def section_monthly_grid(use_latex: bool) -> None:
    """Section 2: Create 4x3 monthly grid with seasonal profiles.

    Args:
        use_latex: If True, enable LaTeX rendering.
    """
    configure_matplotlib_style(use_latex=use_latex)

    print("\n=== Section 2: Monthly Grid ===")

    fig, axes = create_monthly_grid(figsize=(12, 16))
    rng = np.random.default_rng(123)

    # Seasonal parameters: (base, amplitude) for each month
    seasonal_params = [
        (8.0, 2.0),
        (7.5, 2.5),
        (9.0, 3.0),
        (10.0, 3.5),
        (12.0, 4.0),
        (14.0, 4.5),
        (15.0, 5.0),
        (14.5, 4.8),
        (11.0, 3.5),
        (9.0, 3.0),
        (7.0, 2.5),
        (6.5, 2.0),
    ]

    for ax, (base, amplitude) in zip(axes, seasonal_params):
        x = np.arange(24)
        mean = base + amplitude * np.exp(-((x - 19) ** 2) / 18)
        q10 = mean * 0.85 + rng.uniform(0, 0.5, 24)
        q90 = mean * 1.15 + rng.uniform(0, 0.5, 24)

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Profile", color="C0")
        configure_24h_axis(ax)

    # The grid title serves as identifier

    fig.text(
        0.5,
        0.98,
        r"Monthly Load Profiles (kW)",
        ha="center",
        va="top",
        fontsize=18,
    )

    save_plot(fig, "analysis_monthly_grid")
    plt.close(fig)
    print("  Saved: analysis_monthly_grid")


def section_stats_box_units(use_latex: bool) -> None:
    """Section 3: Stats box with different unit types (kW, kWh, °C).

    Args:
        use_latex: If True, enable LaTeX rendering.
    """
    configure_matplotlib_style(use_latex=use_latex)

    print("\n=== Section 3: Stats Box with Different Units ===")

    # 3a) Power in kW
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(24)
    mean_power = 5 + 4 * np.exp(-((x - 19) ** 2) / 18)
    plot_profile_with_quantiles(
        ax,
        x,
        mean_power,
        mean_power * 0.85,
        mean_power * 1.15,
        label="Power",
        color="C0",
    )
    configure_24h_axis(ax)
    add_stats_box(ax, avg=mean_power.mean(), peak=mean_power.max(), unit=r"\text{kW}")
    ax.set_ylabel(r"Power (kW)")
    ax.set_xlabel(r"Time of Day (h)")
    save_plot(fig, "analysis_stats_box_kw")
    plt.close(fig)
    print("  Saved: analysis_stats_box_kw (kW — 1 decimal for values < 100)")

    # 3b) Energy in kWh (larger values)
    fig, ax = plt.subplots(figsize=(10, 6))
    mean_energy = 120 + 60 * np.exp(-((x - 19) ** 2) / 18)
    plot_profile_with_quantiles(
        ax,
        x,
        mean_energy,
        mean_energy * 0.85,
        mean_energy * 1.15,
        label="Energy",
        color="C1",
    )
    configure_24h_axis(ax)
    add_stats_box(
        ax, avg=mean_energy.mean(), peak=mean_energy.max(), unit=r"\text{kWh}"
    )
    ax.set_ylabel(r"Energy (kWh)")
    ax.set_xlabel(r"Time of Day (h)")
    save_plot(fig, "analysis_stats_box_kwh")
    plt.close(fig)
    print("  Saved: analysis_stats_box_kwh (kWh — 0 decimals for values >= 100)")

    # 3c) Temperature in °C
    fig, ax = plt.subplots(figsize=(10, 6))
    mean_temp = -5 + 12 * np.exp(-((x - 14) ** 2) / 20)
    plot_profile_with_quantiles(
        ax,
        x,
        mean_temp,
        mean_temp * 0.9,
        mean_temp * 1.1,
        label="Temperature",
        color="C2",
    )
    configure_24h_axis(ax)
    add_stats_box(
        ax,
        avg=float(mean_temp.mean()),
        peak=float(mean_temp.max()),
        unit=r"^\circ\mathrm{C}",
    )
    ax.set_ylabel(r"Temperature ($^\circ\mathrm{C}$)")
    ax.set_xlabel(r"Time of Day (h)")
    save_plot(fig, "analysis_stats_box_celsius")
    plt.close(fig)
    print("  Saved: analysis_stats_box_celsius (\u00b0C — always 1 decimal)")


def section_latex_check(use_latex: bool) -> None:
    """Section 4: Check system requirements when LaTeX is enabled.

    Args:
        use_latex: Whether LaTeX mode is requested.
    """
    if not use_latex:
        print("\n=== Section 4: LaTeX Skip ===")
        print("  LaTeX not requested — skipping system check.")
        return

    print("\n=== Section 4: LaTeX System Check ===")
    result = check_system_requirements()

    if result["available"]:
        print(f"  LaTeX available: {result['available']}")
        print(f"  Warnings: {result['warnings']}")
    else:
        print(f"  LaTeX available: {result['available']}")
        print(f"  Missing executables: {result['missing']}")
        print(f"  Warnings: {result['warnings']}")

    # Create a simple plot with LaTeX check info in the title
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label=r"$\sin(x)$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\sin(x)$")
    ax.set_title(
        f"LaTeX Mode Active\nAvailable: {result['available']}, "
        f"Missing: {len(result['missing'])}"
    )
    ax.legend()
    save_plot(fig, "analysis_latex_status")
    plt.close(fig)
    print("  Saved: analysis_latex_status")


def main(use_latex: bool = False) -> None:
    """Generate analysis example plots.

    Args:
        use_latex: If True, enable LaTeX rendering and run system check.
    """
    # Section 1: Basic daily stats
    section_basic_daily_stats(use_latex)

    # Section 2: Monthly grid with seasonal profiles
    section_monthly_grid(use_latex)

    # Section 3: Stats box with different unit types
    section_stats_box_units(use_latex)

    # Section 4: LaTeX system requirements check
    section_latex_check(use_latex)

    print("\nDone! All plots saved to output/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate SciencePlots analysis example figures."
    )
    parser.add_argument(
        "--latex", action="store_true", help="Enable LaTeX rendering for text"
    )
    args = parser.parse_args()
    main(use_latex=args.latex)
