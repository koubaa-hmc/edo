"""RDF Inspector Widget - Displays RDF/graph data."""

from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class RDFInspector(QWidget):
    """Widget for inspecting RDF/graph data."""

    def __init__(self, data: Any, parent: QWidget | None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Info section
        info_group = QGroupBox("RDF Resource")
        info_layout = QVBoxLayout(info_group)

        self._uri_label = QLabel("")
        self._uri_label.setWordWrap(True)
        self._uri_label.setStyleSheet("font-family: 'Courier New', monospace; color: #0066cc;")
        info_layout.addWidget(self._uri_label)

        self._type_label = QLabel("")
        self._type_label.setStyleSheet("font-weight: bold; color: #666;")
        info_layout.addWidget(self._type_label)

        layout.addWidget(info_group)

        # Properties tree
        props_group = QGroupBox("Properties")
        props_layout = QVBoxLayout(props_group)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Property", "Value"])
        self._tree.setAlternatingRowColors(True)
        props_layout.addWidget(self._tree)

        layout.addWidget(props_group)

    def _load_data(self) -> None:
        """Load RDF data into the inspector."""
        if not isinstance(self._data, dict):
            self._uri_label.setText("Invalid RDF data")
            return

        uri = self._data.get("uri", self._data.get("@id", "Unknown"))
        rdf_type = self._data.get("@type", "Unknown")
        label = self._data.get("rdfs:label", self._data.get("label", ""))

        self._uri_label.setText(f"URI: {uri}")
        self._type_label.setText(f"Type: {rdf_type}" + (f" — {label}" if label else ""))

        # Load properties
        self._tree.clear()

        for key, value in self._data.items():
            # Skip special keys
            if key.startswith("@") or key == "uri":
                continue

            item = QTreeWidgetItem([key, str(value)])
            self._tree.addTopLevelItem(item)

        self._tree.expandAll()
        self._tree.resizeColumnToContents(0)
