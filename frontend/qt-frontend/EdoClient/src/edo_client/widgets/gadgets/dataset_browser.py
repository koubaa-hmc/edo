"""Dataset Browser Widget - Displays dataset metadata and resources."""

from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DatasetBrowser(QWidget):
    """Widget for browsing dataset metadata and resources."""

    def __init__(self, data: Any, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title section
        title_group = QGroupBox("Dataset Information")
        title_layout = QVBoxLayout(title_group)

        self._title_label = QLabel("")
        self._title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self._title_label.setWordWrap(True)
        title_layout.addWidget(self._title_label)

        self._description_label = QLabel("")
        self._description_label.setWordWrap(True)
        self._description_label.setStyleSheet("color: #666;")
        title_layout.addWidget(self._description_label)

        layout.addWidget(title_group)

        # Resources tree
        resources_group = QGroupBox("Resources")
        resources_layout = QVBoxLayout(resources_group)

        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Name", "Format", "Size"])
        self._tree.setAlternatingRowColors(True)
        resources_layout.addWidget(self._tree)

        layout.addWidget(resources_group)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self._load_btn = QPushButton("Load Dataset")
        self._load_btn.clicked.connect(self._on_load_clicked)
        button_layout.addWidget(self._load_btn)

        layout.addLayout(button_layout)

    def _load_data(self) -> None:
        """Load dataset information into the UI."""
        if isinstance(self._data, dict):
            self._title_label.setText(self._data.get("title", "Untitled Dataset"))
            self._description_label.setText(self._data.get("description", ""))

            # Load resources
            resources = self._data.get("resources", [])
            self._tree.clear()

            for resource in resources:
                item = QTreeWidgetItem([
                    resource.get("name", "Unknown"),
                    resource.get("format", "Unknown"),
                    resource.get("size", "-")
                ])
                self._tree.addTopLevelItem(item)

            # Expand all items
            self._tree.expandAll()

    def _on_load_clicked(self) -> None:
        """Handle load button click."""
        # Emit signal or trigger data loading
        print(f"Loading dataset: {self._data.get('title', 'Unknown')}")
