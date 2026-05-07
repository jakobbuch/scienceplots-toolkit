"""
Generate README example plots.
Uses PURE DEFAULT settings with smart figsize scaling.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from scienceplots_toolkit import (
    configure_matplotlib_style,
    save_plot,
    plot_profile_with_quantiles,
    generate_profile_grid,
)
from scienceplots_toolkit.style import get_figsize
from scienceplots_toolkit.utils import configure_24h_axis, add_stats_box

# PURE DEFAULTS - exactly what users get
configure_matplotlib_style()

output_dir = Path(__file__).parent.parent / 'output' / 'readme'
output_dir.mkdir(parents=True, exist_ok=True)

print("Generating README example plots with PURE DEFAULTS...")
print("Settings: use_latex=False (default), grid=True (default)")
print("Using smart figsize scaling...")

# Example 1: Basic line plot (single panel - auto figsize)
print("  1. Basic line plot...")
figsize = get_figsize(1, 1)  # Returns (8.0, 5.0) - perfect for single plot
fig, ax = plt.subplots(figsize=figsize)
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label=r'$\sin(x)$')
ax.plot(x, np.cos(x), label=r'$\cos(x)$')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
ax.legend()
save_plot(fig, '01_basic_line', output_dir=output_dir)
plt.close(fig)

# Example 2: 24h load profile (single panel with x-label)
print("  2. 24h load profile...")
figsize = get_figsize(1, 1)
fig, ax = plt.subplots(figsize=figsize)
hours = np.arange(24)
load = 50 + 30 * np.sin(2 * np.pi * (hours - 6) / 24)
ax.plot(hours, load, marker='o', markersize=4)
configure_24h_axis(ax)
ax.set_xlabel('Time (h)')  # FIXED: Added x-axis label
ax.set_ylabel('Power (kW)')
add_stats_box(ax, avg=np.mean(load), peak=np.max(load), unit='kW')
save_plot(fig, '02_daily_profile', output_dir=output_dir)
plt.close(fig)

# Example 3: Quantile shading (single panel with x-label)
print("  3. Quantile profile...")
figsize = get_figsize(1, 1)
fig, ax = plt.subplots(figsize=figsize)
x = np.linspace(0, 24, 100)
mean = 50 + 25 * np.sin(2 * np.pi * (x - 6) / 24)
q10 = mean * 0.85
q90 = mean * 1.15
plot_profile_with_quantiles(ax, x, mean, q10, q90, label='Forecast')
configure_24h_axis(ax)
ax.set_xlabel('Time (h)')  # FIXED: Added x-axis label
ax.set_ylabel('Power (kW)')
ax.legend()
save_plot(fig, '03_quantile_profile', output_dir=output_dir)
plt.close(fig)

# Example 4: Multi-panel grid (2x2 - uses full base size)
print("  4. Multi-panel comparison...")
# figsize auto-calculated by generate_profile_grid
fig, axes = generate_profile_grid(n_rows=2, n_cols=2)
for i, ax in enumerate(axes):
    x = np.linspace(0, 24, 100)
    mean = 40 + i * 10 + 20 * np.sin(2 * np.pi * (x - 6) / 24)
    ax.fill_between(x, mean * 0.9, mean * 1.1, alpha=0.3)
    ax.plot(x, mean)
    configure_24h_axis(ax)
    ax.set_ylabel('Power (kW)')
    ax.set_title(f'Scenario {i+1}')
save_plot(fig, '04_multi_panel', output_dir=output_dir)
plt.close(fig)

# Example 5: Scatter with error bars (single panel)
print("  5. Scatter with error bars...")
figsize = get_figsize(1, 1)
fig, ax = plt.subplots(figsize=figsize)
x = np.arange(10)
y = 2 * x + 5 + np.random.normal(0, 2, 10)
yerr = np.random.uniform(1, 3, 10)
ax.errorbar(x, y, yerr=yerr, fmt='o', capsize=5, label='Measurements')
ax.plot(x, 2 * x + 5, '--', label='Model')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.legend()
save_plot(fig, '05_scatter_errorbars', output_dir=output_dir)
plt.close(fig)

print(f"\n✅ Generated with defaults: grid=True, use_latex=False")
print(f"Figsize scaling: single={get_figsize(1,1)}, 2x2={get_figsize(2,2)}")
print(f"Output: {output_dir}/")
