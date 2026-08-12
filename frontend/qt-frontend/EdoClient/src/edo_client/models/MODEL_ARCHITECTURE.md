# EDO Client - Model Architecture

## Overview

This document describes the data model and view model architecture implementing the **Abstract Model Trees** from the MDUID specification (`abstract_model_trees.md`).

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    QML / PyQt UI Layer                      │
│  (QML files in qml/EdoClientContent/*.qml)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   ViewModels (viewmodels/)                  │
│  - QObject subclasses with pyqtSignal/pyqtSlot             │
│  - QAbstractListModel for list views                        │
│  - Business logic for UI state management                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Models (models/)                     │
│  - Pure Python dataclasses                                  │
│  - No Qt dependencies                                       │
│  - Serialization support (to_dict methods)                  │
│  - Validation logic                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend Bridge                            │
│  - core/backend_bridge.py                                   │
│  - Async action execution                                   │
│  - Service communication                                    │
└─────────────────────────────────────────────────────────────┘
```

## Model Packages

### `models/` - Data Models

Pure Python dataclasses representing domain entities. These are **platform-independent** and can be used in both PyQt and QML contexts.

| Model | File | Abstract UI Tree | Description |
|-------|------|------------------|-------------|
| `DatasetCard` | `catalog.py` | BrowseCatalog | Dataset metadata for catalog display |
| `CatalogModel` | `catalog.py` | BrowseCatalog | Complete catalog state with filters/pagination |
| `MetadataField` | `metadata.py` | CreateMetadataWizard, EditMetadata | Single metadata field with validation |
| `MetadataSection` | `metadata.py` | CreateMetadataWizard, EditMetadata | Group of related fields |
| `MetadataModel` | `metadata.py` | CreateMetadataWizard, EditMetadata | Complete metadata with RO-Crate support |
| `ReviewItem` | `review.py` | ReviewDashboard, ReviewDetail | Single review submission |
| `ReviewQueueModel` | `review.py` | ReviewDashboard | Complete review queue with bulk actions |
| `UserProfile` | `user.py` | All (auth context) | User profile and roles |
| `PlatformConfig` | `platform.py` | PlatformConfiguration | Target platform configuration |
| `PlatformMapping` | `platform.py` | PlatformConfiguration | Schema mapping between EDO and platforms |

### `viewmodels/` - View Models

Qt-specific wrappers that expose models to QML via properties, signals, and slots.

| ViewModel | QML Exposure | Key Features |
|-----------|--------------|--------------|
| `CatalogViewModel` | `catalog_vm` | Filtering, pagination, dataset selection |
| `MetadataViewModel` | `metadata_vm` | Wizard navigation, validation, RO-Crate generation |
| `ReviewViewModel` | `review_vm` | Queue management, bulk actions, correspondence |
| `DatasetDetailViewModel` | `dataset_detail_vm` | Tabbed view, file access, citation export |
| `PlatformViewModel` | `platform_vm` | Platform CRUD, connection testing, schema mapping |

## Mapping to Abstract Model Trees

### Abstract Model Tree 1: BrowseCatalog

**Files:** `models/catalog.py`, `viewmodels/catalog_vm.py`

```python
# Usage in QML
CatalogViewModel {
    id: catalogVM
    
    ListView {
        model: catalogVM.list_model
        delegate: DatasetCardDelegate {
            onClicked: catalogVM.selectDataset(index)
        }
    }
    
    // Filter controls
    TextField {
        onTextChanged: catalogVM.setSearchQuery(text)
    }
}
```

### Abstract Model Tree 2: ViewDatasetDetail

**Files:** `viewmodels/dataset_detail_vm.py`

Implements tabbed interface with:
- Overview tab
- Metadata tab
- Files tab
- Usage tab
- Similar datasets tab

### Abstract Model Tree 3: CreateMetadataWizard

**Files:** `models/metadata.py`, `viewmodels/metadata_vm.py`

Six-step wizard:
1. Select Template
2. Basic Information
3. Scientific Context
4. Technical Metadata
5. Access & Reuse
6. Target Platforms

Features:
- Step validation before navigation
- Auto-save every 30 seconds
- RO-Crate JSON-LD generation
- Completeness scoring

### Abstract Model Tree 4: EditMetadata

**Files:** Same as CreateMetadataWizard

Two-column layout:
- Left: Form editor with dynamic fields
- Right: Assistance tools (recommendations, similar datasets, external lookups)

### Abstract Model Tree 5: ReviewDashboard

**Files:** `models/review.py`, `viewmodels/review_vm.py`

Features:
- Filterable/sortable queue
- Bulk actions (assign, approve)
- Statistics widgets
- Status badges

### Abstract Model Tree 6: ReviewDetail

**Files:** Same as ReviewDashboard

Split view:
- Left: Read-only metadata
- Right: Review tools (validation report, checklist, correspondence)

### Abstract Model Tree 7: PlatformConfiguration

**Files:** `models/platform.py`, `viewmodels/platform_vm.py`

Features:
- Platform card list
- Connection testing
- Schema mapping editor
- Plugin management (admin only)

## Role-Based Access Control

All view models respect role-based constraints defined in `core/role_registry.py`:

```python
# Example: Check permission before action
if current_role.can_create_metadata:
    metadata_vm.saveDraft()
else:
    show_access_denied()
```

**Role Matrix:**

| Component | guest_viewer | research_fellow | data_steward | admin |
|-----------|--------------|-----------------|--------------|-------|
| BrowseCatalog | ✅ | ✅ | ✅ | ✅ |
| CreateMetadata | ❌ | ✅ | ✅ | ❌ |
| ReviewDashboard | ❌ | ❌ | ✅ | ❌ |
| PlatformConfig | ❌ | ❌ | ⚠️ | ✅ |

## Validation System

Models include built-in validation:

```python
from models.metadata import MetadataField, FieldDataType

field = MetadataField(
    field_id="title",
    display_name="Title",
    data_type=FieldDataType.TEXT,
    required=True,
    min_length=10
)

errors = field.validate()
if errors:
    for error in errors:
        print(f"{error.level}: {error.message}")
```

Validation levels:
- `INFO`: Suggestions for improvement
- `WARNING`: Non-blocking issues
- `ERROR`: Must be fixed before submission

## RO-Crate Integration (CF3)

MetadataModel can generate RO-Crate JSON-LD:

```python
crate = metadata_model.to_ro_crate()
json_output = json.dumps(crate, indent=2)
```

This produces compliant Research Object Crates for FAIR data packaging.

## Next Steps: Concrete UI Implementation

### For PyQt Mode

Create widget classes in `src/edo_client/widgets/`:

```python
# widgets/catalog_view.py
from ..viewmodels.catalog_vm import CatalogViewModel

class CatalogView(QWidget):
    def __init__(self):
        super().__init__()
        self.vm = CatalogViewModel(self)
        self._setup_ui()
        self._bind_signals()
```

### For QML Mode

Create QML files in `qml/EdoClientContent/`:

```qml
// BrowseCatalogView.qml
import QtQuick
import QtQuick.Controls

Item {
    property alias viewModel: catalogVM
    
    CatalogViewModel {
        id: catalogVM
    }
    
    ListView {
        model: catalogVM.list_model
        // ...
    }
}
```

## Testing

Unit tests should target the **data models** (platform-independent):

```python
# test_models.py
from edo_client.models.catalog import DatasetCard, CatalogModel

def test_catalog_pagination():
    model = CatalogModel()
    model.datasets = [DatasetCard(title=f"Dataset {i}", doi=f"10.x/{i}") 
                      for i in range(100)]
    model.pagination.page_size = 25
    
    assert model.pagination.total_pages == 4
    assert len(model.get_visible_datasets()) == 25
    
    model.next_page()
    assert model.pagination.current_page == 2
```

View models require Qt test framework or manual UI testing.

## Related Documents

- `PROJECT_OVERVIEW.md` - Overall project structure
- `abstract_model_trees.md` - MDUID specification (source)
- `core_functions_resume.md` - Functional requirements (CF1-CF4)
- `edo_roles.md` - Role definitions

---

**Last Updated**: 2026-08-12  
**Version**: 0.1.0  
**Status**: Skeleton implementation complete
