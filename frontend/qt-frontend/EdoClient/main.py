#!/usr/bin/env python3
"""Energy Data Orchestrator entry point."""

import sys
import os

# Add src to path for direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from edo_client.main import main

if __name__ == "__main__":
    exit(main())
