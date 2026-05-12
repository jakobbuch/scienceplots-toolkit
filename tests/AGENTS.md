# AGENTS.md — Testing (`tests/`)

This directory contains all test suites for the `scienceplots_toolkit` package.

## Global Mandates

<!-- rule:T-001 -->

- **Inherit Root Mandates**: All instructions in the [Root AGENTS.md](../AGENTS.md) apply here.

## Testing Philosophy

<!-- rule:T-002 -->

- **Testing Pyramid**: Follow the testing pyramid
  - **Unit Tests** (base): Fast, isolated, test individual functions
  - **Integration Tests** (middle): Test module interactions
  - **Visual Tests** (top): Validate plot output with baseline comparison

<!-- rule:T-003 -->

- **100% Coverage Goal**: All new code must have complete test coverage
  - Use `pytest-cov` to measure coverage
  - Aim for >90% line coverage, 100% for critical paths
  - Branch coverage for conditional logic

<!-- rule:T-004 -->

- **Test Isolation**: Each test must be independent
  - No shared state between tests
  - Use fixtures for setup/teardown
  - Clean up after tests (close figures, remove temp files)

## Test Organization

```
tests/
├── __init__.py              # Empty package marker
├── conftest.py              # Shared fixtures (CREATE THIS)
├── test_style.py            # Style configuration tests
├── test_utils.py            # Utility function tests
├── test_analysis.py         # Analysis module tests
└── test_visual_baselines.py # Visual regression tests
```

## Test File Structure

<!-- rule:T-005 -->

- **Class-per-Module**: Organize tests in classes mapping to source modules
  ```python
  class TestConfigureMatplotlibStyle:
      """Tests for style.py functions."""

  class TestSavePlot:
      """Tests for utils.py functions."""
  ```

<!-- rule:T-006 -->

- **Descriptive Method Names**: Test methods describe what they test
  ```python
  def test_calculate_daily_stats_mean(self):
      """Verify mean calculation is correct."""

  def test_save_plot_creates_directory(self):
      """Verify output directory is created if missing."""
  ```

## Fixture Standards

<!-- rule:T-007 -->

- **Use `conftest.py` for Shared Fixtures**: Move reusable fixtures to `conftest.py`
  ```python
  @pytest.fixture
  def sample_data() -> np.ndarray:
      """Generate sample data for testing."""
      return np.arange(24)

  @pytest.fixture(autouse=True)
  def close_figures():
      """Close all matplotlib figures after each test."""
      yield
      plt.close("all")
  ```

<!-- rule:T-008 -->

- **Autouse for Cleanup**: Use `autouse=True` for cleanup fixtures
  - Close matplotlib figures
  - Remove temporary files
  - Reset global state

## Test Types

### Unit Tests

Test individual functions in isolation:

```python
class TestAddStatsBox:
    def test_add_stats_box_default_unit(self):
        """Test stats box with default kW unit."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=5.2, peak=12.3)
        # Assert text contains expected values

    def test_add_stats_box_custom_unit(self):
        """Test stats box with custom unit."""
        fig, ax = plt.subplots()
        add_stats_box(ax, avg=25, peak=40, unit=r"\text{°C}")
        # Assert text contains custom unit
```

### Visual Baseline Tests

Use `pytest-mpl` for visual regression testing:

```python
@pytest.mark.mpl_image_compare
def test_basic_line_plot():
    """Test basic line plot matches baseline."""
    configure_matplotlib_style(use_latex=False)
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x))
    return fig  # pytest-mpl captures and compares
```

**Baseline Management**:

- Baselines stored in `tests/baseline/`
- Update baselines: `pytest --mpl-generate-path=tests/baseline`
- Run visual tests: `pytest tests/test_visual_baselines.py -v`

### Integration Tests

Test module interactions:

```python
def test_full_workflow():
    """Test complete plotting workflow."""
    configure_matplotlib_style()
    fig, ax = plt.subplots()
    plot_profile_with_quantiles(ax, x, mean, q10, q90)
    configure_24h_axis(ax)
    add_stats_box(ax, avg=mean.mean(), peak=mean.max())
    save_plot(fig, "test_output")
    # Verify file created
```

## Assertion Standards

<!-- rule:T-009 -->

- **Use Specific Assertions**: Prefer specific over generic
  ```python
  # ✅ GOOD
  assert result == 42
  assert isinstance(value, str)
  assert len(items) == 5

  # ❌ BAD
  assert result
  assert value
  ```

<!-- rule:T-010 -->

- **Float Comparison**: Use `np.isclose()` for floating-point
  ```python
  # ✅ GOOD
  assert np.isclose(result, expected, rtol=1e-5)

  # ❌ BAD
  assert result == expected  # May fail due to floating-point
  ```

<!-- rule:T-011 -->

- **Array Comparison**: Use `np.all()` or `np.array_equal()`
  ```python
  # ✅ GOOD
  assert np.all(array1 == array2)
  assert np.array_equal(array1, array2)

  # ❌ BAD
  assert array1 == array2  # Ambiguous for arrays
  ```

## Error Handling Tests

<!-- rule:T-012 -->

- **Test Error Cases**: Verify functions raise appropriate errors
  ```python
  def test_invalid_input_raises_value_error():
      """Verify invalid input raises ValueError."""
      with pytest.raises(ValueError, match="invalid.*input"):
          function_with_validation(invalid_input)
  ```

## Logging Tests

Use `caplog` to verify logging:

```python
def test_logs_warning(caplog):
    """Verify warning is logged."""
    with caplog.at_level(logging.WARNING):
        function_that_logs()
    assert "expected warning message" in caplog.text
```

## Mocking Standards

<!-- rule:T-013 -->

- **Use `unittest.mock.patch`**: Mock external dependencies
  ```python
  @patch('module.function_to_mock')
  def test_with_mock(mock_func):
      """Test with mocked dependency."""
      mock_func.return_value = 42
      result = function_under_test()
      mock_func.assert_called_once()
  ```

## Validation

Before committing test changes:

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=scienceplots_toolkit --cov-report=term-missing

# Run visual tests only
uv run pytest tests/test_visual_baselines.py -v

# Run specific test class
uv run pytest tests/test_style.py::TestConfigureMatplotlibStyle -v
```

## Adding New Tests

When adding new functionality:

1. **Create test file** if module doesn't have tests
2. **Add test class** for the new function/class
3. **Write test methods** for:
   - Normal case (expected behavior)
   - Edge cases (boundary conditions)
   - Error cases (invalid input)
4. **Add visual baseline** if function creates plots
5. **Verify coverage** with `pytest-cov`

## Related Documentation

- **[Root AGENTS.md](../AGENTS.md)**: Global mandates
- **[PYTHON_STANDARDS.md](docs/PYTHON_STANDARDS.md)**: Python coding standards
- **[pytest Documentation](https://docs.pytest.org/)**: pytest reference
- **[pytest-mpl Documentation](https://github.com/matplotlib/pytest-mpl)**: Visual testing

## Gotchas

- **Don't Skip Cleanup**: Always close figures, remove temp files
- **Don't Share State**: Tests must be independent
- **Don't Test Implementation**: Test behavior, not internal details
- **Don't Ignore Failures**: All tests must pass before merging
- **Don't Skip Visual Tests**: Visual baselines catch rendering bugs
