"""Tests for analysis module."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from scienceplots_toolkit.analysis import (
    generate_profile_grid,
    plot_profile_with_quantiles,
)


class TestPlotProfileWithQuantiles:
    """Tests for plot_profile_with_quantiles function."""

    def test_plot_profile_basic(self):
        """Test basic profile plotting."""
        fig, ax = plt.subplots()
        x = np.linspace(0, 24, 24)
        mean = np.sin(x) + 5
        q10 = mean * 0.9
        q90 = mean * 1.1

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Test")

        # Check that line was added
        assert len(ax.lines) == 1
        # Check that fill_between was added (as a collection)
        assert len(ax.collections) == 1

        # Check label
        assert ax.lines[0].get_label() == "Test"
        plt.close(fig)

    def test_plot_profile_custom_color(self):
        """Test profile with custom color."""
        fig, ax = plt.subplots()
        x = np.linspace(0, 24, 24)
        mean = np.ones(24) * 5
        q10 = np.ones(24) * 4
        q90 = np.ones(24) * 6

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Test", color="red")

        # Check line color
        line = ax.lines[0]
        assert line.get_color() == "red"
        plt.close(fig)

    def test_plot_profile_line_width(self):
        """Test that line has correct width."""
        fig, ax = plt.subplots()
        x = np.linspace(0, 24, 24)
        mean = np.ones(24) * 5
        q10 = np.ones(24) * 4
        q90 = np.ones(24) * 6

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Test")

        line = ax.lines[0]
        assert line.get_linewidth() == 2.5
        plt.close(fig)

    def test_plot_profile_fill_alpha(self):
        """Test that fill_between has correct alpha."""
        fig, ax = plt.subplots()
        x = np.linspace(0, 24, 24)
        mean = np.ones(24) * 5
        q10 = np.ones(24) * 4
        q90 = np.ones(24) * 6

        plot_profile_with_quantiles(ax, x, mean, q10, q90, label="Test")

        fill = ax.collections[0]
        assert fill.get_alpha() == 0.2
        plt.close(fig)


class TestGenerateProfileGrid:
    """Tests for generate_profile_grid function."""

    def test_generate_profile_grid_2x2(self):
        """Test 2x2 grid generation."""
        fig, axes = generate_profile_grid(n_rows=2, n_cols=2)

        assert isinstance(fig, Figure)
        assert len(axes) == 4
        assert all(isinstance(ax, Axes) for ax in axes)
        plt.close(fig)

    def test_generate_profile_grid_1x1(self):
        """Test 1x1 grid (single plot)."""
        fig, axes = generate_profile_grid(n_rows=1, n_cols=1)

        assert isinstance(fig, Figure)
        # Single axis should still be returned as a list
        assert len(axes) == 1
        plt.close(fig)

    def test_generate_profile_grid_3x3(self):
        """Test 3x3 grid generation."""
        fig, axes = generate_profile_grid(n_rows=3, n_cols=3)

        assert isinstance(fig, Figure)
        assert len(axes) == 9
        plt.close(fig)

    def test_generate_profile_grid_custom_figsize(self):
        """Test custom figure size."""
        fig, axes = generate_profile_grid(n_rows=2, n_cols=2, figsize=(12, 8))

        # Figure size should match (within floating point precision)
        assert abs(fig.get_figwidth() - 12) < 0.01
        assert abs(fig.get_figheight() - 8) < 0.01
        plt.close(fig)

    def test_generate_profile_grid_sharey_row(self):
        """Test sharey='row' parameter."""
        fig, axes = generate_profile_grid(n_rows=2, n_cols=2, sharey="row")

        assert isinstance(fig, Figure)
        assert len(axes) == 4
        plt.close(fig)

    def test_generate_profile_grid_sharey_all(self):
        """Test sharey='all' parameter."""
        fig, axes = generate_profile_grid(n_rows=2, n_cols=2, sharey="all")

        assert isinstance(fig, Figure)
        assert len(axes) == 4
        plt.close(fig)

    def test_generate_profile_grid_sharey_false(self):
        """Test sharey=False parameter."""
        fig, axes = generate_profile_grid(n_rows=2, n_cols=2, sharey=False)

        assert isinstance(fig, Figure)
        assert len(axes) == 4
        plt.close(fig)
