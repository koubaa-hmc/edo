#!/usr/bin/env python3
"""
Unit tests for EDO Client data models.

These tests verify the platform-independent business logic in the models package.
Run with: pytest tests/test_models.py -v
"""

import pytest
from datetime import datetime, timedelta

# Import models directly (avoid PyQt6 dependency in tests)
import sys
from pathlib import Path
from importlib import import_module

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import model modules using importlib to avoid conflicts
_catalog = import_module("edo_client.models.catalog")
_metadata = import_module("edo_client.models.metadata")
_review = import_module("edo_client.models.review")
_user = import_module("edo_client.models.user")
_platform = import_module("edo_client.models.platform")

# Extract classes for testing
DatasetCard = _catalog.DatasetCard
CatalogModel = _catalog.CatalogModel
FilterState = _catalog.FilterState
AccessType = _catalog.AccessType
LicenseType = _catalog.LicenseType
Author = _catalog.Author

MetadataField = _metadata.MetadataField
MetadataSection = _metadata.MetadataSection
MetadataModel = _metadata.MetadataModel
FieldDataType = _metadata.FieldDataType
ValidationLevel = _metadata.ValidationLevel

ReviewItem = _review.ReviewItem
ReviewQueueModel = _review.ReviewQueueModel
ReviewStatus = _review.ReviewStatus
ValidationReport = _review.ValidationReport
FAIRScore = _review.FAIRScore
RevisionIssue = _review.RevisionIssue

UserProfile = _user.UserProfile
UserRole = _user.UserRole
UserRoleType = _user.UserRoleType

PlatformConfig = _platform.PlatformConfig
PlatformMapping = _platform.PlatformMapping
FieldMapping = _platform.FieldMapping
ConnectionStatus = _platform.ConnectionStatus
AuthType = _platform.AuthType


class TestDatasetCard:
    """Test DatasetCard model."""
    
    def test_create_basic_card(self):
        card = DatasetCard(
            title="Test Dataset",
            doi="10.1234/test.001"
        )
        assert card.title == "Test Dataset"
        assert card.doi == "10.1234/test.001"
        assert card.authors == []
        assert card.access_type == AccessType.OPEN
    
    def test_author_names_single(self):
        card = DatasetCard(
            title="Test",
            doi="10.1234/test",
            authors=[Author(name="John Doe")]
        )
        assert card.author_names == "John Doe"
    
    def test_author_names_multiple(self):
        card = DatasetCard(
            title="Test",
            doi="10.1234/test",
            authors=[
                Author(name="John Doe"),
                Author(name="Jane Smith"),
                Author(name="Bob Wilson")
            ]
        )
        assert card.author_names == "John Doe et al."
    
    def test_publication_year(self):
        card = DatasetCard(
            title="Test",
            doi="10.1234/test",
            publication_date=datetime(2025, 6, 15)
        )
        assert card.publication_year == 2025
    
    def test_is_open_access(self):
        open_card = DatasetCard(title="Open", doi="10.1234/open", access_type=AccessType.OPEN)
        restricted_card = DatasetCard(title="Restricted", doi="10.1234/rest", access_type=AccessType.RESTRICTED)
        
        assert open_card.is_open_access is True
        assert restricted_card.is_open_access is False
    
    def test_to_dict(self):
        card = DatasetCard(
            title="Test",
            doi="10.1234/test",
            reuse_count=42,
            domain="Energy"
        )
        d = card.to_dict()
        
        assert d["title"] == "Test"
        assert d["doi"] == "10.1234/test"
        assert d["reuseCount"] == 42
        assert d["domain"] == "Energy"


class TestCatalogModel:
    """Test CatalogModel."""
    
    def test_pagination(self):
        model = CatalogModel()
        model.datasets = [
            DatasetCard(title=f"Dataset {i}", doi=f"10.1234/{i}")
            for i in range(100)
        ]
        model.pagination.total_items = 100
        model.pagination.page_size = 25
        
        assert model.pagination.total_pages == 4
        assert model.pagination.has_next is True
        assert model.pagination.has_previous is False
        
        # Get first page
        visible = model.get_visible_datasets()
        assert len(visible) == 25
        assert visible[0].title == "Dataset 0"
        
        # Next page
        model.next_page()
        assert model.pagination.current_page == 2
        visible = model.get_visible_datasets()
        assert visible[0].title == "Dataset 25"
    
    def test_jump_to_page(self):
        model = CatalogModel()
        model.pagination.total_items = 100
        model.pagination.page_size = 25
        
        assert model.jump_to_page(3) is True
        assert model.pagination.current_page == 3
        
        assert model.jump_to_page(10) is False  # Invalid page
    
    def test_change_page_size(self):
        model = CatalogModel()
        model.pagination.total_items = 100
        model.pagination.page_size = 25
        model.pagination.current_page = 3
        
        model.change_page_size(50)
        assert model.pagination.page_size == 50
        assert model.pagination.current_page == 1  # Reset to first page


