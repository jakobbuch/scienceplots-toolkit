"""Production orchestrator example for batch plot generation.

This script demonstrates how to build a production-ready plotting script
by subclassing BaseOrchestrator and using the @plot_function decorator.

Run with:
    uv run python examples/example_orchestrator.py              # Run all plots
    uv run python examples/example_orchestrator.py --list       # List available plots
    uv run python examples/example_orchestrator.py --only daily   # Run single plot
    uv run python examples/example_orchestrator.py --skip grid  # Skip a plot
    uv run python examples/example_orchestrator.py --latex      # With LaTeX

Usage examples:
    # List all available plots
    uv run python examples/example_orchestrator.py --list

    # Run all plots without LaTeX
    uv run python examples/example_orchestrator.py

    # Run only the daily profile with LaTeX
    uv run python examples/example_orchestrator.py --latex --only daily_profile

    # Skip the monthly grid and use custom output directory
    uv run python examples/example_orchestrator.py --skip monthly_grid --output-dir plots/

    # Run with high verbosity for debugging
    uv run python examples/example_orchestrator.py -vv --latex
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

from scienceplots_toolkit import (
    configure_matplotlib_style,
    generate_profile_grid,
    plot_profile_with_quantiles,
    save_plot,
)
from scienceplots_toolkit.cli import BaseOrchestrator, plot_function
from scienceplots_toolkit.utils import (
    add_stats_box,
    configure_24h_axis,
    create_monthly_grid,
)


def _make_mock_profile(
    base: float = 5.0, amplitude: float = 4.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate a mock 24h load profile with quantiles.

    Args:
        base: Base load level.
        amplitude: Peak-to-base amplitude.

    Returns:
        Tuple of (x, mean, q10, q90) for a 24h profile.
    """
    rng = np.random.default_rng(42)
    x = np.arange(24)
    mean = base + amplitude * np.exp(-((x - 19) ** 2) / 18)
    q10 = mean * 0.85 + rng.uniform(0, 0.5, 24)
    q90 = mean * 1.15 + rng.uniform(0, 0.5, 24)
    return x, mean, q10, q90


@plot_function(
    name="daily_profile",
    description="Basic 24-hour load profile with quantile shading",
    tags=["daily", "profile", "quantiles"],
)
def plot_daily_profile(args: argparse.Namespace) -> None:
    """Generate a single 24h load profile with quantile shading.

    Args:
        args: Parsed CLI arguments with latex, output_dir attributes.
    """
    latex = args.latex
    output_dir = args.output_dir

    configure_matplotlib_style(use_latex=latex)

    x, mean, q10, q90 = _make_mock_profile(base=5.0, amplitude=4.0)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Load", color="C0")
    configure_24h_axis(ax)
    add_stats_box(ax, avg=mean.mean(), peak=mean.max(), unit=r"\text{kW}")
    ax.set_xlabel(r"Time of Day (h)")
    ax.set_ylabel(r"Power (kW)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=2)

    save_plot(fig, "orch_daily_profile", output_dir)
    plt.close(fig)
    print(f"[daily_profile] Saved (latex={latex})")


@plot_function(
    name="seasonal_comparison",
    description="Four-season comparison grid",
    tags=["seasonal", "comparison", "grid"],
)
def plot_seasonal_comparison(args: argparse.Namespace) -> None:
    """Generate a 2x2 grid comparing seasonal load profiles.

    Args:
        args: Parsed CLI arguments with latex, output_dir attributes.
    """
    latex = args.latex
    output_dir = args.output_dir

    configure_matplotlib_style(use_latex=latex)

    fig, axes = generate_profile_grid(n_rows=2, n_cols=2, figsize=(14, 10))
    seasons_data = [
        ("Spring", 6.0, 3.0),
        ("Summer", 10.0, 4.5),
        ("Autumn", 8.0, 3.5),
        ("Winter", 14.0, 5.0),
    ]
    handles, labels = [], []

    for i, (ax, (season, base, amp)) in enumerate(zip(axes, seasons_data)):
        x, mean, q10, q90 = _make_mock_profile(base=base, amplitude=amp)
        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Seasonal Load")
        ax.set_title(season)
        configure_24h_axis(ax)

        h, l = ax.get_legend_handles_labels()
        for hi, li in zip(h, l):
            if li not in labels:
                handles.append(hi)
                labels.append(li)

        if i >= 2:
            ax.set_xlabel(r"Time (h)")
        if i % 2 == 0:
            ax.set_ylabel(r"Load (kW)")

    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=2)
    save_plot(fig, "orch_seasonal_comparison", output_dir)
    plt.close(fig)
    print(f"[seasonal_comparison] Saved (latex={latex})")


