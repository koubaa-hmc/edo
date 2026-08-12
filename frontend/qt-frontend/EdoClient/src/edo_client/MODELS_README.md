# EDO Client - Models & ViewModels

This directory contains the data model and view model implementation for the EDO Desktop Client, following the **Model-Driven User Interface Development (MDUID)** specification.

## Quick Start

### Using Data Models

```python
from edo_client.models import DatasetCard, CatalogModel
from datetime import datetime

# Create a dataset card
card = DatasetCard(
    title="Energy Consumption Data 2025",
    doi="10.1234/energy.2025.001",
    publication_date=datetime.now(),
    license=LicenseType.CC_BY,
)

# Use in catalog
catalog = CatalogModel()
catalog.datasets = [card]
catalog.apply_filters([card])
```

### Using ViewModels (for QML)

```python
from edo_client.viewmodels import CatalogViewModel
from PyQt6.QtCore import QTimer

# Create view model
vm = CatalogViewModel()

# Load data
vm.load_datasets([...])  # List of dicts from backend

# Bind to QML context
engine.rootContext().setContextProperty("catalogVM", vm)
```

## Directory Structure

```
src/edo_client/
├── models/                    # Platform-independent data models
│   ├── catalog.py            # BrowseCatalog (Abstract Model Tree 1)
│   ├── metadata.py           # Create/Edit Metadata (Trees 3 & 4)
│   ├── review.py             # Review Dashboard/Detail (Trees 5 & 6)
│   ├── user.py               # User profiles & roles
│   ├── platform.py           # Platform Configuration (Tree 7)
│   └── MODEL_ARCHITECTURE.md # Architecture documentation
│
└── viewmodels/               # Qt-specific view models for QML
    ├── catalog_vm.py         # CatalogViewModel
    ├── metadata_vm.py        # MetadataViewModel (wizard)
    ├── review_vm.py          # ReviewViewModel
    ├── dataset_detail_vm.py  # DatasetDetailViewModel
    ├── platform_vm.py        # PlatformViewModel
    └── VIEWMODEL_GUIDE.md    # Implementation guide
```

## Key Concepts

### Abstract Model Trees

Each major UI component corresponds to an Abstract Model Tree from the MDUID spec:

| Tree | Component | Files |
|------|-----------|-------|
| 1 | BrowseCatalog | `models/catalog.py`, `viewmodels/catalog_vm.py` |
| 2 | ViewDatasetDetail | `viewmodels/dataset_detail_vm.py` |
| 3 | CreateMetadataWizard | `models/metadata.py`, `viewmodels/metadata_vm.py` |
| 4 | EditMetadata | (shared with Tree 3) |
| 5 | ReviewDashboard | `models/review.py`, `viewmodels/review_vm.py` |
| 6 | ReviewDetail | (shared with Tree 5) |
| 7 | PlatformConfiguration | `models/platform.py`, `viewmodels/platform_vm.py` |

### Role-Based Access

All models respect role constraints:

```python
from edo_client.core.role_registry import get_role_registry

registry = get_role_registry()
policy = registry.get_policy("research_fellow")

# Check permission
if policy.has_permission(Permission.CREATE_METADATA):
    # Show metadata creation wizard
```

### Validation

Models include built-in validation:

```python
from edo_client.models.metadata import MetadataField, FieldDataType

field = MetadataField(
    field_id="title",
    display_name="Title",
    required=True,
    min_length=10
)
field.value = "Short"

errors = field.validate()
if errors:
    print(f"Validation failed: {errors[0].message}")
```

### RO-Crate Generation (CF3)

Generate FAIR-compliant RO-Crate packages:

```python
from edo_client.models.metadata import MetadataModel

model = MetadataModel(title="My Dataset")
# ... add sections and fields ...

crate = model.to_ro_crate()
print(crate["@graph"][1]["name"])  # Dataset name
```

## Documentation

- **[MODEL_ARCHITECTURE.md](models/MODEL_ARCHITECTURE.md)** - Overall architecture and mapping to Abstract Model Trees
- **[VIEWMODEL_GUIDE.md](viewmodels/VIEWMODEL_GUIDE.md)** - How to create and use ViewModels with QML
- **[IMPLEMENTATION_SUMMARY.md](../../IMPLEMENTATION_SUMMARY.md)** - What's implemented and what's pending

## Testing

Run unit tests:

```bash
cd /Users/ot2661/Documents/01_dev/edo/frontend/qt-frontend/EdoClient
pytest tests/test_models.py -v
pytest tests/test_viewmodels.py -v
```

## Integration with Existing Code

The new models integrate with existing components:

- **Backend Bridge**: `core/backend_bridge.py` - Execute async actions
- **Role Registry**: `core/role_registry.py` - Permission checks
- **Widget Factory**: `core/widget_factory.py` - Dynamic widget creation

Example integration:

```python
from edo_client.core.backend_bridge import get_backend_bridge

bridge = get_backend_bridge()
result = await bridge.execute("data.import", path="/path/to/data.csv")

if result.is_success:
    catalog_vm.load_datasets(result.data)
```

## Next Steps

1. **Create QML Views** - Bind ViewModels to QML components
2. **Connect Backend** - Replace demo handlers with real API calls
3. **Add Tests** - Unit tests for models and integration tests for ViewModels
4. **Implement System Admin** - Complete Abstract Model Tree 8

See [IMPLEMENTATION_SUMMARY.md](../../IMPLEMENTATION_SUMMARY.md) for details.

---

**Version**: 0.1.0  
**Last Updated**: 2026-08-12
