"""
EDO Client - Energy Data Orchestrator Desktop Application

A unified PyQt6/QML application for managing FAIR energy data.
Implements Model-Driven User Interface Development (MDUID) following
the Cameleon Reference Framework.

Project Structure:
    src/edo_client/
    ├── models/          # Data models (platform-independent)
    ├── viewmodels/      # Qt-specific view models for QML binding
    ├── core/            # Business logic, roles, bridges
    └── widgets/         # PyQt widget components

Key Features:
    - Role-based access control (guest_viewer, research_fellow, data_steward, admin)
    - FAIR data lifecycle support (PLAN, COLLECT, PROCESS, PRESERVE, SHARE, REUSE)
    - RO-Crate metadata packaging
    - Multi-platform publication (OEP, Helmholtz KG, etc.)
    - Semantic annotation and expansion

Usage:
    from edo_client import create_app

    app = create_app(demo_mode=True)
    exit_code = app.run()

See PROJECT_OVERVIEW.md for integration architecture details.
"""

__version__ = "0.1.0"
__author__ = "Energy Data Orchestrator Team"

from .app import EDOApplication, create_app, main
from .core.backend_bridge import BackendBridge, get_backend_bridge
from .core.role_registry import RoleRegistry, get_role_registry
from .core.widget_factory import WidgetFactory, get_widget_factory

__all__ = [
    'EDOApplication',
    'create_app',
    'main',
    'BackendBridge',
    'get_backend_bridge',
    'RoleRegistry',
    'get_role_registry',
    'WidgetFactory',
    'get_widget_factory',
]
