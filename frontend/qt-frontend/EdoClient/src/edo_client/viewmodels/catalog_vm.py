"""
Catalog View Model - Abstract Model Tree 1: BrowseCatalog

ViewModel for PyQt/QML binding following MDUID specification.
Supports CF1, CF2, CF4 for FAIR Phase: SHARE/REUSE
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from PyQt6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    QVariant,
    pyqtSignal,
    pyqtSlot,
)

from ..models.catalog import (
    AccessType,
    CatalogModel,
    DatasetCard,
    FilterState,
    LicenseType,
)


class DatasetCardListModel(QAbstractListModel):
    """QML-compatible list model for dataset cards."""

    def __init__(self, parent: QObject | None):
        super().__init__(parent)
        self._cards: list[DatasetCard] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._cards)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(self._cards):
            return None

        card = self._cards[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return card.title
        elif role == Qt.ItemDataRole.UserRole:
            return card.to_dict()

        return None

    def roleNames(self) -> dict[int, bytes]:  # noqa: N802
        return {
            Qt.ItemDataRole.DisplayRole: b"title",
            Qt.ItemDataRole.UserRole: b"dataset",
        }

    def set_cards(self, cards: list[DatasetCard]) -> None:
        self.beginResetModel()
        self._cards = cards
        self.endResetModel()

    def get_card(self, index: int) -> DatasetCard | None:
        if 0 <= index < len(self._cards):
            return self._cards[index]
        return None


class CatalogViewModel(QObject):
    """
    ViewModel for catalog browsing interface.

    Corresponds to AbstractUI: BrowseCatalog
    Exposes properties and methods for QML binding.
    """

    # Signals
    loadingChanged = pyqtSignal(bool)  # noqa: N815
    errorChanged = pyqtSignal(str)  # noqa: N815
    filterStateChanged = pyqtSignal()  # noqa: N815
    paginationChanged = pyqtSignal()  # noqa: N815
    datasetSelected = pyqtSignal(QVariant)  # noqa: N815

    def __init__(self, parent: QObject | None):
        super().__init__(parent)
        self._model = CatalogModel()
        self._list_model = DatasetCardListModel(self)
        self._log = logging.getLogger("edo_client.viewmodel.catalog")

    @property
    def list_model(self) -> DatasetCardListModel:
        """Get the QML-compatible list model."""
        return self._list_model

    # Properties exposed to QML
    @property
    def isLoading(self) -> bool:  # noqa: N802
        return self._model.isLoading

    @isLoading.setter
    def isLoading(self, value: bool):  # noqa: N802
        if self._model.isLoading != value:
            self._model.isLoading = value
            self.loadingChanged.emit(value)

    @property
    def error(self) -> str | None:
        return self._model.error

    @error.setter
    def error(self, value: str | None):
        if self._model.error != value:
            self._model.error = value
            self.errorChanged.emit(value or "")

    @property
    def totalItems(self) -> int:  # noqa: N802
        return self._model.pagination.total_items

    @property
    def currentPage(self) -> int:  # noqa: N802
        return self._model.pagination.current_page

    @property
    def totalPages(self) -> int:  # noqa: N802
        return self._model.pagination.total_pages

    @property
    def pageSize(self) -> int:  # noqa: N802
        return self._model.pagination.page_size

    @property
    def hasPrevious(self) -> bool:  # noqa: N802
        return self._model.pagination.has_previous

    @property
    def hasNext(self) -> bool:  # noqa: N802
        return self._model.pagination.has_next

    @property
    def availableDomains(self) -> list[str]:  # noqa: N802
        return self._model.available_domains

    @property
    def activeFiltersCount(self) -> int:  # noqa: N802
        """Count of currently active filters."""
        count = 0
        fs = self._model.filter_state
        if fs.domains:
            count += 1
        if fs.search_query:
            count += 1
        if fs.licenses:
            count += 1
        if fs.access_types:
            count += 1
        if fs.date_start or fs.date_end:
            count += 1
        return count

    # Filter methods
    @pyqtSlot(str)
    def setSearchQuery(self, query: str):  # noqa: N802
        """Set search query and apply filters."""
        self._model.filter_state.search_query = query if query.strip() else None
        self._apply_filters()

    @pyqtSlot(QVariant)
    def setDomainFilter(self, domains: Any):  # noqa: N802
        """Set domain filter (array of strings)."""
        if isinstance(domains, list):
            self._model.filter_state.domains = domains
        elif isinstance(domains, str):
            self._model.filter_state.domains = [domains] if domains else []
        self._apply_filters()

    @pyqtSlot(QVariant)
    def setLicenseFilter(self, licenses: Any):  # noqa: N802
        """Set license filter (array of license types)."""
        if isinstance(licenses, list):
            self._model.filter_state.licenses = [
                LicenseType(l) for l in licenses if l
            ]
        self._apply_filters()

    @pyqtSlot(QVariant)
    def setAccessTypeFilter(self, access_types: Any):  # noqa: N802
        """Set access type filter (array of access types)."""
        if isinstance(access_types, list):
            self._model.filter_state.access_types = [
                AccessType(a) for a in access_types if a
            ]
        self._apply_filters()

    @pyqtSlot(str, str)
    def setDateRangeFilter(self, start: str, end: str):  # noqa: N802
        """Set date range filter (ISO format strings)."""
        try:
            self._model.filter_state.date_start = (
                datetime.fromisoformat(start) if start else None
            )
            self._model.filter_state.date_end = (
                datetime.fromisoformat(end) if end else None
            )
        except ValueError as e:
            self._log.warning("Invalid date format: %s", e)
        self._apply_filters()

    @pyqtSlot()
    def clearFilters(self):  # noqa: N802
        """Clear all filters and reload."""
        self._model.filter_state = FilterState()
        self._apply_filters()

    def _apply_filters(self):
        """Apply current filters to dataset list."""
        self._log.debug("Applying filters...")
        self.filterStateChanged.emit()
        # In real implementation, would call backend service
        # For now, just notify UI
        self._update_list_model()

    # Pagination methods
    @pyqtSlot()
    def nextPage(self):  # noqa: N802
        """Go to next page."""
        if self._model.next_page():
            self.paginationChanged.emit()
            self._update_list_model()

    @pyqtSlot()
    def previousPage(self):  # noqa: N802
        """Go to previous page."""
        if self._model.previous_page():
            self.paginationChanged.emit()
            self._update_list_model()

    @pyqtSlot(int)
    def jumpToPage(self, page: int):  # noqa: N802
        """Jump to specific page."""
        if self._model.jump_to_page(page):
            self.paginationChanged.emit()
            self._update_list_model()

    @pyqtSlot(int)
    def changePageSize(self, size: int):  # noqa: N802
        """Change page size."""
        self._model.change_page_size(size)
        self.paginationChanged.emit()
        self._update_list_model()

    # Dataset selection
    @pyqtSlot(int)
    def selectDataset(self, index: int):  # noqa: N802
        """Select a dataset by index."""
        card = self._list_model.get_card(index)
        if card:
            self.datasetSelected.emit(QVariant(card.to_dict()))
            self._log.info("Dataset selected: %s", card.doi)

    # Data loading
    def load_datasets(self, datasets: list[dict[str, Any]]) -> None:
        """Load datasets from backend response."""
        try:
            cards = []
            for data in datasets:
                card = DatasetCard(
                    title=data.get("title", "Untitled"),
                    doi=data.get("doi", ""),
                    publication_date=(
                        datetime.fromisoformat(data["publicationDate"])
                        if data.get("publicationDate") else None
                    ),
                    reuse_count=data.get("reuseCount", 0),
                    domain=data.get("domain"),
                    description=data.get("description"),
                )
                cards.append(card)

            self._model.datasets = cards
            self._model.pagination.total_items = len(cards)
            self._update_list_model()
            self._log.info("Loaded %d datasets", len(cards))

        except Exception as e:
            self._log.error("Failed to load datasets: %s", e)
            self.error = f"Failed to load datasets: {e}"

    def _update_list_model(self):
        """Update the QML list model with current page data."""
        visible = self._model.get_visible_datasets()
        self._list_model.set_cards(visible)

    def refresh(self) -> None:
        """Refresh catalog data."""
        self._log.info("Refreshing catalog...")
        self.isLoading = True
        self.error = None
        # In real implementation, would fetch from backend
        self.isLoading = False
