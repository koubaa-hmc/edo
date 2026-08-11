"""Literal Viewer Widget - Displays simple data types (strings, numbers, etc.)."""

from __future__ import annotations

import json
from typing import Any

from PyQt6.QtWidgets import QGroupBox, QLabel, QTextEdit, QVBoxLayout, QWidget


class LiteralViewer(QWidget):
    """Widget for viewing literal/simple data values."""

    def __init__(self, data: Any, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Info label
        info_group = QGroupBox("Data Value")
        info_layout = QVBoxLayout(info_group)

        self._type_label = QLabel("")
        self._type_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self._type_label)

        layout.addWidget(info_group)

        # Content display
        self._content = QTextEdit()
        self._content.setReadOnly(True)
        self._content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                background-color: #ffffff;
                font-family: 'Courier New', Courier, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self._content)

    def _load_data(self) -> None:
        """Load data into the viewer."""
        # Update type label
        self._type_label.setText(f"Type: {type(self._data).__name__}")

        # Format content based on type
        if isinstance(self._data, (dict, list)):
            try:
                formatted = json.dumps(self._data, indent=2, default=str)
                self._content.setPlainText(formatted)
            except Exception as e:
                self._content.setPlainText(str(self._data))
        else:
            self._content.setPlainText(str(self._data))
