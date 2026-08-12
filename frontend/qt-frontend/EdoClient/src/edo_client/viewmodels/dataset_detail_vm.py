"""
Dataset Detail View Model - Abstract Model Tree 2: ViewDatasetDetail

ViewModel for PyQt/QML binding following MDUID specification.
Supports CF1, CF2, CF4 for FAIR Phase: REUSE
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from PyQt6.QtCore import QObject, QVariant, pyqtSignal, pyqtSlot

from ..models.catalog import AccessType, Author, DatasetCard, LicenseType


class DatasetDetailViewModel(QObject):
    """
    ViewModel for dataset detail view.

    Corresponds to AbstractUI: ViewDatasetDetail
    Exposes properties and methods for QML binding.
    """

    # Signals
    loadingChanged = pyqtSignal(bool)  # noqa: N815
    errorChanged = pyqtSignal(str)  # noqa: N815
    tabChanged = pyqtSignal(int)  # noqa: N815
    dataExported = pyqtSignal(str, str)  # noqa: N815 (format, content)
    accessRequested = pyqtSignal(QVariant)  # noqa: N815

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._dataset: DatasetCard | None = None
        self._current_tab = 0  # 0=Overview, 1=Metadata, 2=Files, 3=Usage, 4=Similar
        self._isLoading = False
        self._error: str | None = None
        self._log = logging.getLogger("edo_client.viewmodel.dataset_detail")

        # Mock data for tabs
        self._files: list[dict[str, Any]] = []
        self._metrics = {
            "viewCount": 0,
            "downloadCount": 0,
            "citationCount": 0
        }
        self._similar_datasets: list[DatasetCard] = []

    # Properties exposed to QML
    @property
    def isLoading(self) -> bool:  # noqa: N802
        return self._isLoading

    @isLoading.setter
    def isLoading(self, value: bool):  # noqa: N802
        if self._isLoading != value:
            self._isLoading = value
            self.loadingChanged.emit(value)

    @property
    def error(self) -> str | None:
        return self._error

    @error.setter
    def error(self, value: str | None):
        if self._error != value:
            self._error = value
            self.errorChanged.emit(value or "")

    @property
    def currentTab(self) -> int:  # noqa: N802
        return self._current_tab

    @property
    def hasDataset(self) -> bool:  # noqa: N802
        return self._dataset is not None

    # Dataset properties
    @property
    def title(self) -> str:  # noqa: N802
        return self._dataset.title if self._dataset else ""

    @property
    def doi(self) -> str:  # noqa: N802
        return self._dataset.doi if self._dataset else ""

    @property
    def description(self) -> str:  # noqa: N802
        return self._dataset.description or ""

    @property
    def authors(self) -> list[dict[str, Any]]:  # noqa: N802
        if not self._dataset:
            return []
        return [
            {"name": a.name, "orcid": a.orcid, "affiliation": a.affiliation}
            for a in self._dataset.authors
        ]

    @property
    def institution(self) -> str:  # noqa: N802
        return self._dataset.institution or "" if self._dataset else ""

    @property
    def publicationDate(self) -> str | None:  # noqa: N802
        if self._dataset and self._dataset.publication_date:
            return self._dataset.publication_date.isoformat()
        return None

    @property
    def license(self) -> str:  # noqa: N802
        return self._dataset.license.value if self._dataset else ""

    @property
    def accessType(self) -> str:  # noqa: N802
        return self._dataset.access_type.value if self._dataset else ""

    @property
    def isOpenAccess(self) -> bool:  # noqa: N802
        return self._dataset.is_open_access if self._dataset else False

    @property
    def reuseCount(self) -> int:  # noqa: N802
        return self._dataset.reuse_count if self._dataset else 0

    # Tab management
    @pyqtSlot(int)
    def setTab(self, index: int):  # noqa: N802
        """Switch to a different tab."""
        if 0 <= index <= 4:
            self._current_tab = index
            self.tabChanged.emit(index)
            self._log.debug("Switched to tab %d", index)

    @pyqtSlot()
    def nextTab(self):  # noqa: N802
        """Go to next tab."""
        if self._current_tab < 4:
            self.setTab(self._current_tab + 1)

    @pyqtSlot()
    def previousTab(self):  # noqa: N802
        """Go to previous tab."""
        if self._current_tab > 0:
            self.setTab(self._current_tab - 1)

    # File access
    @pyqtSlot(result=QVariant)
    def getFiles(self) -> Any:  # noqa: N802
        """Get list of files in dataset."""
        return self._files

    @pyqtSlot(int)
    def downloadFile(self, index: int):  # noqa: N802
        """Download a specific file."""
        if 0 <= index < len(self._files):
            file_info = self._files[index]
            self._log.info("Downloading file: %s", file_info.get("name"))
            # In real implementation, would trigger download

    @pyqtSlot()
    def downloadAll(self):  # noqa: N802
        """Download all files."""
        if self.isOpenAccess:
            self._log.info("Downloading all files (%d)", len(self._files))
            # In real implementation, would trigger batch download
        else:
            self.requestAccess()

    @pyqtSlot()
    def requestAccess(self):  # noqa: N802
        """Request access to restricted dataset."""
        if self._dataset:
            self.accessRequested.emit(QVariant({
                "doi": self._dataset.doi,
                "title": self._dataset.title
            }))

    # Export functionality
    @pyqtSlot(str)
    def exportCitation(self, format: str):  # noqa: N802
        """Export citation in specified format."""
        if not self._dataset:
            return

        citation = self._generate_citation(format)
        self.dataExported.emit(format, citation)
        self._log.info("Exported citation in %s format", format)

    def _generate_citation(self, format: str) -> str:
        """Generate citation string in specified format."""
        if not self._dataset:
            return ""

        authors_str = self._dataset.author_names
        year = self._dataset.publication_year or "n.d."
        title = self._dataset.title
        doi = self._dataset.doi

        if format == "APA":
            return f"{authors_str} ({year}). {title}. DOI: {doi}"
        elif format == "MLA":
            return f"{authors_str}. \"{title}.\" {year}, DOI: {doi}."
        elif format == "BibTeX":
            return f"""@dataset{{{self._dataset.doi.replace('10.', '')},
  author = {{{authors_str}}},
  title = {{{title}}},
  year = {{{year}}},
  doi = {{{doi}}}
}}"""
        elif format == "RIS":
            return f"""TY  - DATA
