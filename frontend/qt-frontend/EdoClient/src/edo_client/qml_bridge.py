"""
QML Bridge - Connects Python backend to QML frontend.

This module provides the bridge between PyQt6 and QML components,
allowing data exchange and signal/slot connections.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from PyQt6.QtCore import QMetaObject, QObject, Qt, QTimer, QVariant, pyqtSignal, pyqtSlot, Q_ARG


class QMLBridge(QObject):
    """
    Bridge object exposed to QML for Python-QML communication.

    Signals emitted from Python can be connected to QML functions,
    and QML signals can trigger Python slots.
    """

    # Signals to QML
    dataLoaded = pyqtSignal(QVariant)  # noqa: N815
    statusMessage = pyqtSignal(str)  # noqa: N815
    roleChanged = pyqtSignal(str)  # noqa: N815
    actionCompleted = pyqtSignal(str, QVariant)  # noqa: N815

    def __init__(self, backend_bridge=None, parent=None):
        super().__init__(parent)
        self._backend_bridge = backend_bridge
        self._current_role = "data_steward"
        self._main_window = None

    def set_main_window(self, window):
        """Set reference to main window for callbacks."""
        self._main_window = window

    @pyqtSlot(str)
    def setRole(self, role_id: str):  # noqa: N802
        """Change user role (called from QML)."""
        self._current_role = role_id
        self.roleChanged.emit(role_id)

        if self._main_window:
            self._main_window.set_user_roles([role_id])

        self.statusMessage.emit(f"Role changed to: {role_id}")

    @pyqtSlot()
    def getCurrentRole(self) -> str:  # noqa: N802
        """Get current role ID."""
        return self._current_role

    @pyqtSlot(QVariant)
    def loadData(self, data: Any):  # noqa: N802
        """Load data into the application (called from QML or Python)."""
        self.dataLoaded.emit(data)

        if self._main_window:
            self._main_window.load_data(data)

    @pyqtSlot(str, QVariant)
    def triggerAction(self, action_id: str, params: QVariant):  # noqa: N802
        """Trigger a backend action (called from QML)."""
        log = logging.getLogger("edo_client")
        
        # Convert QJSValue/QVariant to Python dict
        params_dict = {}
        if params is not None:
            try:
                # Handle QJSValue or QVariant wrapping a QJSValue
                if hasattr(params, 'toVariant'):
                    params = params.toVariant()
                if isinstance(params, dict):
                    params_dict = params
                elif hasattr(params, 'property'):
                    # QJSValue object - extract properties
                    for key in ['actionId', 'params']:
                        val = params.property(key)
                        if val and hasattr(val, 'toVariant'):
                            params_dict[key] = val.toVariant()
            except Exception as e:
                log.warning("⚠️ Failed to convert params: %s", e)
        
        log.info("🔵 QML Action triggered: action_id=%r params=%r", action_id, params_dict)

        if not self._backend_bridge:
            log.warning("⚠️ Backend bridge not available")
            self.statusMessage.emit("Backend bridge not available")
            return

        self.statusMessage.emit(f"Executing: {action_id}...")

        # Schedule async execution via event loop
        loop = asyncio.get_event_loop()
        if loop and loop.is_running():
            asyncio.ensure_future(self._execute_action_async(action_id, params_dict))
        else:
            # Fallback: run synchronously if no event loop
            QTimer.singleShot(0, lambda: self._execute_action_sync(action_id, params_dict))

    async def _execute_action_async(self, action_id: str, params: dict[str, Any]) -> None:
        """Execute action asynchronously."""
        result = await self._backend_bridge.execute(action_id, **params)
        self._handle_action_result(action_id, result)

    def _execute_action_sync(self, action_id: str, params: dict[str, Any]) -> None:
        """Execute action synchronously (fallback)."""
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self._backend_bridge.execute(action_id, **params))
            self._handle_action_result(action_id, result)
        finally:
            loop.close()

    def _handle_action_result(self, action_id: str, result) -> None:
        """Handle action result on main thread."""
        log = logging.getLogger("edo_client")
        if result.is_success:
            log.info("✅ Action completed: %s - %s", action_id, result.message)
            data = result.data or {}
            QMetaObject.invokeMethod(
                self, "_emitSuccess", Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, action_id),
                Q_ARG(QVariant, data),
                Q_ARG(str, result.message)
            )
        else:
            log.error("❌ Action failed: %s - %s", action_id, result.error)
            QMetaObject.invokeMethod(
                self, "_emitError", Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, action_id),
                Q_ARG(str, result.error)
            )

    @pyqtSlot(str, QVariant, str)
    def _emitSuccess(self, action_id: str, data: Any, message: str) -> None:
        """Emit success signals (thread-safe)."""
        self.statusMessage.emit(f"✓ {message}")
        if data is not None:
            self.dataLoaded.emit(data)
        self.actionCompleted.emit(action_id, data)

    @pyqtSlot(str, str)
    def _emitError(self, action_id: str, error: str) -> None:
        """Emit error signal (thread-safe)."""
        self.statusMessage.emit(f"✗ {error}")

    @pyqtSlot()
    def newWorkspace(self):  # noqa: N802
        """Create new workspace (called from QML)."""
        self.statusMessage.emit("New workspace created")
        if self._main_window:
            self._main_window._container.clear()

    @pyqtSlot(QVariant)
    def displayData(self, data: Any):  # noqa: N802
        """Display data in the content area."""
        self.loadData(data)

    @pyqtSlot(str)
    def showStatus(self, message: str):  # noqa: N802
        """Show status message in QML."""
        self.statusMessage.emit(message)


def create_qml_bridge(backend_bridge=None):
    """Create and configure a QML bridge instance."""
    return QMLBridge(backend_bridge=backend_bridge)
