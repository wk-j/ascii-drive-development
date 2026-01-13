#!/usr/bin/env python3
"""
Notes TUI - A Terminal-Based Note Taking Application
=====================================================

Built with ASCII Driven Development methodology.

Usage:
    python -m src.main [--data-path PATH]

or:
    ./src/main.py [--data-path PATH]

+===========================================================================+
|                         NOTES TUI                                        |
|              A Terminal-Based Note Taking Application                    |
+===========================================================================+
"""

import argparse
import sys
from pathlib import Path

# Add src to path if running directly
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path.parent))

from src.app import App


def main():
    """Main entry point for Notes TUI."""
    parser = argparse.ArgumentParser(
        description="Notes TUI - A terminal-based note taking application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Keyboard shortcuts:
  j/k or Up/Down   Navigate
  h/l or Tab       Switch panels
  n                New note
  N                New notebook
  e or Enter       Edit note
  d                Delete
  /                Search
  ?                Help
  q                Quit
        """
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default=None,
        help="Path to the data file (default: data/notes.json)"
    )

    args = parser.parse_args()

    try:
        app = App(data_path=args.data_path)
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
