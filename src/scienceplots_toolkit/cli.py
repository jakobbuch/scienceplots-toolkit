"""CLI infrastructure for batch plotting with orchestration support.

This module provides the BaseOrchestrator abstract base class and CLI tools
for managing and executing multiple plot generation functions.

Example usage:
    >>> from scienceplots_toolkit.cli import BaseOrchestrator, plot_function
    >>>
    >>> class MyOrchestrator(BaseOrchestrator):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.register_plot(
    ...             "daily_profile",
    ...             self.plot_daily,
    ...             "Daily load profile"
    ...         )
    ...
    ...     def plot_daily(self, args):
    ...         print("Plotting daily profile")
    ...
    ...     def run_plots(self, args):
    ...         self.list_plots()
    >>>
    >>> if __name__ == "__main__":
    ...     orchestrator = MyOrchestrator()
    ...     orchestrator.main()
"""

import argparse
import functools
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Protocol

logger = logging.getLogger(__name__)

# Registry for plot functions decorated with @plot_function
_plot_registry: list[dict[str, Any]] = []


def plot_function(
    name: str | None = None,
    description: str = "",
    tags: list[str] | None = None,
) -> Callable:
    """Decorator to register a function as a plot generator.

    Stores function metadata for later registration with an orchestrator.

    Args:
        name: Plot name. If None, uses the function's __name__.
        description: Human-readable description of the plot.
        tags: Optional list of tags for categorization.

    Returns:
        Decorated function with metadata attached.

    Example:
        >>> @plot_function(name="load_profile", description="Daily load curve")
        ... def plot_load(args):
        ...     pass
    """

    def decorator(func: Callable) -> Callable:
        plot_name = name if name is not None else getattr(func, "__name__", "unknown")
        metadata = {
            "name": plot_name,
            "func": func,
            "description": description,
            "tags": tags or [],
        }
        _plot_registry.append(metadata)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Attach metadata to the function for inspection
        setattr(wrapper, "_plot_metadata", metadata)
        return wrapper

    return decorator


