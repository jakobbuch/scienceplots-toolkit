"""CLI entry point for scienceplots_toolkit.

This module enables running the CLI directly with:
    python -m scienceplots_toolkit.cli [args]

Or importing and using the orchestrator classes:
    from scienceplots_toolkit.cli import BaseOrchestrator, plot_function
"""

if __name__ == "__main__":
    print("SciencePlots Toolkit CLI")
    print("=" * 40)
    print("\nThis module provides CLI infrastructure for batch plotting.")
    print("Use the BaseOrchestrator class to create your own orchestrator:")
    print("\nExample:")
    print("    from scienceplots_toolkit.cli import BaseOrchestrator, plot_function")
    print("")
    print("    @plot_function(name='my_plot', description='My custom plot')")
    print("    def my_plot_func(args):")
    print("        # Your plotting code here")
    print("        pass")
    print("")
    print("    class MyOrchestrator(BaseOrchestrator):")
    print("        def run_plots(self, args):")
    print("            # Define which plots to run")
    print("            self.run_plot('my_plot', args)")
    print("")
    print("    if __name__ == '__main__':")
    print("        orchestrator = MyOrchestrator()")
    print("        orchestrator.main()")
    print("\n" + "=" * 40)
    print("\nRun 'python -m your_script.cli --help' to see available options.")
