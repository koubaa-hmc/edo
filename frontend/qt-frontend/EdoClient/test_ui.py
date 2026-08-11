#!/usr/bin/env python3
"""
Test script for EDO Client UI.

This script provides various ways to test the user interface:
- Run with demo data auto-loading
- Test specific data types
- Test different role permissions
- Interactive testing mode

Usage:
    python test_ui.py                    # Run with default demo mode
    python test_ui.py --no-demo          # Run without demo data
    python test_ui.py --role guest       # Test with guest viewer role
    python test_ui.py --role steward     # Test with data steward role
    python test_ui.py --test-dataset     # Load only dataset demo
    python test_ui.py --test-timeseries  # Load only timeseries demo
    python test_ui.py --test-rdf         # Load only RDF demo
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Test EDO Client User Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          Run with demo data (default)
  %(prog)s --no-demo                Run without auto-loading demo data
  %(prog)s --role guest             Test guest viewer permissions
  %(prog)s --role fellow            Test research fellow permissions
  %(prog)s --role steward           Test data steward permissions
  %(prog)s --role admin             Test admin permissions
  %(prog)s --test-dataset           Load dataset demo only
  %(prog)s --test-timeseries        Load timeseries demo only
  %(prog)s --test-rdf               Load RDF demo only
  %(prog)s --interactive            Interactive test mode
        """
    )
    
    parser.add_argument(
        "--no-demo",
        action="store_true",
        help="Run without automatically loading demo data"
    )
    
    parser.add_argument(
        "--role",
        type=str,
        default="data_steward",
        choices=["guest_viewer", "research_fellow", "data_steward", "admin"],
        help="Set the user role for testing permissions (default: data_steward)"
    )
    
    parser.add_argument(
        "--test-dataset",
        action="store_true",
        help="Load only dataset demo data"
    )
    
    parser.add_argument(
        "--test-timeseries",
        action="store_true",
        help="Load only timeseries demo data"
    )
    
    parser.add_argument(
        "--test-rdf",
        action="store_true",
        help="Load only RDF demo data"
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enable interactive test mode with console commands"
    )
    
    return parser.parse_args()


def get_demo_dataset():
    """Create demo dataset for testing."""
    return {
        "title": "Energy Consumption Timeseries 2025",
        "description": "Hourly energy consumption data for testing the EDO client. This dataset contains simulated power consumption measurements from a solar park in Brandenburg, Germany.",
        "resources": [
            {"name": "consumption_2025.csv", "format": "CSV", "size": "2.4 MB"},
            {"name": "metadata.json", "format": "JSON", "size": "12 KB"},
            {"name": "README.md", "format": "Markdown", "size": "3 KB"}
        ],
    }


def get_demo_timeseries():
    """Create demo timeseries data for testing."""
    return {
        "timestamps": [f"2025-01-{d:02d}T{h:02d}:00" for d in range(1, 4) for h in range(24)],
        "values": [1200 + (h * 50) + (d * 100) for d in range(1, 4) for h in range(24)],
    }


def get_demo_rdf():
    """Create demo RDF data for testing."""
    return {
        "uri": "https://openenergyontology.org/resource/EnergyPlant_001",
        "@type": "oeo:EnergyPlant",
        "rdfs:label": "Solar Park Brandenburg",
        "location": "Brandenburg, Germany",
        "capacity_mw": 150,
        "operator": "Energy Corp GmbH",
        "commissioned": "2023-06-15"
    }


def run_tests(args):
    """Run the UI tests based on arguments."""
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QTimer, Qt
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Set environment variable for role
    os.environ["EDO_ROLE"] = args.role
    
    # Import application
    from edo_client.app import EDOApplication
    from edo_client.widgets.main_window import MainWindow
    
    print(f"\n🧠 EDO Client UI Test")
    print(f"{'='*50}")
    print(f"Role: {args.role}")
    print(f"Demo mode: {not args.no_demo}")
    print(f"{'='*50}\n")
    
    # Create application
    app = EDOApplication(sys.argv, demo_mode=(not args.no_demo) and not (args.test_dataset or args.test_timeseries or args.test_rdf))
    
    # Get main window reference for custom demo loading
    main_window = app._main_window
    
    if main_window and (args.test_dataset or args.test_timeseries or args.test_rdf):
        # Load specific demos based on flags
        delay = 500
        
        if args.test_dataset:
            print("→ Loading dataset demo...")
            QTimer.singleShot(delay, lambda: main_window.load_data(get_demo_dataset()))
            delay += 1000
        
        if args.test_timeseries:
            print("→ Loading timeseries demo...")
            QTimer.singleShot(delay, lambda: main_window.load_data(get_demo_timeseries()))
            delay += 1000
        
        if args.test_rdf:
            print("→ Loading RDF demo...")
            QTimer.singleShot(delay, lambda: main_window.load_data(get_demo_rdf()))
            delay += 1000
    
    if args.interactive:
        print("\n📝 Interactive Test Mode")
        print(f"{'='*50}")
        print("Available commands:")
        print("  'dataset'  - Load demo dataset")
        print("  'timeseries' - Load demo timeseries")
        print("  'rdf'      - Load demo RDF data")
        print("  'clear'    - Clear current display")
        print("  'quit'     - Exit application")
        print(f"{'='*50}\n")
        
        def check_input():
            try:
                cmd = input("test> ").strip().lower()
                if cmd == "quit" or cmd == "exit":
                    app.quit()
                elif cmd == "dataset":
                    main_window.load_data(get_demo_dataset())
                elif cmd == "timeseries":
                    main_window.load_data(get_demo_timeseries())
                elif cmd == "rdf":
                    main_window.load_data(get_demo_rdf())
                elif cmd == "clear":
                    main_window.load_data(None)
                else:
                    print(f"Unknown command: {cmd}")
                
                # Schedule next input check
                QTimer.singleShot(100, check_input)
            except EOFError:
                app.quit()
            except Exception as e:
                print(f"Error: {e}")
                QTimer.singleShot(100, check_input)
        
        # Start interactive loop after a short delay
        QTimer.singleShot(1000, check_input)
    
    print("✅ Application started successfully")
    print("Press Ctrl+C or close the window to exit\n")
    
    # Run the application
    return app.run()


def main():
    """Main entry point for test script."""
    args = parse_args()
    
    try:
        exit_code = run_tests(args)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
