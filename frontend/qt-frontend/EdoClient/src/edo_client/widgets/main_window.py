"""Main Window - Central container assembling dynamic components."""

from __future__ import annotations
import asyncio
import os as _os
from typing import Any
from PyQt6.QtWidgets import QMainWindow, QWidget, QMenuBar, QStatusBar, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QAction

from ..core.role_registry import RoleRegistry, RolePolicy, Permission, get_role_registry
from ..core.widget_factory import WidgetFactory, get_widget_factory
from ..core.backend_bridge import BackendBridge, get_backend_bridge
from .role_aware_container import RoleAwareContainer


class MainWindow(QMainWindow):
    """Main application window with dynamic role-based UI construction."""

    role_changed = pyqtSignal(list)
    data_selected = pyqtSignal(object)
    action_triggered = pyqtSignal(str, dict)

    def __init__(
        self,
        role_registry: RoleRegistry | None = None,
        widget_factory: WidgetFactory | None = None,
        backend_bridge: BackendBridge | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._role_registry = role_registry or get_role_registry()
        self._widget_factory = widget_factory or get_widget_factory()
        self._backend_bridge = backend_bridge or get_backend_bridge()
        # Development role override: set EDO_ROLE env var to any built-in role
        dev_role = _os.environ.get("EDO_ROLE", "data_steward").strip()
        self._current_roles: list[str] = [dev_role] if dev_role else ["research_fellow"]
        self._current_policy: RolePolicy | None = None
        self._menu_actions: list[QAction] = []
        self._ingestion_menu_actions: list[QAction] = []
        self._setup_window()
        self._create_menu_bar()
        self._update_ui_for_role()
        self.role_changed.connect(self._on_role_changed)
        self.data_selected.connect(self._on_data_selected)

    def _setup_window(self) -> None:
        self.setWindowTitle("Energy Data Orchestrator")
        self.setMinimumSize(1200, 800)
        self._container = RoleAwareContainer(
            role_policy=self._current_policy,
            widget_factory=self._widget_factory,
            backend_bridge=self._backend_bridge,
        )
        self.setCentralWidget(self._container)
        self._container.action_requested.connect(self._on_action_requested)
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("Ready")

    def _create_menu_bar(self) -> None:
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        self._add_menu_action(file_menu, "&New Workspace", "workspace.new")
        file_menu.addSeparator()
        self._add_menu_action(file_menu, "E&xit", "app.exit", shortcut="Ctrl+Q")
        
        edit_menu = menubar.addMenu("&Edit")
        self._add_menu_action(edit_menu, "&Undo", "edit.undo", shortcut="Ctrl+Z")
        
        self._view_menu = menubar.addMenu("&View")
        
        data_menu = menubar.addMenu("&Data")
        self._add_menu_action(data_menu, "&Import Dataset", "data.import")
        self._add_menu_action(data_menu, "&Validate", "data.validate")
        
        # B0 Ingestion menu - Data Steward access
        self._ingestion_menu = menubar.addMenu("&Ingestion")
        self._oep_submenu = self._ingestion_menu.addMenu("&OEP (Open Energy Platform)")
        self._add_menu_action(self._oep_submenu, "&Get Metadata…", "ingestion.oep.get_metadata", is_ingestion=True)
        self._oep_submenu.addSeparator()
        self._add_menu_action(self._oep_submenu, "&Fetch Data", "ingestion.oep.fetch", is_ingestion=True)
        self._add_menu_action(self._oep_submenu, "&Preprocess", "ingestion.oep.preprocess", is_ingestion=True)
        self._add_menu_action(self._oep_submenu, "&Merge into Graph", "ingestion.oep.merge", is_ingestion=True)
        self._ingestion_menu.addSeparator()
        self._hkg_submenu = self._ingestion_menu.addMenu("&HKG (Helmholtz KG)")
        self._add_menu_action(self._hkg_submenu, "&Run Ingestion", "ingestion.hkg.run", is_ingestion=True)
        self._ingestion_menu.addSeparator()
        self._add_menu_action(self._ingestion_menu, "&Workflow Status", "ingestion.workflow.status", is_ingestion=True)
        
        semantic_menu = menubar.addMenu("&Semantic")
        self._add_menu_action(semantic_menu, "&Expand", "semantic.expand")
        self._add_menu_action(semantic_menu, "&Annotate", "semantic.annotate")
        
        help_menu = menubar.addMenu("&Help")
        self._add_menu_action(help_menu, "&About", "help.about")

    def _add_menu_action(self, menu: Any, text: str, action_id: str, shortcut: str | None = None, is_ingestion: bool = False) -> QAction:
        action = QAction(text, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.setData(action_id)
        action.triggered.connect(lambda: self._on_menu_action_triggered(action_id))
        menu.addAction(action)
        if is_ingestion:
            self._ingestion_menu_actions.append(action)
        else:
            self._menu_actions.append(action)
        return action

    def set_user_roles(self, role_ids: list[str]) -> None:
        if not role_ids:
            role_ids = [self._role_registry.default_role or "guest_viewer"]
        self._current_roles = role_ids
        self._current_policy = self._role_registry.get_effective_policy(role_ids)
        self.role_changed.emit(role_ids)
        self._status_bar.showMessage(f"Active role: {self._current_policy.display_name}")

    def _update_ui_for_role(self) -> None:
        if not self._current_policy:
            self._current_policy = self._role_registry.get_effective_policy(self._current_roles)
        self._update_menu_visibility()
        self._container.set_policy(self._current_policy)
        # Update container policy reference
        self._container._policy = self._current_policy

    def _update_menu_visibility(self) -> None:
        policy = self._current_policy
        if not policy:
            return
        
        # Standard menu permissions
        permission_map: dict[str, Permission] = {
            "data.import": Permission.IMPORT_DATASETS,
            "data.validate": Permission.RUN_VALIDATION,
            "semantic.expand": Permission.RUN_SEMANTIC_EXPANSION,
            "semantic.annotate": Permission.ANNOTATE_RESOURCES,
        }
        for action in self._menu_actions:
            action_id = action.data()
            if action_id in permission_map:
                required = permission_map[action_id]
                visible = policy.has_permission(required)
                action.setVisible(visible)
        
        # Ingestion menu visibility (Data Steward workflow)
        ingestion_permission_map: dict[str, Permission] = {
            "ingestion.oep.get_metadata": Permission.RUN_INGESTION_OEP,
            "ingestion.oep.fetch": Permission.RUN_INGESTION_OEP,
            "ingestion.oep.preprocess": Permission.RUN_INGESTION_OEP,
            "ingestion.oep.merge": Permission.RUN_INGESTION_OEP,
            "ingestion.hkg.run": Permission.RUN_INGESTION_HKG,
            "ingestion.workflow.status": Permission.ACCESS_INGESTION_WORKFLOW,
        }
        has_ingestion_access = any(
            policy.has_permission(perm) for perm in [
                Permission.RUN_INGESTION_OEP,
                Permission.RUN_INGESTION_HKG,
                Permission.ACCESS_INGESTION_WORKFLOW,
            ]
        )
        self._ingestion_menu.setVisible(has_ingestion_access)
        
        for action in self._ingestion_menu_actions:
            action_id = action.data()
            if action_id in ingestion_permission_map:
                required = ingestion_permission_map[action_id]
                visible = policy.has_permission(required)
                action.setVisible(visible)

    def load_data(self, data: Any) -> None:
        self._selected_data = data
        self.data_selected.emit(data)

    @pyqtSlot(list)
    def _on_role_changed(self, role_ids: list[str]) -> None:
        self._update_ui_for_role()

    @pyqtSlot(object)
    def _on_data_selected(self, data: Any) -> None:
        self._container.display_data(data)
        self._status_bar.showMessage(f"Data loaded: {type(data).__name__}")

    @pyqtSlot(str, dict)
    def _on_action_requested(self, action_id: str, params: dict) -> None:
        self.action_triggered.emit(action_id, params)
        self._execute_action(action_id, params)

    def _on_menu_action_triggered(self, action_id: str) -> None:
        if action_id == "app.exit":
            self.close()
        elif action_id == "help.about":
            QMessageBox.about(self, "About Energy Data Orchestrator", "Energy Data Orchestrator v0.1.0\n\nDesktop Application\n\nBuilt with PyQt6")
        elif action_id == "ingestion.oep.get_metadata":
            table_name, ok = QInputDialog.getText(
                self, "Get OEP Metadata", "Table name:"
            )
            if ok and table_name.strip():
                self._schedule_async_action(action_id, {"table_name": table_name.strip()})
        else:
            self._schedule_async_action(action_id, {})

    def _schedule_async_action(self, action_id: str, params: dict[str, Any]) -> None:
        QTimer.singleShot(0, lambda: asyncio.create_task(self._execute_action(action_id, params)))

    async def _execute_action(self, action_id: str, params: dict[str, Any]) -> None:
        spec = self._backend_bridge.get_action(action_id)
        if not spec:
            self._status_bar.showMessage(f"Unknown action: {action_id}")
            return
        self._status_bar.showMessage(f"Executing: {spec.display_name}...")
        result = await self._backend_bridge.execute(action_id, **params)
        if result.is_success:
            self._status_bar.showMessage(f"✓ {spec.display_name} completed")
            if result.data is not None:
                self._container.display_data(result.data)
        else:
            self._status_bar.showMessage(f"✗ {result.error}")

    def closeEvent(self, event: Any) -> None:
        self._container.cleanup()
        event.accept()
