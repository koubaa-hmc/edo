"""Role-Aware Container - Dynamic widget container based on user roles."""

from __future__ import annotations
from typing import Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..core.role_registry import RolePolicy
from ..core.widget_factory import WidgetFactory
from ..core.backend_bridge import BackendBridge


class RoleAwareContainer(QWidget):
    """
    Central container that displays data using appropriate widgets
    based on user role permissions.
    """
    
    action_requested = pyqtSignal(str, dict)
    
    def __init__(
        self,
        role_policy: Optional[RolePolicy] = None,
        widget_factory: Optional[WidgetFactory] = None,
        backend_bridge: Optional[BackendBridge] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._policy = role_policy
        self._widget_factory = widget_factory or WidgetFactory()
        self._backend_bridge = backend_bridge or BackendBridge()
        self._current_widget: Optional[QWidget] = None
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main content area
        self._content_area = QStackedWidget()
        
        # Empty state placeholder
        self._empty_widget = QWidget()
        empty_layout = QVBoxLayout(self._empty_widget)
        empty_label = QLabel("No data loaded\n\nImport or select a dataset to begin")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 16px;
                padding: 40px;
            }
        """)
        empty_layout.addWidget(empty_label)
        
        self._content_area.addWidget(self._empty_widget)
        layout.addWidget(self._content_area)
    
    def set_policy(self, policy: RolePolicy) -> None:
        """Update the active role policy."""
        self._policy = policy
        # Could refresh UI based on new permissions if needed
    
    def display_data(self, data: Any) -> None:
        """Display data using an appropriate widget."""
        if data is None:
            self._content_area.setCurrentWidget(self._empty_widget)
            return
        
        # Create widget for data type
        widget = self._widget_factory.get_widget(data)
        
        if widget:
            # Remove old widget if exists
            if self._current_widget:
                self._content_area.removeWidget(self._current_widget)
                self._current_widget.deleteLater()
            
            self._current_widget = widget
            self._content_area.addWidget(widget)
            self._content_area.setCurrentWidget(widget)
        else:
            self._content_area.setCurrentWidget(self._empty_widget)
    
    def clear(self) -> None:
        """Clear the displayed data."""
        self.display_data(None)
    
    def cleanup(self) -> None:
        """Cleanup resources before destruction."""
        if self._current_widget:
            self._current_widget.deleteLater()
            self._current_widget = None
