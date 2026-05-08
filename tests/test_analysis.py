"""Tests for analysis module."""

import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from scienceplots_toolkit.analysis import (
    DailyStats,
    calculate_daily_stats,
    generate_profile_grid,
    plot_profile_with_quantiles,
)


class TestCalculateDailyStats:
    """Tests for calculate_daily_stats function."""

    @pytest.fixture
    def sample_data(self) -> tuple[np.ndarray, np.ndarray]:
        """Sample time-series data with multiple days."""
        # Create data for 3 days at 3 different times of day (0, 1, 2)
        timestamps = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
        data = np.array(
            [
                1.0,
                10.0,
                20.0,  # Day 1
                2.0,
                12.0,
                22.0,  # Day 2
                3.0,
                14.0,
                24.0,  # Day 3
            ]
        )
        return data, timestamps

    @pytest.fixture
    def daily_profile_data(self) -> tuple[np.ndarray, np.ndarray]:
        """Realistic 24h load profile data."""
        # Create 7 days of hourly data (0-23 hours)
        n_days = 7
        hours = np.tile(np.arange(24), n_days)
        # Base load with daily variation
        base_load = 50 + 20 * np.sin(2 * np.pi * (hours - 6) / 24)
        # Add some noise
        np.random.seed(42)
        noise = np.random.normal(0, 5, len(hours))
        data = base_load + noise
        return data, hours

    def test_calculate_daily_stats_basic(self, sample_data):
        """Test basic calculation of daily stats."""
        data, timestamps = sample_data
        stats = calculate_daily_stats(data, timestamps)

        # Check return type
        assert isinstance(stats, DailyStats)

        # Check that we have 3 unique timestamps (0, 1, 2)
        assert len(stats.timestamps) == 3
        assert np.array_equal(stats.timestamps, np.array([0, 1, 2]))

        # Check array shapes
        assert stats.mean.shape == (3,)
        assert stats.q10.shape == (3,)
        assert stats.q90.shape == (3,)
        assert stats.peak.shape == (3,)
        assert stats.min.shape == (3,)

    def test_calculate_daily_stats_mean(self, sample_data):
        """Test mean calculation accuracy."""
        data, timestamps = sample_data
        stats = calculate_daily_stats(data, timestamps)

        # For timestamp 0: values are [1.0, 2.0, 3.0], mean = 2.0
        assert np.isclose(stats.mean[0], 2.0)
        # For timestamp 1: values are [10.0, 12.0, 14.0], mean = 12.0
        assert np.isclose(stats.mean[1], 12.0)
        # For timestamp 2: values are [20.0, 22.0, 24.0], mean = 22.0
        assert np.isclose(stats.mean[2], 22.0)

    def test_calculate_daily_stats_percentiles(self, sample_data):
        """Test q10 and q90 calculation accuracy."""
        data, timestamps = sample_data
        stats = calculate_daily_stats(data, timestamps)

        # Verify q10 < mean < q90 for all timestamps
        assert np.all(stats.q10 < stats.mean)
        assert np.all(stats.mean < stats.q90)

        # For timestamp 0: values [1.0, 2.0, 3.0]
        # q10 should be close to 1.0 + (2.0-1.0)*0.2 = 1.2 (interpolated)
        # q90 should be close to 2.0 + (3.0-2.0)*0.8 = 2.8 (interpolated)
        assert stats.q10[0] < stats.mean[0] < stats.q90[0]
        assert stats.q10[1] < stats.mean[1] < stats.q90[1]
        assert stats.q10[2] < stats.mean[2] < stats.q90[2]

    def test_calculate_daily_stats_peak_min(self, sample_data):
        """Test peak and min calculation accuracy."""
        data, timestamps = sample_data
        stats = calculate_daily_stats(data, timestamps)

        # For timestamp 0: values [1.0, 2.0, 3.0]
        assert np.isclose(stats.peak[0], 3.0)
        assert np.isclose(stats.min[0], 1.0)

        # For timestamp 1: values [10.0, 12.0, 14.0]
        assert np.isclose(stats.peak[1], 14.0)
        assert np.isclose(stats.min[1], 10.0)

        # For timestamp 2: values [20.0, 22.0, 24.0]
        assert np.isclose(stats.peak[2], 24.0)
        assert np.isclose(stats.min[2], 20.0)

    def test_calculate_daily_stats_empty_data(self):
        """Test that empty data raises ValueError."""
        empty_data = np.array([])
        empty_timestamps = np.array([])

        with pytest.raises(ValueError, match="Data array is empty"):
            calculate_daily_stats(empty_data, empty_timestamps)

        # Test with data but empty timestamps
        data = np.array([1.0])
        with pytest.raises(ValueError, match="Timestamps array is empty"):
            calculate_daily_stats(data, empty_timestamps)

    def test_calculate_daily_stats_single_value(self):
        """Test handling of single data point."""
        data = np.array([5.0])
        timestamps = np.array([0])
        stats = calculate_daily_stats(data, timestamps)

        assert len(stats.timestamps) == 1
        assert np.isclose(stats.mean[0], 5.0)
        assert np.isclose(stats.q10[0], 5.0)
        assert np.isclose(stats.q90[0], 5.0)
        assert np.isclose(stats.peak[0], 5.0)
        assert np.isclose(stats.min[0], 5.0)

    def test_calculate_daily_stats_shape_mismatch(self):
        """Test that mismatched shapes raise ValueError."""
        data = np.array([1.0, 2.0, 3.0])
        timestamps = np.array([0, 1])  # Different length

        with pytest.raises(ValueError, match="must have the same shape"):
            calculate_daily_stats(data, timestamps)

    def test_calculate_daily_stats_24h_profile(self, daily_profile_data):
        """Test with realistic 24h load profile data."""
        data, hours = daily_profile_data
        stats = calculate_daily_stats(data, hours)

        # Should have 24 unique hours
        assert len(stats.timestamps) == 24
        assert np.array_equal(stats.timestamps, np.arange(24))

        # All arrays should have length 24
        assert stats.mean.shape == (24,)
        assert stats.q10.shape == (24,)
        assert stats.q90.shape == (24,)
        assert stats.peak.shape == (24,)
        assert stats.min.shape == (24,)

        # Verify q10 < mean < q90 for all hours
        assert np.all(stats.q10 < stats.mean)
        assert np.all(stats.mean < stats.q90)

        # Verify min <= q10 and q90 <= peak
        assert np.all(stats.min <= stats.q10)
        assert np.all(stats.q90 <= stats.peak)

    def test_calculate_daily_stats_output_types(self, sample_data):
        """Test that all output fields are numpy arrays."""
        data, timestamps = sample_data
        stats = calculate_daily_stats(data, timestamps)

        assert isinstance(stats.mean, np.ndarray)
        assert isinstance(stats.q10, np.ndarray)
        assert isinstance(stats.q90, np.ndarray)
        assert isinstance(stats.peak, np.ndarray)
        assert isinstance(stats.min, np.ndarray)
        assert isinstance(stats.timestamps, np.ndarray)


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
