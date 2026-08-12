# ViewModel Implementation Guide

## Purpose

ViewModels bridge data models with Qt/QML UI components, providing:
- **Qt properties** for QML data binding
- **Signals** for reactive updates
- **Slots** for QML method calls
- **QAbstractListModel** for list/grid views

## Architecture

```
┌─────────────────────────────────────────┐
│           QML Component                 │
│  (e.g., BrowseCatalogView.qml)         │
└─────────────────────────────────────────┘
         │ binds to
         ▼
┌─────────────────────────────────────────┐
│          ViewModel                      │
│  - @property (read-only)                │
│  - pyqtSignal (notifications)           │
│  - pyqtSlot (callable from QML)         │
│  - QAbstractListModel (list data)       │
└─────────────────────────────────────────┘
         │ wraps
         ▼
┌─────────────────────────────────────────┐
│          Data Model                     │
│  - Pure Python dataclass                │
│  - Business logic                       │
│  - Validation                           │
└─────────────────────────────────────────┘
```

## Creating a New ViewModel

### Step 1: Define Properties

Use Python `@property` decorator for read-only properties exposed to QML:

```python
from PyQt6.QtCore import QObject, pyqtSignal

class MyViewModel(QObject):
    loadingChanged = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isLoading = False
    
    @property
    def isLoading(self) -> bool:
        return self._isLoading
    
    @isLoading.setter
    def isLoading(self, value: bool):
        if self._isLoading != value:
            self._isLoading = value
            self.loadingChanged.emit(value)
```

### Step 2: Define Slots

Use `@pyqtSlot` for methods callable from QML:

```python
from PyQt6.QtCore import pyqtSlot, QVariant

@pyqtSlot(str)
def setSearchQuery(self, query: str):
    """Set search query (called from QML)."""
    self._model.filter_state.search_query = query
    self._apply_filters()

@pyqtSlot(result=QVariant)
def getStatistics(self) -> Any:
    """Get statistics (called from QML)."""
    return self._model.stats.to_dict()
```

### Step 3: Create List Model

For list/grid views, subclass `QAbstractListModel`:

```python
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt

class ItemListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []
    
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._items) if not parent.isValid() else 0
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        item = self._items[index.row()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return item.title
        elif role == Qt.ItemDataRole.UserRole:
            return item.to_dict()
        
        return None
    
    def roleNames(self) -> dict:
        return {
            Qt.ItemDataRole.DisplayRole: b"title",
            Qt.ItemDataRole.UserRole: b"item",
        }
    
    def set_items(self, items: list):
        self.beginResetModel()
        self._items = items
        self.endResetModel()
```

### Step 4: Use in QML

```qml
import QtQuick
import QtQuick.Controls

Item {
    MyViewModel {
        id: viewModel
    }
    
    // Bind to property
    BusyIndicator {
        running: viewModel.isLoading
    }
    
    // Call slot
    TextField {
        onTextChanged: viewModel.setSearchQuery(text)
    }
    
    // Use list model
    ListView {
        model: viewModel.list_model
        delegate: ItemDelegate {
            text: model.title
            onClicked: viewModel.selectItem(index)
        }
    }
}
```

## Existing ViewModels

### CatalogViewModel

**File:** `viewmodels/catalog_vm.py`

**Purpose:** Browse and filter dataset catalog

**Key Methods:**
- `setSearchQuery(query: str)`
- `setDomainFilter(domains: QVariant)`
- `nextPage()`, `previousPage()`, `jumpToPage(page: int)`
- `selectDataset(index: int)`
- `clearFilters()`

**Properties:**
- `isLoading: bool`
- `totalItems: int`
- `currentPage: int`
- `totalPages: int`
- `hasPrevious: bool`
- `hasNext: bool`
- `activeFiltersCount: int`

**List Model:** `DatasetCardListModel`

---

### MetadataViewModel

**File:** `viewmodels/metadata_vm.py`

**Purpose:** Create and edit metadata (wizard interface)

