# EDO Client - Energy Data Orchestrator Desktop Application

A unified PyQt6/QML desktop application with Qt Design Studio support for editing UI designs.

## 🎯 Project Structure

```
EdoClient/
├── run.py                      # Unified launcher (pyqt|qml|test) - single entry point
├── test_ui.py                  # PyQt UI test script
├── test_core.py                # Core logic tests
├── CMakeLists.txt              # CMake build configuration
│
├── src/                        # Python source code
│   └── edo_client/
│       ├── app.py              # PyQt application class
│       ├── qml_app.py          # QML application class
│       ├── qml_bridge.py       # Python-QML bridge
│       ├── __main__.py         # Module entry point (python -m edo_client)
│       │
│       ├── core/               # Core business logic
│       │   ├── role_registry.py    # Role & permission system
│       │   ├── widget_factory.py   # Dynamic widget creation
│       │   └── backend_bridge.py   # Backend communication
│       │
│       └── widgets/            # PyQt widgets (programmatic UI)
│           ├── main_window.py
│           ├── role_aware_container.py
│           └── gadgets/            # Data-specific viewers
│               ├── dataset_browser.py
│               ├── table_viewer.py
│               ├── timeseries_grid.py
│               ├── literal_viewer.py
│               ├── rdf_inspector.py
│               └── fallback_viewer.py
│
├── qml/                        # QML files (Qt Design Studio)
│   ├── EdoClientContent/
│   │   ├── Screen01.ui.qml         # Main content (editable in QDS)
│   │   └── ContentArea.qml         # Dynamic data display
│   │
│   └── EdoClient/
│       ├── App.qml                 # Main window
│       ├── Constants.qml           # Shared constants
│       └── qmldir                  # QML module definition
│
├── .idea/                      # PyCharm project configuration
│   └── runConfigurations/      # Run/debug configurations
│
└── docs/                       # Documentation
```

## 🚀 Quick Start

### Installation

```bash
cd /Users/ot2661/Documents/01_dev/edo/frontend/qt-frontend/EdoClient

# Activate virtual environment
source .venv/bin/activate

# Verify installation
python -c "import PyQt6; print('PyQt6:', PyQt6.__version__)"
```

### Running the Application

#### Option 1: Unified Launcher (Recommended)

```bash
# Run PyQt UI with demo data
python run.py pyqt

# Run QML UI (Qt Design Studio compatible)
python run.py qml

# Run without demo data
python run.py pyqt --no-demo

# Set specific role
python run.py pyqt --role guest_viewer

# Run tests
python run.py test
```

#### Option 2: Module Execution

```bash
# Run as Python module (PyQt mode)
python -m edo_client

# Test UI
python test_ui.py

# Core tests
python test_core.py
```

#### Option 3: PyCharm

Open the project in PyCharm and use the pre-configured run configurations:

- **Run PyQt UI** - Runs `test_ui.py` with demo data
- **Run QML App** - Runs QML-based interface
- **Run Tests** - Executes `test_core.py`

## 🎨 Working with Qt Design Studio

### Editing UI Files

The following QML files are designed to be edited in **Qt Design Studio**:

| File | Description |
|------|-------------|
| `qml/EdoClientContent/Screen01.ui.qml` | Main content area (.ui.qml format) |
| `qml/EdoClientContent/ContentArea.qml` | Dynamic data display component |
| `qml/EdoClient/App.qml` | Application window |
| `qml/EdoClient/Constants.qml` | Shared constants (singleton) |

### Workflow

1. **Edit in Qt Design Studio:**
   - Open `EdoClient.qmlproject` in Qt Design Studio
   - Edit `.ui.qml` files visually
   - Save changes

2. **Test in PyCharm:**
   - Run `python run.py qml` to see QML UI
   - Changes are reflected immediately

3. **Integrate with Python:**
   - QML signals connect to Python slots via `qml_bridge.py`
   - Python data is exposed to QML through context properties

### QML ↔ Python Integration

```qml
// In QML
Button {
    onClicked: pythonBridge.loadData({
        "title": "My Dataset",
        "resources": [...]
    })
}
```

```python
# In Python
from edo_client.qml_bridge import QMLBridge

bridge = QMLBridge()
bridge.dataLoaded.connect(qml_handler)
bridge.triggerAction("data.import", {"path": "..."})
```

## 🧪 Testing

### Core Logic Tests (No GUI Required)

```bash
python test_core.py
```

Tests:
- ✅ Role registry and permissions
- ✅ Widget factory data type detection
- ✅ Backend bridge action execution
- ✅ Demo data structures

### UI Tests (Requires Display)

```bash
# PyQt UI
python test_ui.py

# Specific scenarios
python test_ui.py --role data_steward
python test_ui.py --test-dataset
python test_ui.py --interactive
```

## 👥 Role-Based Access Control

| Permission | Guest | Fellow | Steward | Admin |
|------------|-------|--------|---------|-------|
| View Datasets | ✓ | ✓ | ✓ | ✓ |
| Import Datasets | | ✓ | ✓ | ✓ |
| Edit Metadata | | ✓ | ✓ | ✓ |
| Run Validation | | ✓ | ✓ | ✓ |
| Annotate Resources | | ✓ | ✓ | ✓ |
| Semantic Expansion | | ✓ | ✓ | ✓ |
| Ingestion OEP | | | ✓ | ✓ |
| Ingestion HKG | | | ✓ | ✓ |
| Workflow Status | | | ✓ | ✓ |
| Manage Users | | | | ✓ |

Set role via:
- Environment: `EDO_ROLE=data_steward python run.py pyqt`
- CLI: `python run.py pyqt --role research_fellow`
- UI: Settings page (QML mode only)

## 🔧 Development

### Project Configuration

- **Python**: 3.10+
- **Qt**: PyQt6 6.5+
- **Build**: CMake 3.16+ (for C++/QML builds)
- **IDE**: PyCharm (configurations included)

### Build from Source (C++)

```bash
mkdir build && cd build
cmake ..
make
./edoclient_bin
```

### Directory Layout

```
src/                    Python source (edit in PyCharm)
qml/                    QML files (edit in Qt Design Studio)
.idea/                  PyCharm configuration
.venv/                  Virtual environment
docs/                   Documentation
```

## 📝 Key Files

| File | Purpose | Edit In |
|------|---------|---------|
| `run.py` | Unified launcher | PyCharm |
| `src/edo_client/app.py` | PyQt application logic | PyCharm |
| `src/edo_client/qml_app.py` | QML application logic | PyCharm |
| `src/edo_client/qml_bridge.py` | Python-QML integration | PyCharm |
| `qml/EdoClientContent/Screen01.ui.qml` | Main UI layout | Qt Design Studio |
| `qml/EdoClient/App.qml` | Window definition | Both |
| `CMakeLists.txt` | Build configuration | Text editor |

## 🐛 Troubleshooting

### "Application icon could not be loaded"
Warning only - application runs normally. Add icon to `src/edo_client/resources/`.

### QML Import Errors
Ensure QML path is correct:
```bash
export QML_IMPORT_PATH=/path/to/EdoClient/qml
```

### PyQt6 Not Found
Activate virtual environment:
```bash
source .venv/bin/activate
```

## 📚 Documentation

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt Design Studio Manual](https://doc.qt.io/qt-design-studio/)
- [QML Reference](https://doc.qt.io/qt-6/qml-reference.html)

## 📄 License

Energy Data Orchestrator Team © 2025
