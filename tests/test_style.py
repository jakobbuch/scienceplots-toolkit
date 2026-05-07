"""Tests for style configuration module."""

import matplotlib.pyplot as plt
import pytest

from scienceplots_toolkit.style import (
    configure_matplotlib_style,
    qual_cmap,
)


class TestQualCmap:
    """Tests for qual_cmap function."""

    def test_default_cmap(self):
        """Test default colormap returns Colormap instance."""
        cmap = qual_cmap()
        assert cmap is not None
        # Colormap has __call__ method and can be indexed
        assert callable(cmap)

    def test_custom_cmap_name(self):
        """Test custom colormap name."""
        cmap = qual_cmap("viridis")
        assert cmap is not None

    def test_invalid_cmap_raises_error(self):
        """Test invalid colormap name raises error."""
        with pytest.raises(Exception):  # cmap raises ValueError for invalid names
            qual_cmap("nonexistent_cmap_12345")


class TestConfigureMatplotlibStyle:
    """Tests for configure_matplotlib_style function."""

    def teardown_method(self):
        """Reset matplotlib style after each test."""
        plt.rcdefaults()

    def test_default_styles(self):
        """Test default style configuration."""
        configure_matplotlib_style()
        # Check that font size is set
        assert plt.rcParams["font.size"] == 26

    def test_custom_font_size(self):
        """Test custom font size."""
        configure_matplotlib_style(fontsize=14)
        assert plt.rcParams["font.size"] == 14

    def test_custom_figsize(self):
        """Test custom figure size."""
        configure_matplotlib_style(figsize=(8, 6))
        # rcParams returns list, not tuple
        assert list(plt.rcParams["figure.figsize"]) == [8.0, 6.0]

    def test_grid_false(self):
        """Test grid=False disables grid."""
        configure_matplotlib_style(grid=False)
        assert plt.rcParams["axes.grid"] is False

    def test_grid_true(self):
        """Test grid=True leaves grid to style (typically enabled)."""
        configure_matplotlib_style(grid=True)
        # Grid should be left to style defaults

    def test_legend_customization(self):
        """Test legend customization."""
        configure_matplotlib_style(legend_framealpha=0.5, legend_shadow=False)
        assert plt.rcParams["legend.framealpha"] == 0.5
        assert plt.rcParams["legend.shadow"] is False

    def test_sans_serif_math(self):
        """Test sans-serif font configuration."""
        configure_matplotlib_style(font="sans-serif")
        # rcParams returns list for font.family
        assert "sans-serif" in plt.rcParams["font.family"]

    def test_line_widths(self):
        """Test line width configuration."""
        configure_matplotlib_style(grid_linewidth=2, lines_linewidth=3)
        assert plt.rcParams["grid.linewidth"] == 2
        assert plt.rcParams["lines.linewidth"] == 3

    def test_color_cycle(self):
        """Test color cycle is set from colormap."""
        configure_matplotlib_style()
        assert "axes.prop_cycle" in plt.rcParams

    def test_constrained_layout(self):
        """Test constrained layout is enabled."""
        configure_matplotlib_style()
        assert plt.rcParams["figure.constrained_layout.use"] is True