**Key Methods:**
- `nextStep() -> bool`
- `previousStep() -> bool`
- `goToStep(step: int) -> bool`
- `setFieldValue(field_id: str, value: QVariant)`
- `validateAll() -> QVariant`
- `saveDraft()`
- `submitForReview()`
- `generateROCrate() -> QVariant`

**Properties:**
- `currentStep: int`
- `totalSteps: int`
- `currentStepTitle: str`
- `completenessScore: float` (percentage)
- `hasValidationErrors: bool`
- `canSubmit: bool`
- `isDirty: bool`

**Wizard Steps:**
1. Select Template
2. Basic Information
3. Scientific Context
4. Technical Metadata
5. Access & Reuse
6. Target Platforms

---

### ReviewViewModel

**File:** `viewmodels/review_vm.py`

**Purpose:** Metadata review queue management

**Key Methods:**
- `setStatusFilter(status: str)`
- `toggleSelection(index: int)`
- `selectAll()`, `clearSelection()`
- `selectItem(index: int)`
- `bulkAssign(reviewer_id: str)`
- `approveReview(review_id: str, notes: str)`
- `requestRevisions(review_id: str, issues_json: str, due_date: str, message: str)`
- `getChecklist(review_id: str) -> QVariant`
- `getTimeline(review_id: str) -> QVariant`
- `getCorrespondence(review_id: str) -> QVariant`

**Properties:**
- `isLoading: bool`
- `stats: Dict[str, Any]`
- `selectedCount: int`
- `hasSelection: bool`

**List Model:** `ReviewQueueListModel`

---

### DatasetDetailViewModel

**File:** `viewmodels/dataset_detail_vm.py`

**Purpose:** View dataset details with tabs

**Key Methods:**
- `setTab(index: int)`
- `nextTab()`, `previousTab()`
- `downloadFile(index: int)`
- `downloadAll()`
- `exportCitation(format: str)`
- `getCitationFormats() -> QVariant`
- `findSimilarBy(criteria: str)`

**Properties:**
- `isLoading: bool`
- `currentTab: int` (0-4)
- `hasDataset: bool`
- `title: str`
- `doi: str`
- `authors: List[Dict]`
- `isOpenAccess: bool`
- `license: str`
- `accessType: str`

**Tabs:**
0. Overview
1. Metadata
2. Files
3. Usage
4. Similar Datasets

---

### PlatformViewModel

**File:** `viewmodels/platform_vm.py`

**Purpose:** Configure target publication platforms

**Key Methods:**
- `addPlatform(platform_id: str, name: str, domain: str)`
- `removePlatform(platform_id: str)`
- `testConnection(platform_id: str)`
- `testAllConnections()`
- `setApiEndpoint(platform_id: str, endpoint: str)`
- `createMapping(platform_id: str, source_schema: str, target_schema: str)`
- `addFieldMapping(platform_id: str, source_field: str, target_field: str, transformation: str)`
- `getFieldMappings(platform_id: str) -> QVariant`
- `installPlugin(plugin_id: str)`

**Properties:**
- `isLoading: bool`
- `statistics: Dict[str, Any]`
- `availableDomains: List[str]`

**List Model:** `PlatformListModel`

## Best Practices

### 1. Signal Naming

Use camelCase with changed suffix for property notifications:
```python
loadingChanged = pyqtSignal(bool)
errorChanged = pyqtSignal(str)
```

### 2. Slot Parameters

Use `QVariant` for complex types passed from QML:
```python
@pyqtSlot(QVariant)
def setData(self, data: Any):
    # Convert QVariant to Python type
    if isinstance(data, dict):
        ...
```

### 3. Return Types

Always specify `result=QVariant` for slots returning data to QML:
```python
@pyqtSlot(result=QVariant)
def getStatistics(self) -> Any:
    return {...}
```

### 4. Thread Safety

For long-running operations, use async patterns:
```python
async def _load_data_async(self):
    # Fetch from backend
    result = await self._backend.fetch(...)
    
    # Update UI on main thread
    QTimer.singleShot(0, lambda: self._update_model(result))
```