class BaseOrchestrator(ABC):
    """Abstract base class for plot orchestration and CLI management.

    Provides infrastructure for registering, listing, and executing plot
    functions with common CLI arguments (--latex, --output-dir, --years, --house).

    Subclasses must implement the run_plots() method to define their
    plot execution logic.

    Attributes:
        plots: Dictionary mapping plot names to their metadata.
        args: Parsed command-line arguments (available after main() is called).

    Example:
        >>> class MyOrchestrator(BaseOrchestrator):
        ...     def run_plots(self, args):
        ...         if "daily" in args.only or not args.only:
        ...             self.run_plot("daily", args)
        >>>
        >>> orchestrator = MyOrchestrator()
        >>> orchestrator.main()
    """

    def __init__(self) -> None:
        """Initialize the orchestrator with empty plot registry."""
        self.plots: dict[str, dict[str, Any]] = {}
        self.args: argparse.Namespace | None = None

    def register_plot(
        self, name: str, func: Callable, description: str = "", tags: list[str] | None = None
    ) -> None:
        """Register a plot function for CLI execution.

        Args:
            name: Unique identifier for the plot.
            func: Callable that accepts (args) namespace parameter.
            description: Human-readable description for --list output.
            tags: Optional tags for filtering/categorization.

        Example:
            >>> orchestrator = BaseOrchestrator()
            >>> orchestrator.register_plot(
            ...     "daily",
            ...     my_plot_func,
            ...     "Daily load profile",
            ...     tags=["energy", "daily"]
            ... )
        """
        self.plots[name] = {
            "func": func,
            "description": description,
            "tags": tags or [],
        }
        logger.debug("Registered plot: %s", name)

    def register_from_decorator(self) -> None:
        """Register all functions decorated with @plot_function.

        Automatically registers all functions from the global _plot_registry.
        Useful for bulk registration without manual calls to register_plot().

        Example:
            >>> orchestrator = MyOrchestrator()
            >>> orchestrator.register_from_decorator()  # Registers all @plot_function decorated funcs
        """
        for metadata in _plot_registry:
            self.register_plot(
                name=metadata["name"],
                func=metadata["func"],
                description=metadata["description"],
                tags=metadata["tags"],
            )
        logger.debug("Registered %d plots from decorator registry", len(_plot_registry))

    def list_plots(self) -> None:
        """Print all registered plots with descriptions and tags.

        Outputs a formatted list to stdout showing:
        - Plot name
        - Description
        - Tags (if any)

        Example:
            >>> orchestrator = MyOrchestrator()
            >>> orchestrator.register_plot("daily", func, "Daily profile", ["energy"])
            >>> orchestrator.list_plots()
            Registered plots:
              - daily: Daily profile [energy]
        """
        if not self.plots:
            print("No plots registered.")
            return

        print("Registered plots:")
        for name, metadata in sorted(self.plots.items()):
            desc = metadata["description"] or "No description"
            tags = metadata["tags"]
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  - {name}: {desc}{tag_str}")

    def run_plot(self, name: str, args: argparse.Namespace) -> None:
        """Execute a single registered plot function.

        Args:
            name: Name of the plot to run (must be registered).
            args: Command-line arguments namespace to pass to the plot function.

        Raises:
            KeyError: If plot name is not registered.

        Example:
            >>> orchestrator = MyOrchestrator()
            >>> orchestrator.register_plot("daily", my_func)
            >>> orchestrator.run_plot("daily", args)
        """
        if name not in self.plots:
            raise KeyError(f"Plot '{name}' not registered. Available: {list(self.plots.keys())}")

        logger.info("Running plot: %s", name)
        self.plots[name]["func"](args)

    def run_plots(self, args: argparse.Namespace) -> None:
        """Execute plot generation logic.

        **MUST BE IMPLEMENTED BY SUBCLASSES**

        This method defines which plots to run and in what order.
        Typically checks args.only and args.skip to filter plots.

        Args:
            args: Parsed command-line arguments with attributes:
                - only: List of plot names to run exclusively
                - skip: List of plot names to skip
                - latex: Whether to use LaTeX rendering
                - output_dir: Output directory path
                - years: List of years to process
                - house: House/building identifier

        Example:
            >>> def run_plots(self, args):
            ...     plots_to_run = args.only or list(self.plots.keys())
            ...     for name in plots_to_run:
            ...         if name not in args.skip:
            ...             self.run_plot(name, args)
        """
        raise NotImplementedError("Subclasses must implement run_plots()")

    def _parse_args(self) -> argparse.Namespace:
        """Parse command-line arguments.

        Sets up standard arguments:
        - --latex: Enable LaTeX rendering
        - --output-dir: Output directory for plots
        - --years: Years to process (comma-separated)
        - --house: House/building identifier
        - --list: List all registered plots
        - --only: Run only specified plots (comma-separated)
        - --skip: Skip specified plots (comma-separated)

        Returns:
            Parsed arguments namespace.
        """
        parser = argparse.ArgumentParser(
            description="Batch plot generator with SciencePlots toolkit",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Output configuration
        parser.add_argument(
            "--latex",
            action="store_true",
            help="Use LaTeX rendering (requires TeX Live installation)",
        )
        parser.add_argument(
            "--output-dir",
            type=Path,
            default=Path("output"),
            help="Output directory for generated plots (default: output)",
        )

        # Data filtering
        parser.add_argument(
            "--years",
            type=str,
            default="",
            help="Years to process (comma-separated, e.g., '2020,2021,2022')",
        )
        parser.add_argument(
            "--house",
            type=str,
            default="",
            help="House or building identifier",
        )

        # Plot selection
        parser.add_argument(
            "--list",
            action="store_true",
            dest="list_plots",
            help="List all registered plots and exit",
        )
        parser.add_argument(
            "--only",
            type=str,
            default="",
            help="Run only specified plots (comma-separated names)",
        )
        parser.add_argument(
            "--skip",
            type=str,
            default="",
            help="Skip specified plots (comma-separated names)",
        )

        # Verbosity
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            default=0,
            help="Increase verbosity (-v for INFO, -vv for DEBUG)",
        )

        return parser.parse_args()

    def _setup_logging(self, verbose: int) -> None:
        """Configure logging based on verbosity level.

        Args:
            verbose: Verbosity level (0=WARNING, 1=INFO, 2+=DEBUG)
        """
        level = logging.WARNING
        if verbose == 1:
            level = logging.INFO
        elif verbose >= 2:
            level = logging.DEBUG

        logging.basicConfig(
            level=level,
            format="%(levelname)s: %(message)s",
        )

    def _process_args(self, args: argparse.Namespace) -> None:
        """Post-process parsed arguments for convenience.

        Converts comma-separated strings to lists for --years, --only, --skip.

        Args:
            args: Parsed arguments to modify in-place.
        """
        # Parse comma-separated values
        if args.years:
            args.years_list = [y.strip() for y in args.years.split(",")]
        else:
            args.years_list = []

        if args.only:
            args.only_list = [p.strip() for p in args.only.split(",")]
        else:
            args.only_list = []

        if args.skip:
            args.skip_list = [p.strip() for p in args.skip.split(",")]
        else:
            args.skip_list = []

    def main(self) -> None:
        """Main CLI entry point.

        Parses arguments, sets up logging, and executes the orchestration.
        Call this method to enable CLI functionality.

        Example:
            >>> if __name__ == "__main__":
            ...     orchestrator = MyOrchestrator()
            ...     orchestrator.main()

        CLI usage:
            # List all available plots
            python -m scienceplots_toolkit.cli --list

            # Run all plots
            python -m scienceplots_toolkit.cli

            # Run specific plots only
            python -m scienceplots_toolkit.cli --only daily,monthly

            # Skip certain plots
            python -m scienceplots_toolkit.cli --skip test,debug

            # With LaTeX and custom output
            python -m scienceplots_toolkit.cli --latex --output-dir plots/2024

            # Filter by years and house
            python -m scienceplots_toolkit.cli --years 2020,2021 --house B123
        """
        args = self._parse_args()
        self._setup_logging(args.verbose)
        self._process_args(args)
        self.args = args

        # Handle --list
        if args.list_plots:
            self.list_plots()
            return

        # Run the plots
        logger.info("Starting batch plot generation")
        logger.info("Output directory: %s", args.output_dir)
        logger.info("LaTeX rendering: %s", "enabled" if args.latex else "disabled")

        if args.years_list:
            logger.info("Years: %s", ", ".join(args.years_list))
        if args.house:
            logger.info("House: %s", args.house)

        self.run_plots(args)
        logger.info("Batch plot generation complete")


