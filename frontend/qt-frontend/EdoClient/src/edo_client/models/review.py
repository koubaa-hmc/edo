"""
Review Models - Abstract Model Trees 5 & 6: ReviewDashboard & ReviewDetail

Supports CF2, CF3, CF4 for FAIR Phase: PRESERVE
Primary Roles: data_steward
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum


class ReviewStatus(Enum):
    """Status of a metadata review item."""
    PENDING = "pending"
    IN_REVIEW = "in-review"
    APPROVED = "approved"
    REVISIONS_REQUESTED = "revisions-requested"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class FAIRnessDimension(Enum):
    """FAIR principle dimensions."""
    FINDABLE = "F"
    ACCESSIBLE = "A"
    INTEROPERABLE = "I"
    REUSABLE = "R"


@dataclass
class FAIRScore:
    """FAIRness scoring breakdown."""
    findable: float = 0.0
    accessible: float = 0.0
    interoperable: float = 0.0
    reusable: float = 0.0
    
    @property
    def overall(self) -> float:
        """Calculate overall FAIR score (average)."""
        return (self.findable + self.accessible + self.interoperable + self.reusable) / 4
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "findable": self.findable,
            "accessible": self.accessible,
            "interoperable": self.interoperable,
            "reusable": self.reusable,
            "overall": self.overall
        }


@dataclass
class ValidationReport:
    """Validation report for a dataset submission."""
    schema_validation_passed: bool = True
    schema_errors: List[str] = field(default_factory=list)
    fair_score: FAIRScore = field(default_factory=FAIRScore)
    quality_warnings: List[str] = field(default_factory=list)
    quality_errors: List[str] = field(default_factory=list)
    completeness_percentage: float = 0.0
    
    def has_errors(self) -> bool:
        return bool(self.schema_errors or self.quality_errors)
    
    def has_warnings(self) -> bool:
        return bool(self.quality_warnings)
    
    def is_acceptable(self) -> bool:
        """Check if submission meets minimum quality threshold."""
        return not self.has_errors() and self.completeness_percentage >= 80.0


@dataclass
class ReviewChecklistItem:
    """Individual checklist item for reviewers."""
    item_id: str
    description: str
    is_checked: bool = False
    notes: Optional[str] = None
    required: bool = False
    
    def toggle(self) -> None:
        """Toggle checked state."""
        self.is_checked = not self.is_checked


@dataclass
class RevisionIssue:
    """Specific issue requiring revision."""
    issue_id: str
    field_reference: Optional[str] = None
    description: str = ""
    suggested_fix: Optional[str] = None
    is_resolved: bool = False
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None


@dataclass
class Correspondence:
    """Message between reviewer and submitter."""
    message_id: str
    from_role: str  # "reviewer" | "submitter"
    message: str
    timestamp: datetime
    is_internal: bool = False  # Internal notes not visible to submitter
    attachments: List[str] = field(default_factory=list)


@dataclass
class ActivityEvent:
    """Timeline activity event."""
    event_id: str
    event_type: str  # submitted | assigned | review_started | correspondence | decision
    description: str
    actor: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReviewItem:
    """
    Single item in the review queue.
    
    Corresponds to AbstractUI: ReviewDashboard → ReviewQueueTable → QueueRows
    """
    review_id: str
    dataset_id: str
    dataset_title: str
    submitter_name: str
    submitter_orcid: Optional[str] = None
    submitter_email: Optional[str] = None
    submission_date: datetime = field(default_factory=datetime.now)
    domain: Optional[str] = None
    status: ReviewStatus = ReviewStatus.PENDING
    assigned_to: Optional[str] = None
    assigned_at: Optional[datetime] = None
    
    # Scoring
    completeness_score: float = 0.0
    validation_report: Optional[ValidationReport] = None
    
    # Review content
    checklist: List[ReviewChecklistItem] = field(default_factory=list)
    revision_issues: List[RevisionIssue] = field(default_factory=list)
    correspondence: List[Correspondence] = field(default_factory=list)
    internal_notes: List[str] = field(default_factory=list)
    
    # Timeline
    activity_log: List[ActivityEvent] = field(default_factory=list)
    
    # Decision
    decision: Optional[str] = None
    decision_date: Optional[datetime] = None
    decision_notes: Optional[str] = None
    
    # Deadlines
    revision_due_date: Optional[datetime] = None
    
    def add_event(self, event_type: str, description: str, actor: Optional[str] = None) -> None:
        """Add an activity event to the timeline."""
        event = ActivityEvent(
            event_id=f"evt_{len(self.activity_log) + 1}",
            event_type=event_type,
            description=description,
            actor=actor or self.assigned_to,
            timestamp=datetime.now()
        )
        self.activity_log.append(event)
    
    def assign_to(self, reviewer_id: str) -> None:
        """Assign review to a steward."""
        self.assigned_to = reviewer_id
        self.assigned_at = datetime.now()
        self.status = ReviewStatus.IN_REVIEW
        self.add_event("assigned", f"Assigned to {reviewer_id}", "system")
    
    def add_correspondence(self, message: str, from_role: str, is_internal: bool = False) -> None:
        """Add a message to the correspondence thread."""
        msg = Correspondence(
            message_id=f"msg_{len(self.correspondence) + 1}",
            from_role=from_role,
            message=message,
            timestamp=datetime.now(),
            is_internal=is_internal
        )
        self.correspondence.append(msg)
        
        if not is_internal:
            self.add_event("correspondence", f"Message sent to {from_role}", from_role)
    
    def request_revisions(
        self,
        issues: List[RevisionIssue],
        due_date: datetime,
        message: str
    ) -> None:
        """Request revisions from submitter."""
        self.revision_issues.extend(issues)
        self.revision_due_date = due_date
        self.status = ReviewStatus.REVISIONS_REQUESTED
        self.decision = "revisions_requested"
        self.decision_date = datetime.now()
        self.decision_notes = message
        
        self.add_event("decision", "Revisions requested", self.assigned_to)
        self.add_correspondence(message, "reviewer")
    
    def approve(self, notes: Optional[str] = None) -> None:
        """Approve the submission."""
        self.status = ReviewStatus.APPROVED
        self.decision = "approved"
        self.decision_date = datetime.now()
        self.decision_notes = notes or "Approved for publication"
        
        self.add_event("decision", "Approved", self.assigned_to)
    
    def reject(self, reason: str) -> None:
        """Reject the submission."""
        self.status = ReviewStatus.REJECTED
        self.decision = "rejected"
        self.decision_date = datetime.now()
        self.decision_notes = reason
        
        self.add_event("decision", f"Rejected: {reason}", self.assigned_to)
        self.add_correspondence(reason, "reviewer")
    
    def get_unresolved_issues(self) -> List[RevisionIssue]:
        """Get list of unresolved revision issues."""
        return [i for i in self.revision_issues if not i.is_resolved]
    
    def days_in_review(self) -> int:
        """Calculate days since submission."""
        delta = datetime.now() - self.submission_date
        return delta.days
    
    def days_until_due(self) -> Optional[int]:
        """Calculate days until revision deadline."""
        if not self.revision_due_date:
            return None
        delta = self.revision_due_date - datetime.now()
        return delta.days
    
    def is_overdue(self) -> bool:
        """Check if review is overdue."""
        if self.revision_due_date:
            return datetime.now() > self.revision_due_date
        # Consider pending reviews older than 14 days as overdue
        return self.days_in_review() > 14
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for UI serialization."""
        return {
            "reviewId": self.review_id,
            "datasetId": self.dataset_id,
            "datasetTitle": self.dataset_title,
            "submitterName": self.submitter_name,
            "submitterOrcid": self.submitter_orcid,
            "submissionDate": self.submission_date.isoformat(),
            "domain": self.domain,
            "status": self.status.value,
            "assignedTo": self.assigned_to,
            "completenessScore": self.completeness_score,
            "fairScore": self.validation_report.fair_score.to_dict() if self.validation_report else None,
            "daysInReview": self.days_in_review(),
            "isOverdue": self.is_overdue(),
            "unresolvedIssuesCount": len(self.get_unresolved_issues()),
        }


