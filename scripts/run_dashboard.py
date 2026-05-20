#!/usr/bin/env python
"""Launch the LLM Router Dashboard in the default browser.

Usage:
    python scripts/run_dashboard.py
    python scripts/run_dashboard.py --port 8502
    python scripts/run_dashboard.py --no-browser
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch the LLM Router Dashboard")
    parser.add_argument("--port", type=int, default=8501, help="Port to run on (default: 8501)")
    parser.add_argument("--host", default="localhost", help="Host to bind to (default: localhost)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    app_path = project_root / "src" / "dashboard" / "app.py"

    if not app_path.exists():
        print(f"Error: Dashboard app not found at {app_path}")
        sys.exit(1)

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.port", str(args.port),
        "--server.address", args.host,
    ]

    if args.no_browser:
        cmd.append("--server.headless")
        cmd.append("true")

    print(f"Launching LLM Router Dashboard at http://{args.host}:{args.port}")
    print(f"App: {app_path}")
    print("Press Ctrl+C to stop.")
    print()

    try:
        subprocess.run(cmd, cwd=str(project_root))
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    except FileNotFoundError:
        print("Error: Streamlit not installed. Run: pip install streamlit")
        sys.exit(1)


if __name__ == "__main__":
    main()