def create_cli_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for batch-plot command.

    This function provides the parser setup separately for testing or
    custom CLI implementations.

    Returns:
        Configured ArgumentParser instance.

    Example:
        >>> parser = create_cli_parser()
        >>> args = parser.parse_args(["--list"])
    """
    parser = argparse.ArgumentParser(
        prog="batch-plot",
        description="Batch plot generator with SciencePlots toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  batch-plot --list                    List all registered plots
  batch-plot                           Run all plots
  batch-plot --only daily,monthly      Run specific plots
  batch-plot --skip test               Skip certain plots
  batch-plot --latex --output-dir out  Use LaTeX, custom output dir
  batch-plot --years 2020,2021         Filter by years
  batch-plot --house B123              Filter by building
        """,
    )

    # Output configuration
    parser.add_argument(
        "--latex",
        action="store_true",
        help="Use LaTeX rendering (requires TeX Live installation)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Output directory for generated plots (default: output)",
    )

    # Data filtering
    parser.add_argument(
        "--years",
        type=str,
        default="",
        help="Years to process (comma-separated, e.g., '2020,2021,2022')",
    )
    parser.add_argument(
        "--house",
        type=str,
        default="",
        help="House or building identifier",
    )

    # Plot selection
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_plots",
        help="List all registered plots and exit",
    )
    parser.add_argument(
        "--only",
        type=str,
        default="",
        help="Run only specified plots (comma-separated names)",
    )
    parser.add_argument(
        "--skip",
        type=str,
        default="",
        help="Skip specified plots (comma-separated names)",
    )

    # Verbosity
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (-v for INFO, -vv for DEBUG)",
    )

    return parser
