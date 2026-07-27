from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .build import write_artifacts
from .validate import validate


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="canon-rag")
    result.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    commands = result.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="build baseline, chunks, and manifest")
    build.add_argument("--output", type=Path, default=Path("generated/chloekatastrophe"))
    commands.add_parser("validate", help="validate sources and retrieval metadata")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = args.root.resolve()
    if args.command == "validate":
        errors = validate(root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("Canon retrieval sources are valid.")
        return 0
    output = args.output if args.output.is_absolute() else root / args.output
    print(json.dumps(write_artifacts(root, output), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

