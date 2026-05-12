"""Shared fixtures and configuration for pytest test suite."""

import numpy as np
import pytest
import matplotlib.pyplot as plt
from pathlib import Path


@pytest.fixture(autouse=True)
def close_figures():
    """Close all matplotlib figures after each test.
    
    This fixture runs automatically for every test to prevent
    memory leaks from unclosed figures.
    """
    yield
    plt.close("all")


@pytest.fixture
def sample_data() -> np.ndarray:
    """Generate sample 1D data for testing.
    
    Returns:
        Numpy array with 24 data points (simulating 24h profile)
    """
    return np.linspace(0, 10, 24)


@pytest.fixture
def sample_2d_data() -> np.ndarray:
    """Generate sample 2D data for testing.
    
    Returns:
        Numpy array with shape (24, 24) for heatmap testing
    """
    x = np.linspace(-3, 3, 24)
    y = np.linspace(-3, 3, 24)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2))
    return Z


@pytest.fixture
def daily_profile_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate mock daily profile data with quantiles.
    
    Returns:
        Tuple of (x, mean, q10, q90) arrays
        - x: 24-hour time axis
        - mean: Mean profile with evening peak
        - q10: 10th percentile
        - q90: 90th percentile
    """
    x = np.arange(24)
    # Sinusoidal profile with peak in the evening
    mean = 50 + 30 * np.sin(2 * np.pi * (x - 6) / 24)
    q10 = mean * 0.85
    q90 = mean * 1.15
    return x, mean, q10, q90


@pytest.fixture
def multi_day_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate mock multi-day time series data.
    
    Returns:
        Tuple of (timestamps, data) arrays
        - timestamps: 7 days of hourly data (168 points)
        - data: Synthetic load data with daily patterns
    """
    # 7 days of hourly data
    timestamps = np.arange(168)
    # Daily pattern with some noise
    daily_pattern = 50 + 30 * np.sin(2 * np.pi * timestamps / 24)
    noise = np.random.normal(0, 5, 168)
    data = daily_pattern + noise
    return timestamps, data


@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    """Create temporary output directory for test plots.
    
    Args:
        tmp_path: Pytest temporary directory fixture
        
    Returns:
        Path to temporary output directory
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def sample_config() -> dict:
    """Generate sample configuration dictionary for testing.
    
    Returns:
        Dictionary with common configuration parameters
    """
    return {
        "fontsize": 26,
        "figsize": (16, 10),
        "use_latex": False,
        "grid": True,
        "dpi": 300,
    }


@pytest.fixture
def monthly_data() -> dict[str, np.ndarray]:
    """Generate mock monthly data for testing.
    
    Returns:
        Dictionary mapping month names to data arrays
    """
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    data = {}
    for i, month in enumerate(months):
        # Different pattern for each month
        base = 50 + i * 2  # Increasing trend through year
        variation = np.random.randn(24) * 5
        data[month] = base + variation
    
    return data


@pytest.fixture
def statsBox_params() -> dict:
    """Generate sample parameters for stats box testing.
    
    Returns:
        Dictionary with stats box parameters
    """
    return {
        "avg": 125.4,
        "peak": 210.8,
        "unit": r"\text{kW}",
    }


@pytest.fixture
def quantile_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate sample data for quantile shading tests.
    
    Returns:
        Tuple of (x, mean, q10, q90) arrays for quantile plotting
    """
    x = np.linspace(0, 24, 100)
    mean = 50 + 25 * np.sin(2 * np.pi * x / 24)
    q10 = mean * 0.9
    q90 = mean * 1.1
    return x, mean, q10, q90


# Optional: Import test utilities if they exist
try:
    from .test_utils import compare_images, image_similarity
except ImportError:
    # Test utilities not available, define stubs
    def compare_images(img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare two images and return similarity score.
        
        Args:
            img1: First image array
            img2: Second image array
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        return 1.0 if np.array_equal(img1, img2) else 0.0
    
    def image_similarity(img1: np.ndarray, img2: np.ndarray, threshold: float = 0.95) -> bool:
        """Check if two images are similar within threshold.
        
        Args:
            img1: First image array
            img2: Second image array
            threshold: Similarity threshold (default: 0.95)
            
        Returns:
            True if images are similar, False otherwise
        """
        return compare_images(img1, img2) >= threshold
