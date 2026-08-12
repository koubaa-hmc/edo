"""
Review View Model - Abstract Model Trees 5 & 6: ReviewDashboard & ReviewDetail

ViewModel for PyQt/QML binding following MDUID specification.
Supports CF2, CF3, CF4 for FAIR Phase: PRESERVE
Primary Role: data_steward
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

from ..models.review import (
    ReviewChecklistItem,
    ReviewItem,
    ReviewQueueModel,
    ReviewStatus,
    RevisionIssue,
)


class ReviewQueueListModel(QAbstractListModel):
    """QML-compatible list model for review queue items."""

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._items: list[ReviewItem] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._items)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= len(self._items):
            return None

        item = self._items[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return item.dataset_title
        elif role == Qt.ItemDataRole.UserRole:
            return item.to_dict()

        return None

    def roleNames(self) -> dict[int, bytes]:  # noqa: N802
        return {
            Qt.ItemDataRole.DisplayRole: b"title",
            Qt.ItemDataRole.UserRole: b"reviewItem",
        }

    def set_items(self, items: list[ReviewItem]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()

    def get_item(self, index: int) -> ReviewItem | None:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None


class ReviewViewModel(QObject):
    """
    ViewModel for metadata review interface.

    Corresponds to AbstractUI: ReviewDashboard & ReviewDetail
    Exposes properties and methods for QML binding.
    """

    # Signals
    loadingChanged = pyqtSignal(bool)  # noqa: N815
    statsChanged = pyqtSignal()  # noqa: N815
    selectionChanged = pyqtSignal()  # noqa: N815
    itemSelected = pyqtSignal(QVariant)  # noqa: N815
    filterChanged = pyqtSignal()  # noqa: N815

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._model = ReviewQueueModel()
        self._list_model = ReviewQueueListModel(self)
        self._selected_item: ReviewItem | None = None
        self._log = logging.getLogger("edo_client.viewmodel.review")

    @property
    def list_model(self) -> ReviewQueueListModel:
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
    def stats(self) -> dict[str, Any]:
        """Get queue statistics."""
        return self._model.stats.to_dict()

    @property
    def selectedCount(self) -> int:  # noqa: N802
        return len(self._model.selected_review_ids)

    @property
    def hasSelection(self) -> bool:  # noqa: N802
        return self.selectedCount > 0

    # Filter properties
    @property
    def statusFilter(self) -> str | None:  # noqa: N802
        return self._model.status_filter.value if self._model.status_filter else None

    @property
    def sortBy(self) -> str:  # noqa: N802
        return self._model.sort_by

    @property
    def sortAscending(self) -> bool:  # noqa: N802
        return self._model.sort_ascending

    # Status filter
    @pyqtSlot(str)
    def setStatusFilter(self, status: str):  # noqa: N802
        """Set status filter."""
        if status:
            self._model.status_filter = ReviewStatus(status)
        else:
            self._model.status_filter = None
        self.filterChanged.emit()
        self._update_list_model()

    @pyqtSlot()
    def clearFilters(self):  # noqa: N802
        """Clear all filters."""
        self._model.refresh()
        self.filterChanged.emit()
        self._update_list_model()

    # Sorting
    @pyqtSlot(str)
    def setSortBy(self, field: str):  # noqa: N802
        """Set sort field."""
        if self._model.sort_by == field:
            # Toggle direction
            self._model.sort_ascending = not self._model.sort_ascending
        else:
            self._model.sort_by = field
            self._model.sort_ascending = True
        self._update_list_model()

    # Selection
    @pyqtSlot(int)
    def toggleSelection(self, index: int):  # noqa: N802
        """Toggle selection of an item."""
        item = self._list_model.get_item(index)
        if item:
            self._model.toggle_selection(item.review_id)
            self.selectionChanged.emit()

    @pyqtSlot()
    def selectAll(self):  # noqa: N802
        """Select all visible items."""
        self._model.select_all()
        self.selectionChanged.emit()

    @pyqtSlot()
    def clearSelection(self):  # noqa: N802
        """Clear all selections."""
        self._model.clear_selection()
        self.selectionChanged.emit()

    @pyqtSlot(int)
    def selectItem(self, index: int):  # noqa: N802
        """Select and open a review item."""
        item = self._list_model.get_item(index)
        if item:
            self._selected_item = item
            self.itemSelected.emit(QVariant(item.to_dict()))
            self._log.info("Selected review item: %s", item.review_id)

    # Bulk actions
    @pyqtSlot(str)
    def bulkAssign(self, reviewer_id: str):  # noqa: N802
        """Assign selected items to a reviewer."""
        count = self._model.bulk_assign(reviewer_id)
        self._log.info("Bulk assigned %d items to %s", count, reviewer_id)
        self._update_list_model()
        self.statsChanged.emit()
        self.clearSelection()

    @pyqtSlot()
    def bulkApprove(self):  # noqa: N802
        """Approve all selected items (if they pass validation)."""
        selected = self._model.get_selected_items()
        approved_count = 0

        for item in selected:
            if item.validation_report and item.validation_report.is_acceptable():
                item.approve("Bulk approval")
                approved_count += 1

        self._log.info("Bulk approved %d items", approved_count)
        self._update_list_model()
        self.statsChanged.emit()
        self.clearSelection()

    # Review operations
    @pyqtSlot(str, str)
    def assignReview(self, review_id: str, reviewer_id: str):  # noqa: N802
        """Assign a review to a steward."""
        item = self._get_review_item(review_id)
        if item:
            item.assign_to(reviewer_id)
            self._update_list_model()
            self.statsChanged.emit()
            self._log.info("Assigned review %s to %s", review_id, reviewer_id)

    @pyqtSlot(str, str, str)
    def approveReview(self, review_id: str, notes: str, auto_publish: bool = False):  # noqa: N802
        """Approve a review submission."""
        item = self._get_review_item(review_id)
        if item:
            item.approve(notes)
            self._update_list_model()
            self.statsChanged.emit()
            self._log.info("Approved review %s", review_id)

            if self._selected_item and self._selected_item.review_id == review_id:
                self._selected_item = item
                self.itemSelected.emit(QVariant(item.to_dict()))

    @pyqtSlot(str, str, str, str)
    def requestRevisions(  # noqa: N802
        self,
        review_id: str,
        issues_json: str,
        due_date: str,
        message: str
    ):  # noqa: N802
        """Request revisions for a review item."""
        import json

        item = self._get_review_item(review_id)
        if not item:
            return

        try:
            issues_data = json.loads(issues_json)
            issues = [
                RevisionIssue(
                    issue_id=i.get("issueId", f"issue_{idx}"),
                    field_reference=i.get("fieldReference"),
                    description=i.get("description", ""),
                    suggested_fix=i.get("suggestedFix")
                )
                for idx, i in enumerate(issues_data)
            ]

            due = datetime.fromisoformat(due_date)
            item.request_revisions(issues, due, message)

            self._update_list_model()
            self.statsChanged.emit()
            self._log.info("Requested revisions for review %s", review_id)

        except Exception as e:
            self._log.error("Failed to request revisions: %s", e)

    @pyqtSlot(str, str, bool)
    def addCorrespondence(  # noqa: N802
        self,
        review_id: str,
        message: str,
        is_internal: bool = False
    ):  # noqa: N802
        """Add correspondence to a review."""
        item = self._get_review_item(review_id)
        if item:
            item.add_correspondence(message, "reviewer", is_internal)
            self._log.info("Added correspondence to review %s", review_id)

            if self._selected_item and self._selected_item.review_id == review_id:
                self._selected_item = item
                self.itemSelected.emit(QVariant(item.to_dict()))

    @pyqtSlot(str, str)
    def addChecklistItem(self, review_id: str, description: str):  # noqa: N802
        """Add a checklist item to a review."""
        item = self._get_review_item(review_id)
        if item:
            checklist_item = ReviewChecklistItem(
                item_id=f"check_{len(item.checklist) + 1}",
                description=description
            )
            item.checklist.append(checklist_item)
            self._log.info("Added checklist item to review %s", review_id)

    @pyqtSlot(str, str)
    def toggleChecklistItem(self, review_id: str, item_id: str):  # noqa: N802
        """Toggle a checklist item."""
        item = self._get_review_item(review_id)
        if item:
            for checklist_item in item.checklist:
                if checklist_item.item_id == item_id:
                    checklist_item.toggle()
                    break
            self._log.debug("Toggled checklist item %s", item_id)

    # Checklist access
    @pyqtSlot(str, result=QVariant)
    def getChecklist(self, review_id: str) -> Any:  # noqa: N802
        """Get checklist for a review item."""
        item = self._get_review_item(review_id)
        if item:
            return [
                {
                    "itemId": ci.item_id,
                    "description": ci.description,
                    "isChecked": ci.is_checked,
                    "notes": ci.notes,
                    "required": ci.required
                }
                for ci in item.checklist
            ]
        return []

    # Timeline access
    @pyqtSlot(str, result=QVariant)
    def getTimeline(self, review_id: str) -> Any:  # noqa: N802
        """Get activity timeline for a review item."""
        item = self._get_review_item(review_id)
        if item:
            return [
                {
                    "eventId": e.event_id,
                    "eventType": e.event_type,
                    "description": e.description,
                    "actor": e.actor,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in item.activity_log
            ]
        return []

    # Correspondence access
    @pyqtSlot(str, result=QVariant)
    def getCorrespondence(self, review_id: str) -> Any:  # noqa: N802
        """Get correspondence thread for a review item."""
        item = self._get_review_item(review_id)
        if item:
            return [
                {
                    "messageId": c.message_id,
                    "fromRole": c.from_role,
                    "message": c.message,
                    "timestamp": c.timestamp.isoformat(),
                    "isInternal": c.is_internal
                }
                for c in item.correspondence
            ]
        return []

    # Helper methods
    def _get_review_item(self, review_id: str) -> ReviewItem | None:
        """Get review item by ID."""
        for item in self._model.items:
            if item.review_id == review_id:
                return item
        return None

    def _update_list_model(self):
        """Update the QML list model with filtered/sorted items."""
        visible = self._model.get_visible_items()
        self._list_model.set_items(visible)

    # Data loading
    def load_reviews(self, reviews: list[dict[str, Any]]) -> None:
        """Load review items from backend response."""
        try:
            items = []
            for data in reviews:
                item = ReviewItem(
                    review_id=data.get("reviewId", ""),
                    dataset_id=data.get("datasetId", ""),
                    dataset_title=data.get("datasetTitle", ""),
                    submitter_name=data.get("submitterName", ""),
                    submitter_orcid=data.get("submitterOrcid"),
                    domain=data.get("domain"),
                    completeness_score=data.get("completenessScore", 0.0),
                    status=ReviewStatus(data.get("status", "pending")),
                )

                # Parse dates
                if data.get("submissionDate"):
                    item.submission_date = datetime.fromisoformat(data["submissionDate"])
                if data.get("assignedAt"):
                    item.assigned_at = datetime.fromisoformat(data["assignedAt"])

                items.append(item)

            self._model.items = items
            self._model.calculate_stats()
            self._update_list_model()
            self.statsChanged.emit()
            self._log.info("Loaded %d review items", len(items))

        except Exception as e:
            self._log.error("Failed to load reviews: %s", e)

    def refresh(self) -> None:
        """Refresh review queue."""
        self._log.info("Refreshing review queue...")
        self.isLoading = True
        # In real implementation, would fetch from backend
        self.isLoading = False
        self.statsChanged.emit()
