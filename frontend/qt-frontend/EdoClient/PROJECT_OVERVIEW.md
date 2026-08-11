# EDO Client - Merged Project Overview

This document explains how the PyQt6 Python project and Qt Design Studio QML project have been merged into a single unified workspace.

## 🎯 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PyCharm IDE                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  src/edo_client/         (Python Backend)            │   │
│  │  ├── app.py              (PyQt application)          │   │
│  │  ├── qml_app.py          (QML application)           │   │
│  │  ├── qml_bridge.py       (Python↔QML bridge)         │   │
│  │  └── core/               (Business logic)            │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  qml/                      (Qt Design Studio UI)     │   │
│  │  ├── EdoClientContent/     (.ui.qml editable)        │   │
│  │  └── EdoClient/            (QML module)              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │      run.py (Unified)         │
              │  pyqt | qml | test modes      │
              └───────────────────────────────┘
```

## 📁 Directory Mapping

### Before Merge

| PyQt Project | Qt Design Studio Project |
|--------------|--------------------------|
| `src/edo_client/` | `EdoClient/` (QML) |
| `test_ui.py` | `EdoClient.qmlproject` |
| `run.py` (pyqt mode) | `EdoClientContent/*.qml` |

### After Merge

All files now live under `/Users/ot2661/Documents/01_dev/edo/frontend/qt-frontend/EdoClient/`:

```
EdoClient/
├── src/                    ← Python source (from PyQt project)
├── qml/                    ← QML files (from Qt Design Studio)
├── .idea/                  ← PyCharm configuration (NEW)
├── run.py                  ← Unified launcher (single entry point)
├── test_ui.py              ← PyQt UI tests
├── test_core.py            ← Core logic tests
└── CMakeLists.txt          ← Optional C++ build support
```

## 🔄 Workflow

### In PyCharm (Python Development)

1. **Edit Python code** in `src/edo_client/`
2. **Run configurations** pre-configured:
   - Run PyQt UI → `test_ui.py`
   - Run QML App → `qml_app.py`
   - Run Tests → `test_core.py`
3. **Debug** with full Python debugger support

### In Qt Design Studio (UI Design)

1. **Open project**: File → Open Project → Select `EdoClient.qmlproject`
2. **Edit `.ui.qml` files** visually:
   - `qml/EdoClientContent/Screen01.ui.qml`
   - `qml/EdoClientContent/ContentArea.qml`
3. **Save** - files update in real-time
4. **Test** in PyCharm with `python run.py qml`

### Python ↔ QML Communication

```python
# Python side (qml_bridge.py)
class QMLBridge(QObject):
    dataLoaded = pyqtSignal(QVariant)
    
    @pyqtSlot(QVariant)
    def loadData(self, data):
        self.dataLoaded.emit(data)
```

```qml
// QML side (App.qml)
ApplicationWindow {
    // Connect to Python
    Connections {
        target: pythonBridge
        function onDataLoaded(data) {
            console.log("Data from Python:", data)
        }
    }
    
    // Call Python
    Button {
        onClicked: pythonBridge.loadData({...})
    }
}
```

## 🚀 Entry Points

### For Users

```bash
# Simple launch
python run.py pyqt

# With options
python run.py pyqt --role data_steward --no-demo
```

### For Developers

```bash
# Test PyQt widgets
python test_ui.py

# Test QML interface
python run.py qml

# Run unit tests
python test_core.py
```

### For Qt Design Studio

1. Open `EdoClient.qmlproject`
2. Edit QML files
3. Save
4. Switch to PyCharm to test integration

## 🔧 Configuration Files

| File | Purpose | Tool |
|------|---------|------|
| `.idea/*.xml` | PyCharm project settings | PyCharm |
| `.idea/runConfigurations/*.xml` | Run/debug configs | PyCharm |
| `EdoClient.qmlproject` | QDS project file | Qt Design Studio |
| `CMakeLists.txt` | C++ build config | CMake |
| `pyproject.toml` | Python package config | pip/uv |
| `run.py` | Unified launcher | Python |

## 📊 Feature Comparison

| Feature | PyQt Mode | QML Mode |
|---------|-----------|----------|
| UI Definition | Python code | QML files |
| Design Tool | PyCharm | Qt Design Studio |
| Widget Library | PyQt6 widgets | Qt Quick Controls |
| Styling | Stylesheets | QML properties |
| Animation | QPropertyAnimation | Qt Quick animations |
| Data Binding | Manual | Declarative |
| Hot Reload | No | Partial |

## 🎨 When to Use Which Mode

### Use PyQt Mode When:
- Building complex data grids/tables
- Need mature widget set (QTableWidget, QTreeWidget)
- Prefer programmatic UI control
- Existing PyQt codebase

### Use QML Mode When:
- Designing in Qt Design Studio
- Need smooth animations
- Prefer declarative UI
- Working with designers

## 📝 Migration Notes

### From Old PyQt Project

- ✅ All Python code preserved in `src/`
- ✅ Tests moved to project root
- ✅ Virtual environment compatible
- ✅ New `run.py` replaces direct execution

### From Old Qt Design Studio Project

- ✅ QML files moved to `qml/` directory
- ✅ `.qmlproject` file preserved
- ✅ Constants and resources migrated
- ✅ Now integrates with Python backend

## 🔮 Future Enhancements

1. **Hybrid UI**: Combine PyQt widgets in QML via `QQuickWidget`
2. **Plugin System**: Load dynamic gadgets at runtime
3. **Theme Support**: Switch between light/dark themes
4. **Internationalization**: Translate UI strings

## 📞 Support

For issues:
- PyQt problems → Check `test_ui.py` output
- QML problems → Verify in Qt Design Studio
- Integration problems → Review `qml_bridge.py` logs

---

**Last Updated**: 2026-08-11  
**Version**: 0.1.0  
**Project**: Energy Data Orchestrator Desktop Client
