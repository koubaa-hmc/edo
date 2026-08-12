"""
Catalog Models - Abstract Model Tree 1: BrowseCatalog

Supports CF1, CF2, CF4 for FAIR Phase: SHARE/REUSE
Primary Roles: guest_viewer, research_fellow, data_steward
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AccessType(Enum):
    """Dataset access types."""
    OPEN = "open"
    EMBARGOED = "embargoed"
    RESTRICTED = "restricted"
    CLOSED = "closed"


class LicenseType(Enum):
    """Common license types."""
    CC0 = "CC0-1.0"
    CC_BY = "CC-BY-4.0"
    CC_BY_SA = "CC-BY-SA-4.0"
    CC_BY_NC = "CC-BY-NC-4.0"
    ODC_BY = "ODC-By-1.0"
    ODC_ODBL = "ODbL-1.0"
    CUSTOM = "custom"


@dataclass
class Author:
    """Dataset author/contributor information."""
    name: str
    orcid: Optional[str] = None
    affiliation: Optional[str] = None
    ror_id: Optional[str] = None
    
    def has_orcid(self) -> bool:
        return self.orcid is not None
    
    def has_affiliation(self) -> bool:
        return self.affiliation is not None


@dataclass
class DatasetCard:
    """
    Represents a dataset card in the catalog grid.
    
    Corresponds to AbstractUI: BrowseCatalog → MainContent → ResultsGrid → DatasetCard
    """
    title: str
    doi: str
    authors: List[Author] = field(default_factory=list)
    institution: Optional[str] = None
    ror_badge: Optional[str] = None
    publication_date: Optional[datetime] = None
    license: LicenseType = LicenseType.CC_BY
    access_type: AccessType = AccessType.OPEN
    reuse_count: int = 0
    domain: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    
    # Computed properties for UI display
    @property
    def author_names(self) -> str:
        """Format authors for display."""
        if not self.authors:
            return "Unknown"
        if len(self.authors) == 1:
            return self.authors[0].name
        elif len(self.authors) == 2:
            return f"{self.authors[0].name} and {self.authors[1].name}"
        else:
            return f"{self.authors[0].name} et al."
    
    @property
    def publication_year(self) -> Optional[int]:
        """Extract year from publication date."""
        if self.publication_date:
            return self.publication_date.year
        return None
    
    @property
    def is_open_access(self) -> bool:
        """Check if dataset is openly accessible."""
        return self.access_type == AccessType.OPEN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for QML serialization."""
        return {
            "title": self.title,
            "doi": self.doi,
            "authors": [
                {"name": a.name, "orcid": a.orcid, "affiliation": a.affiliation}
                for a in self.authors
            ],
            "institution": self.institution,
            "publicationDate": self.publication_date.isoformat() if self.publication_date else None,
            "license": self.license.value,
            "accessType": self.access_type.value,
            "reuseCount": self.reuse_count,
            "domain": self.domain,
            "description": self.description,
        }


@dataclass
class FilterState:
    """Current state of catalog filters."""
    domains: List[str] = field(default_factory=list)
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    licenses: List[LicenseType] = field(default_factory=list)
    access_types: List[AccessType] = field(default_factory=list)
    search_query: Optional[str] = None
    
    def is_active(self) -> bool:
        """Check if any filters are applied."""
        return bool(
            self.domains or 
            self.date_start or 
            self.date_end or 
            self.licenses or 
            self.access_types or
            self.search_query
        )


@dataclass
class PaginationState:
    """Pagination state for catalog results."""
    page_size: int = 25
    current_page: int = 1
    total_items: int = 0
    
    @property
    def total_pages(self) -> int:
        if self.page_size <= 0:
            return 1
        return (self.total_items + self.page_size - 1) // self.page_size
    
    @property
    def has_previous(self) -> bool:
        return self.current_page > 1
    
    @property
    def has_next(self) -> bool:
        return self.current_page < self.total_pages
    
    @property
    def offset(self) -> int:
        return (self.current_page - 1) * self.page_size


@dataclass
class CatalogModel:
    """
    Complete catalog browsing model.
    
    Corresponds to AbstractUI: BrowseCatalog
    """
    datasets: List[DatasetCard] = field(default_factory=list)
    filter_state: FilterState = field(default_factory=FilterState)
    pagination: PaginationState = field(default_factory=PaginationState)
    isLoading: bool = False
    error: Optional[str] = None
    
    # Available filter options
    available_domains: List[str] = field(default_factory=list)
    available_licenses: List[LicenseType] = field(default_factory=list)
    
    def apply_filters(self, filtered_datasets: List[DatasetCard]) -> None:
        """Update datasets after applying filters."""
        self.datasets = filtered_datasets
        self.pagination.total_items = len(filtered_datasets)
        self.pagination.current_page = 1
    
    def get_visible_datasets(self) -> List[DatasetCard]:
        """Get datasets for current page."""
        start = self.pagination.offset
        end = start + self.pagination.page_size
        return self.datasets[start:end]
    
    def next_page(self) -> bool:
        """Advance to next page. Returns True if successful."""
        if self.pagination.has_next:
            self.pagination.current_page += 1
            return True
        return False
    
    def previous_page(self) -> bool:
        """Go to previous page. Returns True if successful."""
        if self.pagination.has_previous:
            self.pagination.current_page -= 1
            return True
        return False
    
    def jump_to_page(self, page: int) -> bool:
        """Jump to specific page. Returns True if valid."""
        if 1 <= page <= self.pagination.total_pages:
            self.pagination.current_page = page
            return True
        return False
    
    def change_page_size(self, size: int) -> None:
        """Change page size and reset to first page."""
        self.pagination.page_size = size
        self.pagination.current_page = 1
