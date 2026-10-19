"""Status entry point for the independent agentic graph path."""

from __future__ import annotations

import argparse
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="FORMA agentic graph reasoning (through provisional HS)"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="show implementation status without running a spectrum",
    )
    parser.parse_args(argv)
    print("GraphWorkflow: run FITS with demo.py (or python -m FORMA.agentic_graph); "
          "the graph currently stops after provisional HS comparison, before RA.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
