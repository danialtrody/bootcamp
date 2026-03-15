"""Shared utilities for e2e test scripts."""
import subprocess
import sys
import time
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
E2E_PORT = 10110
BASE_URL = f"http://127.0.0.1:{E2E_PORT}"
AUTH_URL = f"{BASE_URL}/auth"


def start_server() -> subprocess.Popen:
    """Start the FastAPI server on the e2e port and wait until it's ready."""
    process = subprocess.Popen(
        [sys.executable, "main.py", str(E2E_PORT)],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _wait_for_server(process)
    return process


def stop_server(process: subprocess.Popen) -> None:
    """Stop the FastAPI server process."""
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def _wait_for_server(process: subprocess.Popen, timeout: int = 15) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            print("❌  Server process exited unexpectedly")
            sys.exit(1)
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            return
        except requests.ConnectionError:
            time.sleep(0.3)
    print("❌  Server did not start in time")
    stop_server(process)
    sys.exit(1)


def login(email: str, password: str) -> requests.Session:
    """Login and return a requests.Session with the auth cookie set."""
    http = requests.Session()
    resp = http.post(f"{AUTH_URL}/login", json={"email": email, "password": password}, timeout=5)
    if resp.status_code != 200:
        raise RuntimeError(f"Login failed ({resp.status_code}): {resp.text}")
    return http


def register_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: str = "admin",
) -> dict:
    """Register a new user. Returns the response JSON."""
    payload = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
    }
    resp = requests.post(f"{AUTH_URL}/register", json=payload, timeout=5)
    if resp.status_code not in (200, 201, 400):
        raise RuntimeError(f"Register failed ({resp.status_code}): {resp.text}")
    return {"status_code": resp.status_code, "body": resp.json() if resp.content else {}}


class TestResults:
    """Accumulates pass/fail/error counts and prints a summary."""

    def __init__(self, suite_name: str) -> None:
        self.suite_name = suite_name
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def ok(self, label: str) -> None:
        print(f"  ✅  {label}")
        self.passed += 1

    def fail(self, label: str, detail: str = "") -> None:
        msg = f"  ❌  {label}"
        if detail:
            msg += f" — {detail}"
        print(msg)
        self.failed += 1

    def error(self, label: str, exc: Exception) -> None:
        print(f"  ⚠️   {label} — {exc}")
        self.errors += 1

    def summary(self) -> dict:
        total = self.passed + self.failed + self.errors
        print(f"\n  {self.suite_name}: {self.passed}/{total} passed", end="")
        if self.failed:
            print(f", {self.failed} failed", end="")
        if self.errors:
            print(f", {self.errors} errors", end="")
        print()
        return {"passed": self.passed, "failed": self.failed, "errors": self.errors}
