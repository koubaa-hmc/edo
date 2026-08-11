"""Table Viewer Widget - Displays tabular data."""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class TableViewer(QWidget):
    """Widget for viewing tabular data."""

    def __init__(self, data: Any, parent: QWidget | None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Info label
        info_group = QGroupBox("Table Data")
        info_layout = QVBoxLayout(info_group)

        self._info_label = QLabel("")
        self._info_label.setWordWrap(True)
        info_layout.addWidget(self._info_label)

        layout.addWidget(info_group)

        # Table
        self._table = QTableWidget()
        self._table.setAlternatingRowColors(True)
        self._table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                gridline-color: #dee2e6;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 4px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        layout.addWidget(self._table)

    def _load_data(self) -> None:
        """Load tabular data into the table."""
        columns: list[str] = []
        rows: list[list[Any]] = []

        if isinstance(self._data, dict):
            columns = self._data.get("columns", [])
            rows = self._data.get("rows", [])
        elif isinstance(self._data, list) and len(self._data) > 0:
            if isinstance(self._data[0], dict):
                columns = list(self._data[0].keys())
                rows = [[row.get(col) for col in columns] for row in self._data]
            else:
                columns = ["Value"]
                rows = [[item] for item in self._data]

        # Update info
        self._info_label.setText(f"Rows: {len(rows)} | Columns: {len(columns)}")

        # Setup table
        self._table.setColumnCount(len(columns))
        self._table.setHorizontalHeaderLabels(columns)
        self._table.setRowCount(len(rows))

        # Populate table (limit to first 100 rows for performance)
        display_rows = min(len(rows), 100)
        for row_idx in range(display_rows):
            for col_idx, col_name in enumerate(columns):
                value = rows[row_idx][col_idx] if col_idx < len(rows[row_idx]) else ""
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self._table.setItem(row_idx, col_idx, item)

        if len(rows) > 100:
            self._table.insertRow(100)
            msg_item = QTableWidgetItem(f"... and {len(rows) - 100} more rows")
            msg_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self._table.setItem(100, 0, msg_item)
            self._table.mergeCells(100, 0, 1, len(columns))

        # Resize columns to fit content
        self._table.resizeColumnsToContents()
