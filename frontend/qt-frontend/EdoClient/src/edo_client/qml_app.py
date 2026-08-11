#!/usr/bin/env python3
"""
EDO Client - QML-based Application.

This module provides a QML frontend with Python backend integration.
Use this when you want to edit the UI in Qt Design Studio.
"""

from __future__ import annotations
import sys
import os
import logging
import pathlib

from PyQt6.QtCore import QObject, QUrl, QTimer
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType


def _setup_logging() -> logging.Logger:
    """Configure application logging."""
    log_dir = pathlib.Path.home() / ".edo-client" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    root = logging.getLogger("edo_client.qml")
    root.setLevel(logging.DEBUG)
    
    # Clear existing handlers to avoid duplicates
    root.handlers.clear()
    
    # Console handler
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
    root.addHandler(console)
    
    # File handler
    log_file = log_dir / "qml_app.log"
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    root.addHandler(file_handler)
    
    return root


class QMLApplication(QObject):
    """QML-based EDO Application."""
    
    def __init__(self, demo_mode: bool = True):
        super().__init__()
        self._demo_mode = demo_mode
        self._log = _setup_logging()
        self._engine: QQmlApplicationEngine | None = None
        self._bridge = None
    
    def run(self) -> int:
        """Run the QML application."""
        from .core.backend_bridge import get_backend_bridge
        from .qml_bridge import create_qml_bridge
        
        self._log.info("Starting QML application (demo_mode=%s)", self._demo_mode)
        
        # Create application
        app = QGuiApplication(sys.argv)
        app.setApplicationName("Energy Data Orchestrator")
        app.setApplicationVersion("0.1.0")
        app.setOrganizationName("EDO Team")
        
        # Force non-native style to allow custom Button backgrounds
        # See: https://doc.qt.io/qt-6/qtquickcontrols2-customize.html
        import os
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
        
        # Setup icon - try multiple formats
        icon_paths = [
            pathlib.Path(__file__).parent / "resources" / "edo_icon.icns",  # macOS
            pathlib.Path(__file__).parent / "resources" / "edo_icon_256.png",
            pathlib.Path(__file__).parent / "resources" / "edo_icon_64.png",
        ]
        for icon_path in icon_paths:
            if icon_path.exists():
                app.setWindowIcon(QIcon(str(icon_path)))
                self._log.debug("Loaded icon: %s", icon_path)
                break
        
        # Create QML engine
        self._engine = QQmlApplicationEngine()
        
        # Add QML import paths
        qml_path = pathlib.Path(__file__).parent.parent.parent / "qml"
        if qml_path.exists():
            self._engine.addImportPath(str(qml_path))
            self._log.debug("Added QML import path: %s", qml_path)
        
        # Create and expose bridge
        self._bridge = create_qml_bridge(get_backend_bridge())
        self._engine.rootContext().setContextProperty("pythonBridge", self._bridge)
        
        # Load main QML file
        qml_file = qml_path / "EdoClientContent" / "App.qml"
        if not qml_file.exists():
            self._log.error("QML file not found: %s", qml_file)
            return 1
        
        self._engine.load(QUrl.fromLocalFile(str(qml_file)))
        
        if not self._engine.rootObjects():
            self._log.error("Failed to load QML")
            return -1
        
        self._log.info("QML application loaded successfully")
        
        # Load demo data after delay
        if self._demo_mode:
            QTimer.singleShot(1000, self._load_demo_data)
        
        return app.exec()
    
    def _load_demo_data(self):
        """Load demo data into the QML interface."""
        if not self._bridge:
            return
        
        demo_dataset = {
            "title": "Energy Consumption Timeseries 2025",
            "description": "Hourly energy consumption data for testing",
            "resources": [
                {"name": "consumption_2025.csv", "format": "CSV", "size": "2.4 MB"}
            ]
        }
        
        demo_timeseries = {
            "timestamps": [f"2025-01-{d:02d}T{h:02d}:00" for d in range(1, 4) for h in range(24)],
            "values": [1200 + (h * 50) + (d * 100) for d in range(1, 4) for h in range(24)]
        }
        
        demo_rdf = {
            "uri": "https://openenergyontology.org/resource/EnergyPlant_001",
            "@type": "oeo:EnergyPlant",
            "rdfs:label": "Solar Park Brandenburg"
        }
        
        # Load sequentially
        QTimer.singleShot(0, lambda: self._bridge.loadData(demo_dataset))
        QTimer.singleShot(3000, lambda: self._bridge.loadData(demo_timeseries))
        QTimer.singleShot(6000, lambda: self._bridge.loadData(demo_rdf))
        
        self._log.debug("Demo data scheduled")


def create_app(demo_mode: bool = True) -> QMLApplication:
    """Create QML application instance."""
    return QMLApplication(demo_mode=demo_mode)


def main() -> int:
    """Main entry point for QML application."""
    app = create_app(demo_mode=False)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
