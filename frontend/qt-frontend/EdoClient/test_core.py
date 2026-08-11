#!/usr/bin/env python3
"""
Core logic tests for EDO Client (no GUI required).

Tests role registry, widget factory, and backend bridge functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_role_registry():
    """Test role registry and permissions."""
    print("\n🧪 Testing Role Registry...")
    
    from edo_client.core.role_registry import RoleRegistry, Permission, get_role_registry
    
    # Get global registry
    registry = get_role_registry()
    
    # Test built-in roles exist
    assert "guest_viewer" in registry.available_roles, "Guest viewer role missing"
    assert "research_fellow" in registry.available_roles, "Research fellow role missing"
    assert "data_steward" in registry.available_roles, "Data steward role missing"
    assert "admin" in registry.available_roles, "Admin role missing"
    print("  ✓ All built-in roles registered")
    
    # Test guest permissions (minimal)
    guest_policy = registry.get_policy("guest_viewer")
    assert guest_policy is not None, "Guest policy not found"
    assert guest_policy.has_permission(Permission.VIEW_DATASETS), "Guest should view datasets"
    assert not guest_policy.has_permission(Permission.IMPORT_DATASETS), "Guest should not import"
    assert not guest_policy.has_permission(Permission.RUN_INGESTION_OEP), "Guest should not ingest"
    print("  ✓ Guest viewer permissions correct")
    
    # Test research fellow permissions
    fellow_policy = registry.get_policy("research_fellow")
    assert fellow_policy.has_permission(Permission.IMPORT_DATASETS), "Fellow should import"
    assert fellow_policy.has_permission(Permission.RUN_SEMANTIC_EXPANSION), "Fellow should expand semantics"
    assert not fellow_policy.has_permission(Permission.RUN_INGESTION_OEP), "Fellow should not ingest OEP"
    print("  ✓ Research fellow permissions correct")
    
    # Test data steward permissions
    steward_policy = registry.get_policy("data_steward")
    assert steward_policy.has_permission(Permission.RUN_INGESTION_OEP), "Steward should ingest OEP"
    assert steward_policy.has_permission(Permission.RUN_INGESTION_HKG), "Steward should ingest HKG"
    assert steward_policy.has_permission(Permission.ACCESS_INGESTION_WORKFLOW), "Steward should access workflow"
    print("  ✓ Data steward permissions correct")
    
    # Test admin permissions (all)
    admin_policy = registry.get_policy("admin")
    for perm in Permission:
        assert admin_policy.has_permission(perm), f"Admin should have {perm}"
    print("  ✓ Admin has all permissions")
    
    # Test effective policy (role combination)
    combined = registry.get_effective_policy(["guest_viewer", "research_fellow"])
    assert combined is not None, "Combined policy should exist"
    print("  ✓ Effective policy combination works")
    
    print("✅ Role Registry tests passed\n")


def test_widget_factory():
    """Test widget factory data type detection."""
    print("🧪 Testing Widget Factory...")
    
    from PyQt6.QtWidgets import QApplication
    from edo_client.core.widget_factory import WidgetFactory, get_widget_factory
    
    # Create QApplication (required for QWidget creation)
    if not QApplication.instance():
        app = QApplication([])
    
    factory = get_widget_factory()
    
    # Test dataset detection
    dataset = {"title": "Test", "description": "Desc", "resources": []}
    widget = factory.get_widget(dataset)
    assert widget is not None, "Should create widget for dataset"
    assert widget.__class__.__name__ == "DatasetBrowser", f"Expected DatasetBrowser, got {widget.__class__.__name__}"
    print("  ✓ Dataset type detected correctly")
    
    # Test timeseries detection
    timeseries = {"timestamps": ["2025-01-01T00:00"], "values": [100]}
    widget = factory.get_widget(timeseries)
    assert widget is not None, "Should create widget for timeseries"
    assert widget.__class__.__name__ == "TimeseriesGrid", f"Expected TimeseriesGrid, got {widget.__class__.__name__}"
    print("  ✓ Timeseries type detected correctly")
    
    # Test RDF detection
    rdf = {"uri": "http://example.org/resource", "@type": "TestClass"}
    widget = factory.get_widget(rdf)
    assert widget is not None, "Should create widget for RDF"
    assert widget.__class__.__name__ == "RDFInspector", f"Expected RDFInspector, got {widget.__class__.__name__}"
    print("  ✓ RDF type detected correctly")
    
    # Test table detection
    table = {"columns": ["a", "b"], "rows": [[1, 2]]}
    widget = factory.get_widget(table)
    assert widget is not None, "Should create widget for table"
    assert widget.__class__.__name__ == "TableViewer", f"Expected TableViewer, got {widget.__class__.__name__}"
    print("  ✓ Table type detected correctly")
    
    # Test fallback for unknown types
    unknown = {"custom": "data"}
    widget = factory.get_widget(unknown)
    assert widget is not None, "Should create fallback widget"
    print("  ✓ Fallback widget created for unknown type")
    
    print("✅ Widget Factory tests passed\n")


def test_backend_bridge():
    """Test backend bridge action registration and execution."""
    print("🧪 Testing Backend Bridge...")
    
    import asyncio
    from edo_client.core.backend_bridge import BackendBridge, get_backend_bridge, ActionResultStatus
    
    bridge = get_backend_bridge()
    
    # Test action registration
    actions = bridge.get_available_actions()
    assert len(actions) > 0, "Should have registered actions"
    print(f"  ✓ {len(actions)} actions registered")
    
    # Test specific actions exist
    action_ids = [a.action_id for a in actions]
    assert "data.import" in action_ids, "data.import action missing"
    assert "ingestion.oep.get_metadata" in action_ids, "OEP metadata action missing"
    assert "semantic.expand" in action_ids, "Semantic expand action missing"
    print("  ✓ Key actions registered")
    
    # Test action execution (demo handler)
    async def test_execution():
        result = await bridge.execute("data.validate")
        assert result.is_success, "Validation should succeed"
        assert result.status == ActionResultStatus.SUCCESS, "Status should be success"
        return result
    
    result = asyncio.run(test_execution())
    print(f"  ✓ Action execution works: {result.message}")
    
    # Test unknown action
    async def test_unknown():
        result = await bridge.execute("nonexistent.action")
        return result
    
    result = asyncio.run(test_unknown())
    assert not result.is_success, "Unknown action should fail"
    assert result.error is not None, "Error message should be present"
    print("  ✓ Unknown action handled correctly")
    
    print("✅ Backend Bridge tests passed\n")


def test_demo_data():
    """Test demo data generation."""
    print("🧪 Testing Demo Data...")
    
    # Import test helpers
    import test_ui as test_helpers
    
    # Test dataset structure
    dataset = test_helpers.get_demo_dataset()
    assert "title" in dataset, "Dataset should have title"
    assert "resources" in dataset, "Dataset should have resources"
    assert len(dataset["resources"]) > 0, "Dataset should have at least one resource"
    print("  ✓ Demo dataset structure valid")
    
    # Test timeseries structure
    ts = test_helpers.get_demo_timeseries()
    assert "timestamps" in ts, "Timeseries should have timestamps"
    assert "values" in ts, "Timeseries should have values"
    assert len(ts["timestamps"]) == len(ts["values"]), "Timestamps and values should match"
    print(f"  ✓ Demo timeseries has {len(ts['timestamps'])} data points")
    
    # Test RDF structure
    rdf = test_helpers.get_demo_rdf()
    assert "uri" in rdf or "@id" in rdf, "RDF should have URI or @id"
    assert "@type" in rdf, "RDF should have @type"
    print("  ✓ Demo RDF structure valid")
    
    print("✅ Demo Data tests passed\n")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EDO Client - Core Logic Tests")
    print("="*60)
    
    try:
        test_role_registry()
        test_widget_factory()
        test_backend_bridge()
        test_demo_data()
        
        print("="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
