#!/usr/bin/env python3
"""
EDO Client - Unified Launcher

This script provides a single entry point for running the application
in different modes:
  - pyqt: Pure PyQt6 UI (programmatic widgets)
  - qml: QML-based UI (Qt Design Studio compatible)
  - test: Run test suite

Usage:
    python run.py [mode] [options]
    
Examples:
    python run.py pyqt                    # Run PyQt UI with demo data
    python run.py pyqt --no-demo          # Run PyQt UI without demo
    python run.py qml                     # Run QML UI with demo data
    python run.py test                    # Run core tests
    python run.py --help                  # Show help
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="EDO Client - Unified Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  pyqt    Run PyQt6-based UI (programmatic widgets)
  qml     Run QML-based UI (Qt Design Studio compatible)
  test    Run test suite

Environment Variables:
  EDO_ROLE         Set default role (guest_viewer, research_fellow, data_steward, admin)
  QT_QPA_PLATFORM  Set Qt platform (e.g., offscreen for testing)

Examples:
  %(prog)s pyqt --role guest_viewer
  %(prog)s qml --demo
  %(prog)s test
        """
    )
    
    parser.add_argument(
        "mode",
        nargs="?",
        default="pyqt",
        choices=["pyqt", "qml", "test"],
        help="Application mode (default: pyqt)"
    )
    
    parser.add_argument(
        "--no-demo",
        action="store_true",
        help="Run without demo data auto-loading"
    )
    
    parser.add_argument(
        "--role",
        type=str,
        default=None,
        choices=["guest_viewer", "research_fellow", "data_steward", "admin"],
        help="Set user role"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()


def run_pyqt(args):
    """Run PyQt6-based UI."""
    from edo_client.app import EDOApplication
    
    if args.role:
        os.environ["EDO_ROLE"] = args.role
    
    app = EDOApplication(sys.argv, demo_mode=not args.no_demo)
    return app.run()


def run_qml(args):
    """Run QML-based UI."""
    from edo_client.qml_app import QMLApplication
    
    app = QMLApplication(demo_mode=not args.no_demo)
    return app.run()


def run_tests(args):
    """Run test suite."""
    import subprocess
    
    print("\n🧪 Running EDO Client Tests\n")
    
    # Run core tests
    result = subprocess.run(
        [sys.executable, "test_core.py"],
        cwd=os.path.dirname(__file__) or ".",
        env={**os.environ, "PYTHONPATH": os.path.join(os.path.dirname(__file__) or ".", "src")}
    )
    
    return result.returncode


def main():
    """Main entry point."""
    args = parse_args()
    
    if args.verbose:
        print(f"Mode: {args.mode}")
        print(f"Demo: {not args.no_demo}")
        if args.role:
            print(f"Role: {args.role}")
        print()
    
    try:
        if args.mode == "pyqt":
            return run_pyqt(args)
        elif args.mode == "qml":
            return run_qml(args)
        elif args.mode == "test":
            return run_tests(args)
        else:
            print(f"Unknown mode: {args.mode}")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
