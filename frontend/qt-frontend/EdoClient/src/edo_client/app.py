#!/usr/bin/env python3
"""
Application entry point with async support.

This module provides:
- QApplication subclass with lifecycle management
- qasync integration for asyncio event loop
- Global stylesheet application
- Demo data generation for testing
"""

from __future__ import annotations

import asyncio
import logging
import logging.handlers
import pathlib
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QApplication

try:
    from qasync import QEventLoop
except ImportError:
    QEventLoop = None  # type: ignore

from .widgets.main_window import MainWindow


def _setup_logging() -> logging.Logger:
    """Configure rotating file + console logging and return the app logger."""
    log_dir = pathlib.Path.home() / ".edo-client" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "edo-client.log"

    root = logging.getLogger("edo_client")
    root.setLevel(logging.DEBUG)

    # Rotate: 5 MB per file, keep 3 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))

    root.addHandler(file_handler)
    root.addHandler(console_handler)
    root.debug("Logging initialised — log file: %s", log_path)
    return root


def _load_app_icon() -> QIcon | None:
    """Load the application icon from the bundled resources."""
    res_dir = pathlib.Path(__file__).parent / "resources"

    # macOS / Linux: prefer the ICNS bundle
    icns_path = res_dir / "edo.icns"
    if icns_path.exists():
        icon = QIcon(str(icns_path))
        if not icon.isNull():
            return icon

    # Windows / fallback: square PNG
    png_path = res_dir / "edo_icon_64.png"
    if png_path.exists():
        pixmap = QPixmap(str(png_path))
        if not pixmap.isNull():
            return QIcon(pixmap)

    return None


class EDOApplication(QApplication):
    """
    Main application class with async support and lifecycle management.
    """

    def __init__(self, args: list[str], demo_mode: bool = True) -> None:
        super().__init__(args)
        self._demo_mode = demo_mode
        self._main_window: MainWindow | None = None
        self._setup_application()

    def _setup_application(self) -> None:
        """Configure application-wide settings."""
        self.setApplicationName("Energy Data Orchestrator")
        self.setApplicationVersion("0.1.0")
        self.setOrganizationName("Energy Data Orchestrator Team")
        self._log = _setup_logging()
        self._log.debug("EDOApplication starting (demo_mode=%s)", self._demo_mode)
        self._apply_icon()

        font = QFont()
        font.setPointSize(11)
        font.setFamilies(["Arial", "Helvetica Neue", "Segoe UI", "Helvetica", "sans-serif"])
        self.setFont(font)
        self._apply_stylesheet()

    def _apply_icon(self) -> None:
        """Set the application icon (shown in macOS dock, taskbar, and window chrome)."""
        icon = _load_app_icon()
        if icon is not None:
            self.setWindowIcon(icon)
            self._log.debug("Application icon loaded")
        else:
            self._log.warning("Application icon could not be loaded")

    def _apply_stylesheet(self) -> None:
        """Apply the application stylesheet using HMC corporate colours."""
        self.setStyleSheet("""
        QMainWindow { background-color: #ffffff; }
        QPushButton {
            background-color: #00305E; color: white; border: none;
            border-radius: 4px; padding: 8px 16px; font-weight: 500;
        }
        QPushButton:hover { background-color: #004B87; }
        QLineEdit, QTextEdit {
            border: 1px solid #ced4da; border-radius: 4px; padding: 6px;
            background-color: #ffffff; color: #212529;
        }
        QTableWidget, QTreeWidget { 
            border: 1px solid #dee2e6; border-radius: 4px; 
            background-color: #ffffff; 
        }
        QStatusBar { background-color: #f8f9fa; border-top: 1px solid #dee2e6; color: #495057; }
        """)

    def run(self) -> int:
        """Run the application."""
        self._log.debug("Creating asyncio event loop")
        if QEventLoop:
            loop = QEventLoop(self)
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            self._log.debug("Instantiating MainWindow")
            self._main_window = MainWindow()
            self._main_window.show()
            self._main_window.action_triggered.connect(self._on_action_triggered)
            self._main_window.role_changed.connect(self._on_role_changed)

            if self._demo_mode:
                self._log.debug("Scheduling demo data load at t=500ms")
                QTimer.singleShot(500, self._load_demo_data)

            self._log.info("EDOApplication running")
            with loop:
                return loop.run_forever()
        finally:
            self._log.debug("Closing event loop")
            loop.close()

    def _load_demo_data(self) -> None:
        """Load demo data into the main window."""
        log = logging.getLogger("edo_client.app")
        if not self._main_window:
            return

        log.debug("Loading demo data")
        demo_dataset = {
            "title": "Energy Consumption Timeseries 2025",
            "description": "Hourly energy consumption data for testing the EDO client",
            "resources": [
                {"name": "consumption_2025.csv", "format": "CSV", "size": "2.4 MB"},
                {"name": "metadata.json", "format": "JSON", "size": "12 KB"}
            ],
        }
        demo_timeseries = {
            "timestamps": [f"2025-01-{d:02d}T{h:02d}:00" for d in range(1, 4) for h in range(24)],
            "values": [1200 + (h * 50) + (d * 100) for d in range(1, 4) for h in range(24)],
        }
        demo_rdf = {
            "uri": "https://openenergyontology.org/resource/EnergyPlant_001",
            "@type": "oeo:EnergyPlant",
            "rdfs:label": "Solar Park Brandenburg",
            "location": "Brandenburg, Germany",
            "capacity_mw": 150
        }

        QTimer.singleShot(1000, lambda: self._main_window.load_data(demo_dataset))
        QTimer.singleShot(2000, lambda: self._main_window.load_data(demo_timeseries))
        QTimer.singleShot(3000, lambda: self._main_window.load_data(demo_rdf))
        log.debug("Demo data load scheduled at t=1s, 2s, 3s")

    def _on_role_changed(self, role_ids: list[str]) -> None:
        log = logging.getLogger("edo_client.app")
        log.info("Role changed → %s", role_ids)

    def _on_action_triggered(self, action_id: str, params: dict) -> None:
        log = logging.getLogger("edo_client.app")
        log.info("Action triggered: action_id=%r params=%r", action_id, params)


def create_app(demo_mode: bool = True) -> EDOApplication:
    return EDOApplication(sys.argv, demo_mode=demo_mode)


def main() -> int:
    app = create_app(demo_mode=False)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