@plot_function(
    name="monthly_grid",
    description="4x3 monthly grid with seasonal load profiles",
    tags=["monthly", "grid", "seasonal"],
)
def plot_monthly_grid(args: argparse.Namespace) -> None:
    """Generate a 4x3 grid showing monthly load profiles for a full year.

    Args:
        args: Parsed CLI arguments with latex, output_dir attributes.
    """
    latex = args.latex
    output_dir = args.output_dir

    configure_matplotlib_style(use_latex=latex)

    fig, axes = create_monthly_grid(figsize=(12, 16))
    rng = np.random.default_rng(100)

    params = [
        (7.0, 2.0),
        (6.5, 2.0),
        (8.0, 2.5),
        (9.5, 3.0),
        (11.5, 3.5),
        (13.0, 4.0),
        (14.5, 4.5),
        (14.0, 4.5),
        (10.5, 3.5),
        (8.5, 3.0),
        (7.0, 2.5),
        (6.5, 2.0),
    ]

    for ax, (base, amp) in zip(axes, params):
        x = np.arange(24)
        mean = base + amp * np.exp(-((x - 19) ** 2) / 18)
        q10 = mean * 0.85 + rng.uniform(0, 0.3, 24)
        q90 = mean * 1.15 + rng.uniform(0, 0.3, 24)

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Profile", color="C0")
        configure_24h_axis(ax)

    fig.text(
        0.5,
        0.98,
        r"Monthly Load Profiles Across a Full Year",
        ha="center",
        va="top",
        fontsize=18,
    )

    save_plot(fig, "orch_monthly_grid", output_dir)
    plt.close(fig)
    print(f"[monthly_grid] Saved (latex={latex})")


@plot_function(
    name="with_stats",
    description="Profile with statistics box demonstrating auto-formatting",
    tags=["stats", "annotation", "formatting"],
)
def plot_with_stats(args: argparse.Namespace) -> None:
    """Generate a profile with annotated statistics using auto-formatting.

    Demonstrates add_stats_box() auto-formatting for kW (<100 -> 1dp)
    and kWh (>=100 -> 0dp).

    Args:
        args: Parsed CLI arguments with latex, output_dir attributes.
    """
    latex = args.latex
    output_dir = args.output_dir

    configure_matplotlib_style(use_latex=latex)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

    # Left: Power in kW (values < 100 -> 1 decimal by format_value)
    x = np.arange(24)
    mean_power = 5.0 + 4.0 * np.exp(-((x - 19) ** 2) / 18)
    plot_profile_with_quantiles(ax1, x, mean_power, mean_power * 0.85, mean_power * 1.15)
    configure_24h_axis(ax1)
    add_stats_box(ax1, avg=float(mean_power.mean()), peak=float(mean_power.max()), unit=r"\text{kW}")
    ax1.set_ylabel(r"Load (units)")

    # Right: Energy in kWh (values >= 100 -> 0 decimals by format_value)
    mean_energy = mean_power * 24.0
    plot_profile_with_quantiles(ax2, x, mean_energy, mean_energy * 0.85, mean_energy * 1.15)
    configure_24h_axis(ax2)
    add_stats_box(ax2, avg=float(mean_energy.mean()), peak=float(mean_energy.max()), unit=r"\text{kWh}")

    save_plot(fig, "orch_stats_formatting", output_dir)
    plt.close(fig)
    print(f"[with_stats] Saved two formatting styles (latex={latex})")


class SamplePlotOrchestrator(BaseOrchestrator):
    """Sample production orchestrator demonstrating plot orchestration.

    Subclasses BaseOrchestrator to register plot functions via the
    @plot_function decorator and implements run_plots() with CLI
    filtering support (--only, --skip).

    Attributes:
        plots: Dictionary mapping plot names to metadata dicts.
        args: Parsed CLI arguments (populated after main() is called).

    Example:
        >>> orchestrator = SamplePlotOrchestrator()
        >>> orchestrator.list_plots()
        >>> # orchestrator.main()
    """

    def __init__(self) -> None:
        """Initialize the orchestrator and register all decorated plot functions."""
        super().__init__()
        self._register_plots()

    def _register_plots(self) -> None:
        """Register all plot functions decorated with @plot_function."""
        self.register_from_decorator()

    def run_plots(self, args: argparse.Namespace) -> None:
        """Execute the requested plot functions.

        Respects --only (run exclusively these) and --skip (exclude these) lists.

        Args:
            args: Parsed CLI arguments containing:
                - only_list: List of plot names to run exclusively.
                - skip_list: List of plot names to exclude.
                - latex: Whether LaTeX rendering is enabled.
                - output_dir: Directory to save plot files.
        """
        plots_to_run = args.only_list if args.only_list else list(self.plots.keys())

        for name in plots_to_run:
            if name in args.skip_list:
                print(f"Skipping plot: {name}")
                continue
            try:
                self.run_plot(name, args)
            except Exception as exc:
                print(f"Error running plot '{name}': {exc}")


if __name__ == "__main__":
    orchestrator = SamplePlotOrchestrator()
    orchestrator.main()
