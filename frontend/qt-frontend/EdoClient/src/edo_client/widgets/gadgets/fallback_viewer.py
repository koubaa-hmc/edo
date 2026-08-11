"""Fallback Viewer Widget - Generic viewer for unsupported data types."""

from __future__ import annotations

import json
from typing import Any

from PyQt6.QtWidgets import QGroupBox, QLabel, QTextEdit, QVBoxLayout, QWidget


class FallbackViewer(QWidget):
    """Generic fallback widget for displaying any data type."""

    def __init__(self, data: Any, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Info section
        info_group = QGroupBox("Data Preview")
        info_layout = QVBoxLayout(info_group)

        self._type_label = QLabel("")
        self._type_label.setStyleSheet("font-weight: bold;")
        info_layout.addWidget(self._type_label)

        self._size_label = QLabel("")
        self._size_label.setStyleSheet("color: #666;")
        info_layout.addWidget(self._size_label)

        layout.addWidget(info_group)

        # Content display
        self._content = QTextEdit()
        self._content.setReadOnly(True)
        self._content.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                background-color: #f8f9fa;
                font-family: 'Courier New', Courier, monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self._content)

        # Note
        note_label = QLabel("ℹ️ This is a generic viewer. Data may have a more specific viewer available.")
        note_label.setStyleSheet("color: #856404; font-style: italic;")
        note_label.setWordWrap(True)
        layout.addWidget(note_label)

    def _load_data(self) -> None:
        """Load data into the viewer."""
        self._type_label.setText(f"Type: {type(self._data).__name__}")

        # Calculate approximate size
        try:
            data_str = str(self._data)
            self._size_label.setText(f"Length: {len(data_str)} characters")
        except:
            self._size_label.setText("Size: Unknown")

        # Display content
        try:
            if isinstance(self._data, (dict, list)):
                formatted = json.dumps(self._data, indent=2, default=str, ensure_ascii=False)
                self._content.setPlainText(formatted[:10000])  # Limit display
            else:
                self._content.setPlainText(str(self._data)[:10000])
        except Exception as e:
            self._content.setPlainText(f"Error displaying data: {e}")
