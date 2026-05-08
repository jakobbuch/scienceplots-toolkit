"""Tests for utility functions."""

import logging
from pathlib import Path
from unittest.mock import patch

import matplotlib.pyplot as plt

from scienceplots_toolkit.utils import (
    OUTPUT_DIR,
    add_stats_box,
    configure_24h_axis,
    create_monthly_grid,
    save_plot,
)


class TestSavePlot:
    """Tests for save_plot function."""

    def teardown_method(self):
        """Clean up test output directory."""
        test_output = Path("test_output")
        if test_output.exists():
            for f in test_output.glob("*"):
                f.unlink()
            test_output.rmdir()
        if OUTPUT_DIR.exists():
            for f in OUTPUT_DIR.glob("*.png"):
                f.unlink()
            for f in OUTPUT_DIR.glob("*.pdf"):
                f.unlink()

    def test_save_plot_default_dir(self, tmp_path):
        """Test saving plot to default output directory."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])

        # Mock OUTPUT_DIR to use temp directory
        with patch("scienceplots_toolkit.utils.OUTPUT_DIR", tmp_path):
            save_plot(fig, "test_plot")

        assert (tmp_path / "test_plot.png").exists()
        assert (tmp_path / "test_plot.pdf").exists()
        plt.close(fig)

    def test_save_plot_custom_dir(self, tmp_path):
        """Test saving plot to custom directory."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        custom_dir = tmp_path / "custom"

        save_plot(fig, "test_plot", output_dir=custom_dir)

        assert (custom_dir / "test_plot.png").exists()
        assert (custom_dir / "test_plot.pdf").exists()
        plt.close(fig)

    def test_save_plot_custom_dpi(self, tmp_path):
        """Test saving plot with custom DPI."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])

        with patch("scienceplots_toolkit.utils.OUTPUT_DIR", tmp_path):
            save_plot(fig, "test_plot", dpi=150)

        assert (tmp_path / "test_plot.png").exists()
        assert (tmp_path / "test_plot.pdf").exists()
        plt.close(fig)

    def test_save_plot_creates_directory(self, tmp_path):
        """Test that save_plot creates output directory if it doesn't exist."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])
        new_dir = tmp_path / "new_dir"

        save_plot(fig, "test_plot", output_dir=new_dir)

        assert new_dir.exists()
        assert (new_dir / "test_plot.png").exists()
        plt.close(fig)

    def test_save_plot_logs_message(self, tmp_path, caplog):
        """Test that save_plot logs info message."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3])

        with patch("scienceplots_toolkit.utils.OUTPUT_DIR", tmp_path):
            with caplog.at_level(logging.INFO):
                save_plot(fig, "test_plot")

        assert "Saved" in caplog.text
        assert "test_plot.png" in caplog.text
        plt.close(fig)


class TestConfigure24hAxis:
    """Tests for configure_24h_axis function."""

    def test_configure_24h_axis_xticks(self):
        """Test that 24h axis sets correct xticks."""
        fig, ax = plt.subplots()
        configure_24h_axis(ax)

        expected_ticks = list(range(0, 25, 4))
        assert list(ax.get_xticks()) == expected_ticks
        plt.close(fig)

    def test_configure_24h_axis_xlim(self):
        """Test that 24h axis sets correct xlim."""
        fig, ax = plt.subplots()
        configure_24h_axis(ax)

        xlim = ax.get_xlim()
        assert xlim[0] == 0
        assert xlim[1] == 24
        plt.close(fig)


class TestAddStatsBox:
    """Tests for add_stats_box function."""

    def test_add_stats_box_default(self):
        """Test stats box with default parameters."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=5.2, peak=12.3)

        # Check that text was added
        assert len(ax.texts) == 1
        text = ax.texts[0].get_text()
        assert "Avg" in text
        assert "Peak" in text
        assert "5.2" in text
        assert "12.3" in text
        plt.close(fig)

    def test_add_stats_box_custom_unit(self):
        """Test stats box with custom unit."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=100, peak=200, unit=r"\text{W}")

        text = ax.texts[0].get_text()
        assert r"\text{W}" in text
        plt.close(fig)

    def test_add_stats_box_positions(self):
        """Test stats box at different positions."""
        fig, ax = plt.subplots()

        # Test upper left
        add_stats_box(ax, avg=1, peak=2, loc="upper left")
        assert len(ax.texts) == 1
        plt.close(fig)

    def test_add_stats_box_upper_right(self):
        """Test stats box at upper right."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=1, peak=2, loc="upper right")

        # Check position
        text_obj = ax.texts[0]
        # upper right should be at (0.95, 0.95)
        assert text_obj.get_position()[0] == 0.95
        plt.close(fig)

    def test_add_stats_box_decimal_formatting(self):
        """Test that values are formatted with one decimal place."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=5.0, peak=10.0)

        text = ax.texts[0].get_text()
        assert "5.0" in text
        assert "10.0" in text
        plt.close(fig)


class TestCreateMonthlyGrid:
    """Tests for create_monthly_grid function."""

    def test_create_monthly_grid_returns_12_axes(self):
        """Test that monthly grid creates 12 axes."""
        fig, axes = create_monthly_grid()
        assert len(axes) == 12
        plt.close(fig)

    def test_create_monthly_grid_month_labels(self):
        """Test that each axis has month label."""
        fig, axes = create_monthly_grid()
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        for ax, month in zip(axes, months):
            assert month in ax.get_title()
        plt.close(fig)

    def test_create_monthly_grid_custom_sharey(self):
        """Test sharey parameter works."""
        fig, axes = create_monthly_grid(sharey=True)
        assert len(axes) == 12
        plt.close(fig)