class TestMetadataField:
    """Test MetadataField validation."""
    
    def test_required_field_empty(self):
        field = MetadataField(
            field_id="title",
            display_name="Title",
            required=True
        )
        field.value = ""
        
        errors = field.validate()
        assert len(errors) == 1
        assert errors[0].level == ValidationLevel.ERROR
        assert "required" in errors[0].message.lower()
    
    def test_min_length_validation(self):
        field = MetadataField(
            field_id="title",
            display_name="Title",
            min_length=10
        )
        field.value = "Short"
        
        errors = field.validate()
        assert len(errors) == 1
        assert "at least 10" in errors[0].message
    
    def test_max_length_validation(self):
        field = MetadataField(
            field_id="title",
            display_name="Title",
            max_length=5
        )
        field.value = "This is too long"
        
        errors = field.validate()
        assert len(errors) == 1
        assert "cannot exceed 5" in errors[0].message
    
    def test_valid_field(self):
        field = MetadataField(
            field_id="title",
            display_name="Title",
            required=True,
            min_length=5
        )
        field.value = "Valid Title"
        
        errors = field.validate()
        assert len(errors) == 0
    
    def test_reset_field(self):
        field = MetadataField(
            field_id="title",
            display_name="Title",
            default_value="Default"
        )
        field.value = "Modified"
        field.is_dirty = True
        
        field.reset()
        
        assert field.value == "Default"
        assert field.is_dirty is False


class TestMetadataSection:
    """Test MetadataSection."""
    
    def test_completeness_score(self):
        section = MetadataSection(
            section_id="identification",
            title="Identification"
        )
        
        # Add required fields
        field1 = MetadataField(field_id="title", display_name="Title", required=True)
        field2 = MetadataField(field_id="doi", display_name="DOI", required=True)
        
        section.add_field(field1)
        section.add_field(field2)
        
        # Empty section = 0% complete
        assert section.get_completeness_score() == 0.0
        
        # Fill one field = 50% complete
        field1.value = "My Title"
        assert section.get_completeness_score() == 0.5
        
        # Fill both = 100% complete
        field2.value = "10.1234/test"
        assert section.get_completeness_score() == 1.0


class TestReviewItem:
    """Test ReviewItem."""
    
    def test_assign_review(self):
        item = ReviewItem(
            review_id="rev_001",
            dataset_id="ds_001",
            dataset_title="Test Dataset",
            submitter_name="John Doe"
        )
        
        assert item.status == ReviewStatus.PENDING
        assert item.assigned_to is None
        
        item.assign_to("steward_001")
        
        assert item.status == ReviewStatus.IN_REVIEW
        assert item.assigned_to == "steward_001"
        assert item.assigned_at is not None
    
    def test_approve_review(self):
        item = ReviewItem(
            review_id="rev_001",
            dataset_id="ds_001",
            dataset_title="Test",
            submitter_name="Test User"
        )
        
        item.approve("Looks good!")
        
        assert item.status == ReviewStatus.APPROVED
        assert item.decision == "approved"
        assert item.decision_notes == "Looks good!"
    
    def test_request_revisions(self):
        item = ReviewItem(
            review_id="rev_001",
            dataset_id="ds_001",
            dataset_title="Test",
            submitter_name="Test User"
        )
        
        from edo_client.models.review import RevisionIssue
        
        issues = [
            RevisionIssue(
                issue_id="issue_001",
                field_reference="title",
                description="Title is too short"
            )
        ]
        
        due_date = datetime.now() + timedelta(days=7)
        item.request_revisions(issues, due_date, "Please fix the issues")
        
        assert item.status == ReviewStatus.REVISIONS_REQUESTED
        assert len(item.revision_issues) == 1
        assert item.revision_due_date is not None
    
    def test_days_in_review(self):
        item = ReviewItem(
            review_id="rev_001",
            dataset_id="ds_001",
            dataset_title="Test",
            submitter_name="Test User",
            submission_date=datetime.now() - timedelta(days=5)
        )
        
        assert item.days_in_review() == 5
    
    def test_is_overdue(self):
        # Overdue by deadline
        item = ReviewItem(
            review_id="rev_001",
            dataset_id="ds_001",
            dataset_title="Test",
            submitter_name="Test User",
            revision_due_date=datetime.now() - timedelta(days=1)
        )
        assert item.is_overdue() is True
        
        # Not overdue yet
        item.revision_due_date = datetime.now() + timedelta(days=1)
        assert item.is_overdue() is False