AU  - {authors_str}
TI  - {title}
PY  - {year}
DO  - {doi}
ER  - """
        else:
            return f"{authors_str} ({year}). {title}. {doi}"

    @pyqtSlot(result=QVariant)
    def getMetrics(self) -> Any:  # noqa: N802
        """Get usage metrics."""
        return self._metrics

    @pyqtSlot(result=QVariant)
    def getSimilarDatasets(self) -> Any:  # noqa: N802
        """Get similar datasets."""
        return [d.to_dict() for d in self._similar_datasets]

    # Similarity search (CF4)
    @pyqtSlot(str)
    def findSimilarBy(self, criteria: str):  # noqa: N802
        """Find similar datasets by criteria."""
        self._log.info("Finding similar datasets by: %s", criteria)
        # In real implementation, would call semantic search service
        # For now, just notify
        self.similarSearchCompleted.emit()

    # Actions
    @pyqtSlot()
    def cite(self):  # noqa: N802
        """Open citation dialog."""
        self._log.info("Opening citation dialog")
        # Would show modal in UI

    @pyqtSlot()
    def flag(self):  # noqa: N802
        """Flag dataset for review."""
        self._log.info("Flagging dataset: %s", self.doi)
        # Would open report issue modal

    @pyqtSlot(str)
    def edit(self, role: str):  # noqa: N802
        """Edit metadata (role-gated)."""
        if role in ["research_fellow", "data_steward"]:
            self._log.info("Opening editor for dataset: %s", self.doi)
            # Would navigate to EditMetadata view
        else:
            self._log.warning("Insufficient permissions to edit")

    # Data loading
    def load_dataset(self, data: dict[str, Any]) -> None:
        """Load dataset from backend response."""
        try:
            self.isLoading = True

            # Parse authors
            authors = []
            for author_data in data.get("authors", []):
                authors.append(Author(
                    name=author_data.get("name", ""),
                    orcid=author_data.get("orcid"),
                    affiliation=author_data.get("affiliation")
                ))

            # Create dataset card
            self._dataset = DatasetCard(
                title=data.get("title", ""),
                doi=data.get("doi", ""),
                authors=authors,
                institution=data.get("institution"),
                publication_date=(
                    datetime.fromisoformat(data["publicationDate"])
                    if data.get("publicationDate") else None
                ),
                license=LicenseType(data.get("license", "CC-BY-4.0")),
                access_type=AccessType(data.get("accessType", "open")),
                reuse_count=data.get("reuseCount", 0),
                domain=data.get("domain"),
                description=data.get("description"),
            )

            # Load files
            self._files = data.get("files", [])

            # Load metrics
            if "metrics" in data:
                self._metrics = data["metrics"]

            self.isLoading = False
            self._log.info("Loaded dataset: %s", self._dataset.doi)

        except Exception as e:
            self.isLoading = False
            self.error = f"Failed to load dataset: {e}"
            self._log.error("Failed to load dataset: %s", e)

    def refresh(self) -> None:
        """Refresh dataset information."""
        self._log.info("Refreshing dataset: %s", self.doi)
        self.isLoading = True
        self.error = None
        # In real implementation, would fetch updated data
        self.isLoading = False