@dataclass
class ReviewQueueStats:
    """Statistics for review dashboard."""
    pending_count: int = 0
    in_review_count: int = 0
    approved_count: int = 0
    revisions_requested_count: int = 0
    rejected_count: int = 0
    
    @property
    def total_count(self) -> int:
        return (
            self.pending_count +
            self.in_review_count +
            self.approved_count +
            self.revisions_requested_count +
            self.rejected_count
        )
    
    @property
    def approval_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        decisions_made = self.approved_count + self.rejected_count
        if decisions_made == 0:
            return 0.0
        return self.approved_count / decisions_made
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pendingCount": self.pending_count,
            "inReviewCount": self.in_review_count,
            "approvedCount": self.approved_count,
            "revisionsRequestedCount": self.revisions_requested_count,
            "rejectedCount": self.rejected_count,
            "totalCount": self.total_count,
            "approvalRate": self.approval_rate,
        }


@dataclass
class ReviewQueueModel:
    """
    Complete review queue model.
    
    Corresponds to AbstractUI: ReviewDashboard
    """
    items: List[ReviewItem] = field(default_factory=list)
    stats: ReviewQueueStats = field(default_factory=ReviewQueueStats)
    isLoading: bool = False
    error: Optional[str] = None
    
    # Filter state
    status_filter: Optional[ReviewStatus] = None
    domain_filter: Optional[str] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None
    researcher_filter: Optional[str] = None
    
    # Sorting
    sort_by: str = "submission_date"  # title | submitter | date | domain | score | status
    sort_ascending: bool = False
    
    # Selection
    selected_review_ids: List[str] = field(default_factory=list)
    
    def calculate_stats(self) -> None:
        """Recalculate queue statistics."""
        stats = ReviewQueueStats()
        for item in self.items:
            if item.status == ReviewStatus.PENDING:
                stats.pending_count += 1
            elif item.status == ReviewStatus.IN_REVIEW:
                stats.in_review_count += 1
            elif item.status == ReviewStatus.APPROVED:
                stats.approved_count += 1
            elif item.status == ReviewStatus.REVISIONS_REQUESTED:
                stats.revisions_requested_count += 1
            elif item.status == ReviewStatus.REJECTED:
                stats.rejected_count += 1
        self.stats = stats
    
    def apply_filters(self) -> List[ReviewItem]:
        """Apply current filters and return filtered items."""
        filtered = self.items.copy()
        
        if self.status_filter:
            filtered = [i for i in filtered if i.status == self.status_filter]
        
        if self.domain_filter:
            filtered = [i for i in filtered if i.domain == self.domain_filter]
        
        if self.date_range_start:
            filtered = [i for i in filtered if i.submission_date >= self.date_range_start]
        
        if self.date_range_end:
            filtered = [i for i in filtered if i.submission_date <= self.date_range_end]
        
        if self.researcher_filter:
            filtered = [
                i for i in filtered 
                if self.researcher_filter.lower() in i.submitter_name.lower()
            ]
        
        return filtered
    
    def sort_items(self, items: List[ReviewItem]) -> List[ReviewItem]:
        """Sort items by current sort settings."""
        key_map = {
            "title": lambda x: x.dataset_title.lower(),
            "submitter": lambda x: x.submitter_name.lower(),
            "date": lambda x: x.submission_date,
            "domain": lambda x: x.domain or "",
            "score": lambda x: x.completeness_score,
            "status": lambda x: x.status.value,
        }
        
        key_func = key_map.get(self.sort_by, lambda x: x.submission_date)
        return sorted(items, key=key_func, reverse=not self.sort_ascending)
    
    def get_visible_items(self) -> List[ReviewItem]:
        """Get filtered and sorted items for display."""
        filtered = self.apply_filters()
        return self.sort_items(filtered)
    
    def toggle_selection(self, review_id: str) -> None:
        """Toggle selection of a review item."""
        if review_id in self.selected_review_ids:
            self.selected_review_ids.remove(review_id)
        else:
            self.selected_review_ids.append(review_id)
    
    def select_all(self) -> None:
        """Select all visible items."""
        visible = self.get_visible_items()
        self.selected_review_ids = [i.review_id for i in visible]
    
    def clear_selection(self) -> None:
        """Clear all selections."""
        self.selected_review_ids = []
    
    def get_selected_items(self) -> List[ReviewItem]:
        """Get currently selected review items."""
        return [i for i in self.items if i.review_id in self.selected_review_ids]
    
    def bulk_assign(self, reviewer_id: str) -> int:
        """Assign all selected items to a reviewer. Returns count."""
        selected = self.get_selected_items()
        for item in selected:
            if item.status == ReviewStatus.PENDING:
                item.assign_to(reviewer_id)
        self.calculate_stats()
        return len(selected)
    
    def refresh(self) -> None:
        """Reset filters and reload."""
        self.status_filter = None
        self.domain_filter = None
        self.date_range_start = None
        self.date_range_end = None
        self.researcher_filter = None
        self.selected_review_ids = []
        self.calculate_stats()
