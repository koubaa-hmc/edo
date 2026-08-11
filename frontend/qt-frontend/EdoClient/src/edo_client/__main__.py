#!/usr/bin/env python3
"""Allow running as python -m edo_client.

Runs the PyQt application by default (equivalent to: python run.py pyqt)
"""

import sys
from os import path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

# Ensure src is in path
sys.path.insert(0, str(path.join(str(path.dirname(__file__)), "..")))


def main() -> int:
    """Main entry point for python -m edo_client."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    from edo_client.app import EDOApplication

    app = EDOApplication(sys.argv, demo_mode=True)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
