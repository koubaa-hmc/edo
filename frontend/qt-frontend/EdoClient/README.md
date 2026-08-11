# EDO Client - Qt Desktop Application

Energy Data Orchestrator desktop client built with PyQt6.

## Features

- **Role-based UI**: Dynamic interface based on user permissions (Guest Viewer, Research Fellow, Data Steward, Admin)
- **Data-driven widgets**: Automatic widget selection based on data type
  - Dataset Browser
  - Table Viewer
  - Timeseries Grid
  - RDF Inspector
  - Literal Viewer
- **Async support**: Full asyncio integration via qasync
- **Backend bridge**: Decoupled communication with backend services

## Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or: .venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .
```

## Running the Application

### Direct execution
```bash
python main.py
```

### As module
```bash
python -m edo_client
```

### With entry point (after install)
```bash
edo-client
```

## Testing the UI

Use the included test script to verify the user interface:

```bash
# Run with demo data (default)
python test_ui.py

# Run without auto-loading demo data
python test_ui.py --no-demo

# Test specific roles
python test_ui.py --role guest_viewer
python test_ui.py --role research_fellow
python test_ui.py --role data_steward
python test_ui.py --role admin

# Test specific data types
python test_ui.py --test-dataset
python test_ui.py --test-timeseries
python test_ui.py --test-rdf

# Interactive mode
python test_ui.py --interactive
```

### Interactive Test Commands

In interactive mode, use these commands:
- `dataset` - Load demo dataset
- `timeseries` - Load demo timeseries
- `rdf` - Load demo RDF data
- `clear` - Clear current display
- `quit` - Exit application

## Project Structure

```
EdoClient/
├── src/edo_client/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py              # Application class
│   ├── main.py             # Entry point
│   ├── core/
│   │   ├── role_registry.py    # Role & permission management
│   │   ├── widget_factory.py   # Dynamic widget creation
│   │   └── backend_bridge.py   # Backend communication
│   └── widgets/
│       ├── main_window.py          # Main application window
│       ├── role_aware_container.py # Dynamic content container
│       └── gadgets/
│           ├── dataset_browser.py
│           ├── table_viewer.py
│           ├── timeseries_grid.py
│           ├── literal_viewer.py
│           ├── rdf_inspector.py
│           └── fallback_viewer.py
├── test_ui.py              # UI test script
├── pyproject.toml
└── README.md
```

## Role Permissions

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
| Admin Access | | | | ✓ |

## Environment Variables

- `EDO_ROLE`: Override the default role for testing (e.g., `EDO_ROLE=guest_viewer`)

## Logging

Logs are written to `~/.edo-client/logs/edo-client.log` with rotation (5 MB per file, 3 backups).

## Requirements

- Python 3.10+
- PyQt6 6.5+
- qasync 0.27+ (optional, for asyncio event loop integration)
