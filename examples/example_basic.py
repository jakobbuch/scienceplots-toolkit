"""Generate standard example plots using SciencePlots Toolkit.

This script demonstrates basic usage of the scienceplots_toolkit package
for creating publication-quality scientific plots with LaTeX typesetting.

Run with:
    uv run example_basic.py          # Without LaTeX (mathtext)
    uv run example_basic.py --latex  # With LaTeX rendering
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np

from scienceplots_toolkit import configure_matplotlib_style, save_plot


def main(use_latex: bool = False) -> None:
    """Generate and save example plots using SciencePlots styles.

    Args:
        use_latex: If True, enable LaTeX rendering for text.
    """
    # 1) Line plot with multiple traces
    configure_matplotlib_style(use_latex=use_latex)
    x = np.linspace(0, 10, 400)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(2 * x) * 0.6

    fig, ax = plt.subplots()
    ax.plot(x, y1, label=r"$\sin(x)$")
    ax.plot(x, y2, label=r"$\cos(x)$")
    ax.plot(x, y3, label=r"$0.6\,\sin(2x)$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=3)
    save_plot(fig, "advanced_lineplot")
    plt.close(fig)

    # 2) Scatter plot with color mapping
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    rng = np.random.default_rng(0)
    x_data = rng.normal(size=(200, 2))
    vals = np.hypot(x_data[:, 0], x_data[:, 1])

    fig, ax = plt.subplots()
    sc = ax.scatter(
        x_data[:, 0], x_data[:, 1], c=vals, cmap="coolwarm", s=50, edgecolor="k"
    )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("distance")
    save_plot(fig, "advanced_scatter")
    plt.close(fig)

    # 3) Simple heatmap
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    xx, yy = np.meshgrid(x, y)
    z = np.exp(-(xx**2 + yy**2))

    fig, ax = plt.subplots()
    im = ax.imshow(z, origin="lower", extent=(x[0], x[-1], y[0], y[-1]), cmap="viridis")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cbar = fig.colorbar(im, ax=ax)
    save_plot(fig, "advanced_heatmap")
    plt.close(fig)

    # 4) Interface tracking profiles with formulas and annotations
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    fig, ax = plt.subplots()
    n = 500
    delta = 0.6
    x = np.linspace(-1, 1, n)

    ax.plot(
        x,
        (1 - np.tanh(4 * x / delta)) / 2,
        color="C0",
    )
    ax.plot(x, (1.4 + np.tanh(4 * x / delta)) / 4, color="C2")
    ax.plot(x, x < 0, "k--")

    ax.legend(("phase field", "level set", "sharp interface"), loc=(0.01, 0.48))

    ax.annotate(
        "",
        xy=(-delta / 2.0, 0.1),
        xytext=(delta / 2.0, 0.1),
        arrowprops=dict(arrowstyle="<->", connectionstyle="arc3", linewidth=2.2),
    )
    ax.text(
        0,
        0.1,
        r"$\delta$",
        color="black",
        horizontalalignment="center",
        verticalalignment="center",
        bbox=dict(boxstyle="round", fc="white", ec="black", pad=0.2),
    )

    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels([r"$-1$", r"$\pm 0$", r"$+1$"], color="k")

    ax.set_ylabel(r"phase field $\phi$", color="C0")
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels([r"0", r".5", r"1"], color="k")

    ax.text(
        1.02,
        0.5,
        r"level set $\phi$",
        color="C2",
        rotation=90,
        horizontalalignment="left",
        verticalalignment="center",
        clip_on=False,
        transform=ax.transAxes,
    )

    eq1 = (
        r"$|\nabla\phi| = 1$"
        "\n"
        r"$\frac{\partial \phi}{\partial t} + U|\nabla \phi| = 0$"
    )
    ax.text(
        1, 0.9, eq1, color="C2", horizontalalignment="right", verticalalignment="top"
    )

    eq2 = (
        r"$\mathcal{F} = \int f( \phi, c ) dV$"
        "\n"
        r"$\frac{ \partial \phi } { \partial t } = -M_{ \phi } \frac{ \delta \mathcal{F} } { \delta \phi }$"
    )
    ax.text(
        0.96,
        0.45,
        eq2,
        color="C0",
        horizontalalignment="right",
        verticalalignment="top",
        transform=ax.transAxes,
    )

    ax.text(-1, 0.30, r"gamma: $\gamma$", color="C2")
    ax.text(-1, 0.18, r"Omega: $\Omega$", color="C0")

    save_plot(fig, "interface_profiles")
    plt.close(fig)

    # 5) Plot with sans-serif font and math font
    configure_matplotlib_style(
        font="sans-serif",
        sans_serif_math=True,
        use_latex=use_latex,
    )

    x = np.linspace(0, 10, 200)
    y = np.sin(2 * np.pi * x / 5) * 0.8

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel(r"Time (s)")
    ax.set_ylabel(r"Amplitude (units)")

    save_plot(fig, "advanced_ticks_sans_serif")
    plt.close(fig)

    # 6) Line plot with legend inside figure, no shadow, alpha 0.8
    configure_matplotlib_style(
        legend_shadow=False,
        legend_framealpha=0.8,
        use_latex=use_latex,
    )
    x = np.linspace(0, 10, 400)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(2 * x) * 0.6

    fig, ax = plt.subplots()
    ax.plot(x, y1, label=r"$\sin(x)$")
    ax.plot(x, y2, label=r"$\cos(x)$")
    ax.plot(x, y3, label=r"$0.6\,\sin(2x)$")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    save_plot(fig, "advanced_legend_no_shadow")
    plt.close(fig)

    # 7) Bar chart with horizontal grid lines only
    configure_matplotlib_style(use_latex=use_latex)
    categories = ["A", "B", "C", "D"]
    values = [23, 45, 10, 30]

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=["C0", "C1", "C2", "C3"])
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    ax.xaxis.grid(False)
    save_plot(fig, "bar_horizontal_grid_only")
    plt.close(fig)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate SciencePlots example figures."
    )
    parser.add_argument(
        "--latex", action="store_true", help="Enable LaTeX rendering for text"
    )
    args = parser.parse_args()
    main(use_latex=args.latex)


if __name__ == "__main__":
    _cli()
