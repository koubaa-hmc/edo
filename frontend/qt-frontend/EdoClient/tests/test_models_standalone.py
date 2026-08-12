#!/usr/bin/env python3
"""
Standalone unit tests for EDO Client data models.

These tests verify the platform-independent business logic without PyQt6 dependencies.
Run with: python3 tests/test_models_standalone.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add models directory directly to path (bypass edo_client.__init__ which imports PyQt6)
models_path = Path(__file__).parent.parent / "src" / "edo_client" / "models"
sys.path.insert(0, str(models_path))


def test_dataset_card():
    """Test DatasetCard model."""
    # Import module directly
    import catalog
    DatasetCard = catalog.DatasetCard
    AccessType = catalog.AccessType
    LicenseType = catalog.LicenseType
    Author = catalog.Author
    
    # Basic card
    card = DatasetCard(
        title="Test Dataset",
        doi="10.1234/test.001"
    )
    assert card.title == "Test Dataset"
    assert card.doi == "10.1234/test.001"
    assert card.authors == []
    assert card.access_type == AccessType.OPEN
    print("✓ Basic card creation")
    
    # Author names
    card.authors = [Author(name="John Doe")]
    assert card.author_names == "John Doe"
    
    card.authors = [
        Author(name="John Doe"),
        Author(name="Jane Smith"),
        Author(name="Bob Wilson")
    ]
    assert card.author_names == "John Doe et al."
    print("✓ Author name formatting")
    
    # Publication year
    card.publication_date = datetime(2025, 6, 15)
    assert card.publication_year == 2025
    print("✓ Publication year extraction")
    
    # Open access check
    open_card = DatasetCard(title="Open", doi="10.1234/open", access_type=AccessType.OPEN)
    restricted_card = DatasetCard(title="Restricted", doi="10.1234/rest", access_type=AccessType.RESTRICTED)
    assert open_card.is_open_access is True
    assert restricted_card.is_open_access is False
    print("✓ Open access detection")
    
    # Serialization
    d = card.to_dict()
    assert d["title"] == "Test Dataset"
    assert d["doi"] == "10.1234/test.001"
    print("✓ Dictionary serialization")


def test_catalog_pagination():
    """Test CatalogModel pagination."""
    import catalog
    CatalogModel = catalog.CatalogModel
    DatasetCard = catalog.DatasetCard
    
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
    print("✓ Pagination calculation")
    
    # Get first page
    visible = model.get_visible_datasets()
    assert len(visible) == 25
    assert visible[0].title == "Dataset 0"
    print("✓ First page retrieval")
    
    # Next page
    model.next_page()
    assert model.pagination.current_page == 2
    visible = model.get_visible_datasets()
    assert visible[0].title == "Dataset 25"
    print("✓ Page navigation")
    
    # Jump to page
    assert model.jump_to_page(3) is True
    assert model.pagination.current_page == 3
    assert model.jump_to_page(10) is False  # Invalid
    print("✓ Jump to page")


def test_metadata_validation():
    """Test MetadataField validation."""
    import metadata
    MetadataField = metadata.MetadataField
    FieldDataType = metadata.FieldDataType
    ValidationLevel = metadata.ValidationLevel
    
    # Required field empty
    field = MetadataField(field_id="title", display_name="Title", required=True)
    field.value = ""
    errors = field.validate()
    assert len(errors) == 1
    assert errors[0].level == ValidationLevel.ERROR
    assert "required" in errors[0].message.lower()
    print("✓ Required field validation")
    
    # Min length
    field = MetadataField(field_id="title", display_name="Title", min_length=10)
    field.value = "Short"
    errors = field.validate()
    assert len(errors) == 1
    assert "at least 10" in errors[0].message
    print("✓ Minimum length validation")
    
    # Max length
    field = MetadataField(field_id="title", display_name="Title", max_length=5)
    field.value = "This is too long"
    errors = field.validate()
    assert "cannot exceed 5" in errors[0].message
    print("✓ Maximum length validation")
    
    # Valid field
    field = MetadataField(field_id="title", display_name="Title", required=True, min_length=5)
    field.value = "Valid Title"
    errors = field.validate()
    assert len(errors) == 0
    print("✓ Valid field passes validation")
    
    # Reset
    field = MetadataField(field_id="title", display_name="Title", default_value="Default")
    field.value = "Modified"
    field.is_dirty = True
    field.reset()
    assert field.value == "Default"
    assert field.is_dirty is False
    print("✓ Field reset")


def test_section_completeness():
    """Test MetadataSection completeness scoring."""
    import metadata
    MetadataSection = metadata.MetadataSection
    MetadataField = metadata.MetadataField
    
    section = MetadataSection(section_id="identification", title="Identification")
    
    # Add required fields
    field1 = MetadataField(field_id="title", display_name="Title", required=True)
    field2 = MetadataField(field_id="doi", display_name="DOI", required=True)
    section.add_field(field1)
    section.add_field(field2)
    
    # Empty = 0%
    assert section.get_completeness_score() == 0.0
    print("✓ Empty section score")
    
    # Half filled = 50%
    field1.value = "My Title"
    assert section.get_completeness_score() == 0.5
    print("✓ Partial completion score")
    
    # Full = 100%
    field2.value = "10.1234/test"
    assert section.get_completeness_score() == 1.0
    print("✓ Complete section score")


def test_review_workflow():
    """Test ReviewItem workflow."""
    import review
    ReviewItem = review.ReviewItem
    ReviewStatus = review.ReviewStatus
    RevisionIssue = review.RevisionIssue
    
    item = ReviewItem(
        review_id="rev_001",
        dataset_id="ds_001",
        dataset_title="Test Dataset",
        submitter_name="John Doe"
    )
    
    # Initial state
    assert item.status == ReviewStatus.PENDING
    assert item.assigned_to is None
    print("✓ Initial review state")
    
    # Assign
    item.assign_to("steward_001")
    assert item.status == ReviewStatus.IN_REVIEW
    assert item.assigned_to == "steward_001"
    print("✓ Review assignment")
    
    # Approve
    item.approve("Looks good!")
    assert item.status == ReviewStatus.APPROVED
    assert item.decision == "approved"
    print("✓ Review approval")
    
    # Request revisions (new item)
    item2 = ReviewItem(review_id="rev_002", dataset_id="ds_002", dataset_title="Test 2", submitter_name="Jane Doe")
    issues = [RevisionIssue(issue_id="issue_001", field_reference="title", description="Too short")]
    due_date = datetime.now() + timedelta(days=7)
    item2.request_revisions(issues, due_date, "Please fix")
    assert item2.status == ReviewStatus.REVISIONS_REQUESTED
    assert len(item2.revision_issues) == 1
    print("✓ Revision request")
    
    # Days in review
    item3 = ReviewItem(
        review_id="rev_003",
        dataset_id="ds_003",
        dataset_title="Test 3",
        submitter_name="Bob Smith",
        submission_date=datetime.now() - timedelta(days=5)
    )
    assert item3.days_in_review() == 5
    print("✓ Days in review calculation")


def test_user_roles():
    """Test UserProfile role permissions."""
    import user
    UserProfile = user.UserProfile
    UserRoleType = user.UserRoleType
    
    # Guest
    guest = UserProfile(
        user_id="user_001",
        username="guest",
        email="guest@example.com",
        display_name="Guest",
        role=UserRoleType.GUEST_VIEWER
    )
    assert guest.can_perform_action("browse") is True
    assert guest.can_perform_action("create_metadata") is False
    print("✓ Guest viewer permissions")
    
    # Research Fellow
    fellow = UserProfile(
        user_id="user_002",
        username="fellow",
        email="fellow@example.com",
        display_name="Fellow",
        role=UserRoleType.RESEARCH_FELLOW
    )
    assert fellow.can_perform_action("create_metadata") is True
    assert fellow.can_perform_action("review") is False
    print("✓ Research Fellow permissions")
    
    # Data Steward
    steward = UserProfile(
        user_id="user_003",
        username="steward",
        email="steward@example.com",
        display_name="Steward",
        role=UserRoleType.DATA_STEWARD
    )
    assert steward.can_perform_action("review") is True
    assert steward.can_perform_action("approve") is True
    print("✓ Data Steward permissions")
    
    # Admin
    admin = UserProfile(
        user_id="user_004",
        username="admin",
        email="admin@example.com",
        display_name="Admin",
        role=UserRoleType.ADMIN
    )
    assert admin.can_perform_action("anything") is True
    print("✓ Admin permissions (wildcard)")


def test_platform_config():
    """Test PlatformConfig."""
    import platform as platform_module
    PlatformConfig = platform_module.PlatformConfig
    PlatformMapping = platform_module.PlatformMapping
    FieldMapping = platform_module.FieldMapping
    ConnectionStatus = platform_module.ConnectionStatus
    
    # Test connection without endpoint
    platform = PlatformConfig(platform_id="p1", platform_name="Test")
    success = platform.test_connection()
    assert success is False
    assert platform.connection_status == ConnectionStatus.ERROR
    print("✓ Connection test fails without endpoint")
    
    # Test connection with endpoint
    platform = PlatformConfig(
        platform_id="p2",
        platform_name="Test",
        api_endpoint="https://api.example.com"
    )
    success = platform.test_connection()
    assert success is True
    assert platform.connection_status == ConnectionStatus.CONNECTED
    print("✓ Connection test succeeds with endpoint")
    
    # Can publish check
    platform = PlatformConfig(
        platform_id="p3",
        platform_name="Test",
        api_endpoint="https://api.example.com",
        plugin_installed=True,
        is_enabled=True
    )
    platform.mapping = PlatformMapping(
        mapping_id="map_1",
        platform_id="p3",
        source_schema="DataCite",
        target_schema="Custom"
    )
    # Set connection status manually since test_connection changes it
    platform.connection_status = ConnectionStatus.CONNECTED
    assert platform.can_publish() is True
    print("✓ Can publish check")
    
    # Field transformation
    mapping = FieldMapping(
        source_field="title",
        target_field="datasetTitle",
        transformation_rule="uppercase"
    )
    result = mapping.apply_transformation("hello")
    assert result == "HELLO"
    print("✓ Field transformation (uppercase)")
    
    # Transform data
    pm = PlatformMapping(mapping_id="map_2", platform_id="p4", source_schema="EDO", target_schema="T")
    pm.add_mapping(FieldMapping(source_field="title", target_field="datasetTitle", transformation_rule="uppercase"))
    pm.add_mapping(FieldMapping(source_field="doi", target_field="identifier"))
    
    source_data = {"title": "My Dataset", "doi": "10.1234/test"}
    target_data = pm.transform_data(source_data)
    assert target_data["datasetTitle"] == "MY DATASET"
    assert target_data["identifier"] == "10.1234/test"
    print("✓ Data transformation")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("EDO Client - Model Unit Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Dataset Card", test_dataset_card),
        ("Catalog Pagination", test_catalog_pagination),
        ("Metadata Validation", test_metadata_validation),
        ("Section Completeness", test_section_completeness),
        ("Review Workflow", test_review_workflow),
        ("User Roles", test_user_roles),
        ("Platform Config", test_platform_config),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
            print()
        except Exception as e:
            import traceback
            failed += 1
            print(f"✗ {name} FAILED: {e}")
            traceback.print_exc()
            print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