### 5. Error Handling

Emit error signals instead of raising exceptions:
```python
try:
    data = self._fetch_data()
except Exception as e:
    self.error = str(e)  # Emits errorChanged signal
    return
```

### 6. Memory Management

Use parent parameter for automatic cleanup:
```python
def __init__(self, parent: Optional[QObject] = None):
    super().__init__(parent)
    self._child = SomeObject(self)  # Parent owns child
```

## Testing ViewModels

### Unit Tests (without UI)

```python
import pytest
from edo_client.viewmodels.catalog_vm import CatalogViewModel

def test_catalog_pagination():
    vm = CatalogViewModel()
    
    # Load test data
    vm.load_datasets([
        {"title": f"Dataset {i}", "doi": f"10.x/{i}"}
        for i in range(100)
    ])
    
    assert vm.currentPage == 1
    assert vm.totalPages == 4
    
    vm.nextPage()
    assert vm.currentPage == 2
```

### Integration Tests (with QML)

Requires Qt test framework:

```python
from pytestqt.qtbot import QtBot

def test_qml_binding(qtbot: QtBot):
    vm = CatalogViewModel()
    
    # Load QML component
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("catalogVM", vm)
    engine.load("qrc:/qml/BrowseCatalogView.qml")
    
    # Trigger action
    vm.setSearchQuery("energy")
    
    # Verify UI updated
    assert vm.activeFiltersCount == 1
```

## Common Patterns

### Loading State Pattern

```python
@property
def isLoading(self) -> bool:
    return self._isLoading

@isLoading.setter
def isLoading(self, value: bool):
    if self._isLoading != value:
        self._isLoading = value
        self.loadingChanged.emit(value)

@pyqtSlot()
def refresh(self):
    self.isLoading = True
    try:
        data = self._fetch()
        self._update_model(data)
    finally:
        self.isLoading = False
```

### Validation Pattern

```python
@pyqtSlot(result=QVariant)
def validateAll(self) -> Any:
    errors = self._model.validate_all()
    self.validationChanged.emit()
    
    return {
        "hasErrors": any(e.is_error() for e in errors),
        "errorCount": len([e for e in errors if e.is_error()]),
        "errors": [
            {"field": e.field_id, "message": e.message}
            for e in errors
        ]
    }
```

### Selection Pattern

```python
@property
def selectedCount(self) -> int:
    return len(self._selected_ids)

@pyqtSlot(int)
def toggleSelection(self, index: int):
    item = self._get_item(index)
    if item:
        if item.id in self._selected_ids:
            self._selected_ids.remove(item.id)
        else:
            self._selected_ids.append(item.id)
        self.selectionChanged.emit()
```

## Migration from PyQt Widgets

If migrating from pure PyQt widgets to QML:

1. **Keep the data model** - it's platform-independent
2. **Create ViewModel** - wrap model with Qt properties/signals/slots
3. **Replace widget signals** with ViewModel signals
4. **Replace widget slots** with ViewModel slots
5. **Update tests** to use ViewModel instead of direct widget access

Example migration:

**Before (PyQt):**
```python
class CatalogWidget(QWidget):
    searchChanged = pyqtSignal(str)
    
    def __init__(self):
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.searchChanged.emit)
```

**After (QML + ViewModel):**
```python
class CatalogViewModel(QObject):
    searchChanged = pyqtSignal(str)
    
    @pyqtSlot(str)
    def setSearchQuery(self, query: str):
        self._model.filter_state.search_query = query
        self.searchChanged.emit(query)
```

```qml
TextField {
    onTextChanged: catalogVM.setSearchQuery(text)
}
```

## Related Documents

- `MODEL_ARCHITECTURE.md` - Data model architecture
- `../core/backend_bridge.py` - Backend integration
- `../core/role_registry.py` - Role-based access control
- Qt Documentation: [Qt Quick](https://doc.qt.io/qt-6/qtquick-index.html)

---

**Last Updated**: 2026-08-12  
**Version**: 0.1.0
