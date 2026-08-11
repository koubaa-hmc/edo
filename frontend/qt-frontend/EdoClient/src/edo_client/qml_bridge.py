"""
QML Bridge - Connects Python backend to QML frontend.

This module provides the bridge between PyQt6 and QML components,
allowing data exchange and signal/slot connections.
"""

from __future__ import annotations

from typing import Any, Dict

from PyQt6.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot


class QMLBridge(QObject):
    """
    Bridge object exposed to QML for Python-QML communication.

    Signals emitted from Python can be connected to QML functions,
    and QML signals can trigger Python slots.
    """

    # Signals to QML
    dataLoaded = pyqtSignal(QVariant)
    statusMessage = pyqtSignal(str)
    roleChanged = pyqtSignal(str)
    actionCompleted = pyqtSignal(str, QVariant)

    def __init__(self, backend_bridge=None, parent=None):
        super().__init__(parent)
        self._backend_bridge = backend_bridge
        self._current_role = "data_steward"
        self._main_window = None

    def set_main_window(self, window):
        """Set reference to main window for callbacks."""
        self._main_window = window

    @pyqtSlot(str)
    def setRole(self, role_id: str):
        """Change user role (called from QML)."""
        self._current_role = role_id
        self.roleChanged.emit(role_id)

        if self._main_window:
            self._main_window.set_user_roles([role_id])

        self.statusMessage.emit(f"Role changed to: {role_id}")

    @pyqtSlot()
    def getCurrentRole(self) -> str:
        """Get current role ID."""
        return self._current_role

    @pyqtSlot(QVariant)
    def loadData(self, data: Any):
        """Load data into the application (called from QML or Python)."""
        self.dataLoaded.emit(data)

        if self._main_window:
            self._main_window.load_data(data)

    @pyqtSlot(str, QVariant)
    async def triggerAction(self, action_id: str, params: Dict[str, Any]):
        """Trigger a backend action (called from QML)."""
        if not self._backend_bridge:
            self.statusMessage.emit("Backend bridge not available")
            return

        self.statusMessage.emit(f"Executing: {action_id}...")

        result = await self._backend_bridge.execute(action_id, **params)

        if result.is_success:
            self.statusMessage.emit(f"✓ {result.message}")
            if result.data is not None:
                self.dataLoaded.emit(result.data)
            self.actionCompleted.emit(action_id, result.data or {})
        else:
            self.statusMessage.emit(f"✗ {result.error}")

    @pyqtSlot()
    def newWorkspace(self):
        """Create new workspace (called from QML)."""
        self.statusMessage.emit("New workspace created")
        if self._main_window:
            self._main_window._container.clear()

    @pyqtSlot(QVariant)
    def displayData(self, data: Any):
        """Display data in the content area."""
        self.loadData(data)

    @pyqtSlot(str)
    def showStatus(self, message: str):
        """Show status message in QML."""
        self.statusMessage.emit(message)


def create_qml_bridge(backend_bridge=None):
    """Create and configure a QML bridge instance."""
    return QMLBridge(backend_bridge=backend_bridge)
