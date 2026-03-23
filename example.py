import argparse

import matplotlib.pyplot as plt
import numpy as np
from plotting_utils import save_plot

from MatplotlibStyle import configure_matplotlib_style


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
    # place legend centered above the plot
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.28), ncol=3)
    save_plot(fig, "advanced_lineplot")
    plt.close(fig)

    # 2) Scatter plot with color mapping
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 2))
    vals = np.hypot(X[:, 0], X[:, 1])

    fig, ax = plt.subplots()
    sc = ax.scatter(X[:, 0], X[:, 1], c=vals, cmap="coolwarm", s=50, edgecolor="k")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("distance")
    save_plot(fig, "advanced_scatter")
    plt.close(fig)

    # 3) Simple heatmap
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    xx = np.linspace(-3, 3, 200)
    yy = np.linspace(-3, 3, 200)
    Xg, Yg = np.meshgrid(xx, yy)
    Z = np.exp(-(Xg**2 + Yg**2))

    fig, ax = plt.subplots()
    im = ax.imshow(
        Z, origin="lower", extent=(xx[0], xx[-1], yy[0], yy[-1]), cmap="viridis"
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    cbar = fig.colorbar(im, ax=ax)
    save_plot(fig, "advanced_heatmap")
    plt.close(fig)

    # 4) interface tracking profiles with formulas and annotations
    # Modified to work without external LaTeX (removed eqnarray, \bf)
    configure_matplotlib_style(use_latex=use_latex, grid=False)
    fig, ax = plt.subplots()
    # interface tracking profiles
    N = 500
    delta = 0.6
    X = np.linspace(-1, 1, N)
    # thicker traces for visibility
    ax.plot(
        X,
        (1 - np.tanh(4 * X / delta)) / 2,  # phase field tanh profiles
        color="C0",
    )
    ax.plot(
        X, (1.4 + np.tanh(4 * X / delta)) / 4, color="C2"
    )  # composition / level-set profile
    ax.plot(X, X < 0, "k--")  # sharp interface (dashed)

    # legend with custom placing to not interfere with the text
    ax.legend(("phase field", "level set", "sharp interface"), loc=(0.01, 0.48))

    # the arrow
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

    # Use tex in labels
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels([r"$-1$", r"$\pm 0$", r"$+1$"], color="k")

    # Left Y-axis labels, combine math mode and text mode
    ax.set_ylabel(r"phase field $\phi$", color="C0")
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels([r"0", r".5", r"1"], color="k")

    # Right Y-axis labels
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

    # level set equations (Simplified for mathtext)
    eq1 = (
        r"$|\nabla\phi| = 1$"
        "\n"
        r"$\frac{\partial \phi}{\partial t} + U|\nabla \phi| = 0$"
    )
    # place the equation
    ax.text(
        1, 0.9, eq1, color="C2", horizontalalignment="right", verticalalignment="top"
    )

    # phase field equations (Simplified for mathtext)
    eq2 = (
        r"$\mathcal{F} = \int f( \phi, c ) dV$"
        "\n"
        r"$\frac{ \partial \phi } { \partial t } = -M_{ \phi } \frac{ \delta \mathcal{F} } { \delta \phi }$"
    )
    # place the equation
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

    # 5) plot with sans-serif font and math font
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
    # legend inside the plot area, no shadow, semi-transparent
    ax.legend()
    save_plot(fig, "advanced_legend_no_shadow")
    plt.close(fig)

    # 7) Bar chart with horizontal grid lines only (no vertical grid lines)
    configure_matplotlib_style(use_latex=use_latex)
    categories = ["A", "B", "C", "D"]
    values = [23, 45, 10, 30]

    fig, ax = plt.subplots()
    ax.bar(categories, values, color=["C0", "C1", "C2", "C3"])
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")
    # Disable vertical grid lines (x-axis grid)
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
