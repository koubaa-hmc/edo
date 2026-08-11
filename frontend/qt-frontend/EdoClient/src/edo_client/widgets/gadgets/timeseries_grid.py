"""Timeseries Grid Widget - Displays time series data."""

from __future__ import annotations
from typing import Any, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel,
    QGroupBox, QHBoxLayout, QSlider
)
from PyQt6.QtCore import Qt


class TimeseriesGrid(QWidget):
    """Widget for viewing timeseries data."""
    
    def __init__(self, data: Any, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._data = data
        self._setup_ui()
        self._load_data()
    
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Info section
        info_group = QGroupBox("Timeseries Data")
        info_layout = QVBoxLayout(info_group)
        
        self._info_label = QLabel("")
        self._info_label.setWordWrap(True)
        info_layout.addWidget(self._info_label)
        
        layout.addWidget(info_group)
        
        # Data grid
        self._grid = QTableWidget()
        self._grid.setColumnCount(2)
        self._grid.setHorizontalHeaderLabels(["Timestamp", "Value"])
        self._grid.setAlternatingRowColors(True)
        self._grid.setStyleSheet("""
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
        layout.addWidget(self._grid)
        
        # Summary stats
        stats_layout = QHBoxLayout()
        
        self._min_label = QLabel("Min: -")
        self._max_label = QLabel("Max: -")
        self._avg_label = QLabel("Avg: -")
        self._count_label = QLabel("Count: -")
        
        for label in [self._min_label, self._max_label, self._avg_label, self._count_label]:
            label.setStyleSheet("font-weight: bold;")
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        layout.addLayout(stats_layout)
    
    def _load_data(self) -> None:
        """Load timeseries data into the grid."""
        timestamps: List[str] = []
        values: List[float] = []
        
        if isinstance(self._data, dict):
            timestamps = self._data.get("timestamps", [])
            values = self._data.get("values", [])
        
        # Update info
        self._info_label.setText(f"Time Range: {len(timestamps)} data points")
        
        # Setup grid
        self._grid.setRowCount(len(timestamps))
        
        # Populate grid (limit to first 100 rows)
        display_count = min(len(timestamps), 100)
        for i in range(display_count):
            ts_item = QTableWidgetItem(timestamps[i] if i < len(timestamps) else "")
            ts_item.setFlags(ts_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._grid.setItem(i, 0, ts_item)
            
            val_item = QTableWidgetItem(str(values[i]) if i < len(values) else "")
            val_item.setFlags(val_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._grid.setItem(i, 1, val_item)
        
        if len(timestamps) > 100:
            self._grid.insertRow(100)
            msg_item = QTableWidgetItem(f"... and {len(timestamps) - 100} more points")
            msg_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self._grid.setItem(100, 0, msg_item)
            self._grid.mergeCells(100, 0, 1, 2)
        
        # Calculate statistics
        if values:
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            if numeric_values:
                self._min_label.setText(f"Min: {min(numeric_values):.2f}")
                self._max_label.setText(f"Max: {max(numeric_values):.2f}")
                self._avg_label.setText(f"Avg: {sum(numeric_values)/len(numeric_values):.2f}")
        
        self._count_label.setText(f"Count: {len(timestamps)}")
        
        # Resize columns
        self._grid.resizeColumnsToContents()
