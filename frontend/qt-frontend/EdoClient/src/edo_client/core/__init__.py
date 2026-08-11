"""Core components for EDO Client."""

from .role_registry import RoleRegistry, RolePolicy, Permission, get_role_registry
from .widget_factory import WidgetFactory, get_widget_factory
from .backend_bridge import BackendBridge, get_backend_bridge

__all__ = [
    "RoleRegistry",
    "RolePolicy",
    "Permission",
    "get_role_registry",
    "WidgetFactory",
    "get_widget_factory",
    "BackendBridge",
    "get_backend_bridge",
]
