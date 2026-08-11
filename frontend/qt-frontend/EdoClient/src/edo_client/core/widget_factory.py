"""Widget Factory - Creates appropriate widgets for different data types."""

from __future__ import annotations
from typing import Any, Dict, Callable, Optional, Type
from PyQt6.QtWidgets import QWidget


class WidgetSpec:
    """Specification for a widget type."""
    
    def __init__(
        self,
        widget_id: str,
        display_name: str,
        data_types: list[str],
        widget_class: Type[QWidget],
        priority: int = 0
    ) -> None:
        self.widget_id = widget_id
        self.display_name = display_name
        self.data_types = data_types
        self.widget_class = widget_class
        self.priority = priority


class WidgetFactory:
    """Factory for creating data-appropriate widgets."""
    
    def __init__(self) -> None:
        self._widgets: Dict[str, WidgetSpec] = {}
        self._setup_builtin_widgets()
    
    def _setup_builtin_widgets(self) -> None:
        """Register built-in widget types."""
        # Import here to avoid circular dependencies
        from ..widgets.gadgets import (
            DatasetBrowser, TableViewer, TimeseriesGrid,
            LiteralViewer, RDFInspector, FallbackViewer
        )
        
        self.register_widget(WidgetSpec(
            widget_id="dataset_browser",
            display_name="Dataset Browser",
            data_types=["dataset"],
            widget_class=DatasetBrowser,
            priority=10
        ))
        
        self.register_widget(WidgetSpec(
            widget_id="table_viewer",
            display_name="Table Viewer",
            data_types=["table", "dataframe"],
            widget_class=TableViewer,
            priority=10
        ))
        
        self.register_widget(WidgetSpec(
            widget_id="timeseries_grid",
            display_name="Timeseries Grid",
            data_types=["timeseries", "time_series"],
            widget_class=TimeseriesGrid,
            priority=10
        ))
        
        self.register_widget(WidgetSpec(
            widget_id="literal_viewer",
            display_name="Literal Viewer",
            data_types=["literal", "string", "text"],
            widget_class=LiteralViewer,
            priority=5
        ))
        
        self.register_widget(WidgetSpec(
            widget_id="rdf_inspector",
            display_name="RDF Inspector",
            data_types=["rdf", "graph", "triple"],
            widget_class=RDFInspector,
            priority=10
        ))
        
        self.register_widget(WidgetSpec(
            widget_id="fallback_viewer",
            display_name="Data Viewer",
            data_types=["*"],
            widget_class=FallbackViewer,
            priority=0
        ))
    
    def register_widget(self, spec: WidgetSpec) -> None:
        """Register a widget specification."""
        self._widgets[spec.widget_id] = spec
    
    def get_widget(self, data: Any) -> Optional[QWidget]:
        """Create an appropriate widget for the given data."""
        data_type = self._infer_data_type(data)
        
        # Find matching widgets
        candidates: list[tuple[int, WidgetSpec]] = []
        for spec in self._widgets.values():
            if "*" in spec.data_types or data_type in spec.data_types:
                candidates.append((spec.priority, spec))
        
        if not candidates:
            # Fall back to fallback viewer
            fallback = self._widgets.get("fallback_viewer")
            if fallback:
                return fallback.widget_class(data)
            return None
        
        # Sort by priority (highest first)
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_spec = candidates[0][1]
        
        try:
            return best_spec.widget_class(data)
        except Exception as e:
            print(f"Error creating widget {best_spec.widget_id}: {e}")
            fallback = self._widgets.get("fallback_viewer")
            if fallback:
                return fallback.widget_class(data)
            return None
    
    def _infer_data_type(self, data: Any) -> str:
        """Infer the data type from the data structure."""
        if data is None:
            return "null"
        
        # Check for explicit type marker
        if isinstance(data, dict):
            if "_type" in data:
                return str(data["_type"]).lower()
            if "timestamps" in data and "values" in data:
                return "timeseries"
            if "title" in data and "resources" in data:
                return "dataset"
            if "@type" in data or "uri" in data:
                return "rdf"
            if "columns" in data and "rows" in data:
                return "table"
        
        # Check Python type
        type_name = type(data).__name__.lower()
        if "dict" in type_name:
            return "literal"
        if "list" in type_name:
            return "literal"
        if "str" in type_name:
            return "literal"
        if "pandas" in str(type(data)).lower():
            return "dataframe"
        
        return "literal"
    
    def get_available_widgets(self) -> list[WidgetSpec]:
        """Get all registered widget specifications."""
        return list(self._widgets.values())


# Global factory instance
_factory: Optional[WidgetFactory] = None


def get_widget_factory() -> WidgetFactory:
    """Get or create the global widget factory."""
    global _factory
    if _factory is None:
        _factory = WidgetFactory()
    return _factory