class TestUserProfile:
    """Test UserProfile and roles."""
    
    def test_guest_permissions(self):
        user = UserProfile(
            user_id="user_001",
            username="guest",
            email="guest@example.com",
            display_name="Guest User",
            role=UserRoleType.GUEST_VIEWER
        )
        
        assert user.can_perform_action("browse") is True
        assert user.can_perform_action("create_metadata") is False
        assert user.can_perform_action("review") is False
    
    def test_research_fellow_permissions(self):
        user = UserProfile(
            user_id="user_002",
            username="fellow",
            email="fellow@example.com",
            display_name="Research Fellow",
            role=UserRoleType.RESEARCH_FELLOW
        )
        
        assert user.can_perform_action("browse") is True
        assert user.can_perform_action("create_metadata") is True
        assert user.can_perform_action("review") is False
    
    def test_data_steward_permissions(self):
        user = UserProfile(
            user_id="user_003",
            username="steward",
            email="steward@example.com",
            display_name="Data Steward",
            role=UserRoleType.DATA_STEWARD
        )
        
        assert user.can_perform_action("browse") is True
        assert user.can_perform_action("create_metadata") is True
        assert user.can_perform_action("review") is True
        assert user.can_perform_action("approve") is True
    
    def test_admin_permissions(self):
        user = UserProfile(
            user_id="user_004",
            username="admin",
            email="admin@example.com",
            display_name="Admin",
            role=UserRoleType.ADMIN
        )
        
        # Admin has all permissions
        assert user.can_perform_action("anything") is True


class TestPlatformConfig:
    """Test PlatformConfig."""
    
    def test_test_connection_no_endpoint(self):
        platform = PlatformConfig(
            platform_id="platform_001",
            platform_name="Test Platform"
        )
        
        success = platform.test_connection()
        
        assert success is False
        assert platform.connection_status == ConnectionStatus.ERROR
    
    def test_test_connection_success(self):
        platform = PlatformConfig(
            platform_id="platform_001",
            platform_name="Test Platform",
            api_endpoint="https://api.example.com"
        )
        
        success = platform.test_connection()
        
        assert success is True
        assert platform.connection_status == ConnectionStatus.CONNECTED
    
    def test_can_publish(self):
        from edo_client.models.platform import ConnectionStatus
        
        platform = PlatformConfig(
            platform_id="platform_001",
            platform_name="Test Platform",
            api_endpoint="https://api.example.com",
            plugin_installed=True,
            is_enabled=True
        )
        platform.mapping = PlatformMapping(
            mapping_id="map_001",
            platform_id="platform_001",
            source_schema="DataCite",
            target_schema="Custom"
        )
        # Set connection status to CONNECTED (required for can_publish)
        platform.connection_status = ConnectionStatus.CONNECTED
        
        assert platform.can_publish() is True
    
    def test_field_mapping_transformation(self):
        mapping = FieldMapping(
            source_field="title",
            target_field="datasetTitle",
            transformation_rule="uppercase"
        )
        
        result = mapping.apply_transformation("hello world")
        assert result == "HELLO WORLD"
    
    def test_transform_data(self):
        platform_mapping = PlatformMapping(
            mapping_id="map_001",
            platform_id="platform_001",
            source_schema="EDO",
            target_schema="Target"
        )
        
        platform_mapping.add_mapping(FieldMapping(
            source_field="title",
            target_field="datasetTitle",
            transformation_rule="uppercase"
        ))
        platform_mapping.add_mapping(FieldMapping(
            source_field="doi",
            target_field="identifier"
        ))
        
        source_data = {
            "title": "My Dataset",
            "doi": "10.1234/test"
        }
        
        target_data = platform_mapping.transform_data(source_data)
        
        assert target_data["datasetTitle"] == "MY DATASET"
        assert target_data["identifier"] == "10.1234/test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
