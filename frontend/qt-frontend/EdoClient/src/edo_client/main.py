#!/usr/bin/env python3
"""
Energy Data Orchestrator - Main Entry Point.

Desktop Application with:
- Dynamic role-based layout construction
- On-the-fly data-driven widget deployment
- Decoupled backend action bridge
"""

import sys


def main() -> int:
    """Main entry point."""
    # Import here to ensure all dependencies are available
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
    except ImportError as e:
        print(
            f"Error: PyQt6 is required but not installed.\n"
            f"Install with: pip install PyQt6\n"
            f"Original error: {e}",
            file=sys.stderr,
        )
        return 1

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Run the application
    try:
        from .app import main as app_main
    except ImportError:
        from app import main as app_main

    return app_main()


if __name__ == "__main__":
    sys.exit(main())
