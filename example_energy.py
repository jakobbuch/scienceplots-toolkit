import argparse

import matplotlib.pyplot as plt
import numpy as np
from plotting_utils import add_stats_box, configure_24h_axis, save_plot
from profile_analysis import generate_profile_grid, plot_profile_with_quantiles

from MatplotlibStyle import configure_matplotlib_style


def generate_mock_profile(
    peak: float = 10.0, base: float = 2.0, noise: float = 0.5
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate a mock 24h load profile with quantiles."""
    x = np.linspace(0, 24, 24)
    # Sinusoidal profile with peak in the evening
    mean = base + (peak - base) * np.exp(-((x - 19) ** 2) / 20)
    q10 = mean * 0.8 + np.random.normal(0, noise, 24)
    q90 = mean * 1.2 + np.random.normal(0, noise, 24)
    return x, mean, q10, q90


def main(use_latex: bool = False) -> None:
    """Generate energy-related example plots."""
    configure_matplotlib_style(use_latex=use_latex)

    # 1) Standard 24h Profile with Stats Box and Quantiles
    x, mean, q10, q90 = generate_mock_profile(peak=12.5, base=3.0)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot_profile_with_quantiles(
        ax, x, mean, q10, q90, label=r"Household Load", color="C0"
    )

    configure_24h_axis(ax)
    add_stats_box(ax, avg=np.mean(mean), peak=np.max(mean), unit=r"\text{kW}")

    ax.set_xlabel(r"Time of Day (h)")
    ax.set_ylabel(r"Power Consumption (kW)")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.37), ncol=2)

    save_plot(fig, "energy_load_profile")
    plt.close(fig)

    # 2) Seasonal Comparison Grid (2x2)
    fig, axes = generate_profile_grid(n_rows=2, n_cols=2, figsize=(14, 10))
    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    peaks = [8.0, 12.0, 9.0, 15.0]

    handles, labels = [], []

    for i, (ax, season, peak) in enumerate(zip(axes, seasons, peaks)):
        x, mean, q10, q90 = generate_mock_profile(peak=peak)
        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Mean Load")
        ax.set_title(season)
        configure_24h_axis(ax)

        if i >= 2:  # Bottom row
            ax.set_xlabel(r"Time (h)")
        if i % 2 == 0:  # Left column
            ax.set_ylabel(r"Load (kW)")

        # Collect handles for a single figure legend from the first plot only
        if not handles:
            handles, labels = ax.get_legend_handles_labels()
            # Add quantile shading to legend manually if needed,
            # but plot_profile_with_quantiles only labels the mean line.

    # Add figure-level legend
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.1),
        ncol=len(labels),
    )

    save_plot(fig, "energy_seasonal_grid")
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--latex", action="store_true", help="Use LaTeX for rendering")
    args = parser.parse_args()
    main(use_latex=args.latex)
