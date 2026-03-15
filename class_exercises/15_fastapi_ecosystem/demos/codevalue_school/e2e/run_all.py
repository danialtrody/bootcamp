"""Run all e2e test suites sequentially and print a combined summary."""
import importlib
import sys
from pathlib import Path

# Make the e2e directory importable regardless of working directory
E2E_DIR = Path(__file__).resolve().parent
if str(E2E_DIR) not in sys.path:
    sys.path.insert(0, str(E2E_DIR))

from e2e_utils import start_server, stop_server  # noqa: E402 (path setup required above)

# ── Registry of all e2e suites ───────────────────────────────────────────────
# Each entry is a module name (file in e2e/) that exposes a run_tests() -> dict function.
SUITES = [
    "auth_e2e",
    "students_e2e",
]


def main() -> None:
    print("\n" + "=" * 55)
    print("  CodeValue School — E2E Test Runner")
    print("=" * 55)

    print("\n  Starting server...")
    process = start_server()
    print(f"  Server up at http://127.0.0.1:10110\n")

    totals = {"passed": 0, "failed": 0, "errors": 0}

    try:
        for suite_name in SUITES:
            print(f"\n{'─' * 55}")
            print(f"  Suite: {suite_name}")
            print(f"{'─' * 55}")
            try:
                module = importlib.import_module(suite_name)
                result = module.run_tests()
                for key in totals:
                    totals[key] += result.get(key, 0)
            except Exception as exc:
                print(f"  ⚠️   Could not run suite '{suite_name}': {exc}")
                totals["errors"] += 1
    finally:
        stop_server(process)
        print(f"\n{'─' * 55}")
        print("  Server stopped.")

    # ── Combined summary ─────────────────────────────────────────────────────
    total_tests = totals["passed"] + totals["failed"] + totals["errors"]
    print(f"\n{'=' * 55}")
    print("  OVERALL RESULTS")
    print(f"{'=' * 55}")
    print(f"  Total tests : {total_tests}")
    print(f"  ✅  Passed  : {totals['passed']}")
    print(f"  ❌  Failed  : {totals['failed']}")
    print(f"  ⚠️   Errors  : {totals['errors']}")
    print(f"{'=' * 55}\n")

    if totals["failed"] > 0 or totals["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
