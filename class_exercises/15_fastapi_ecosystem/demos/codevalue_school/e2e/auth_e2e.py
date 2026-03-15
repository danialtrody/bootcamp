"""E2E tests for the /auth router."""
import sys
import time

import requests

from e2e_utils import AUTH_URL, BASE_URL, TestResults, login, register_user, start_server, stop_server

E2E_ADMIN_EMAIL = "e2e.admin@example-e2e.com"
E2E_ADMIN_PASSWORD = "E2eAdminPass123!"
E2E_STUDENT_EMAIL = "e2e.student@example-e2e.com"
E2E_STUDENT_PASSWORD = "E2eStudentPass123!"


def _setup_users() -> None:
    register_user(E2E_ADMIN_EMAIL, E2E_ADMIN_PASSWORD, "E2E", "Admin", role="admin")
    register_user(E2E_STUDENT_EMAIL, E2E_STUDENT_PASSWORD, "E2E", "Student", role="student")


def run_tests() -> dict:
    results = TestResults("Auth E2E")
    _setup_users()

    # ── POST /auth/register ──────────────────────────────────────────────────
    try:
        unique_email = f"e2e.newuser.{int(time.time())}@example-e2e.com"
        payload = {
            "email": unique_email,
            "password": "NewUserPass123!",
            "first_name": "New",
            "last_name": "User",
            "role": "student",
        }
        resp = requests.post(f"{AUTH_URL}/register", json=payload, timeout=5)
        if resp.status_code == 201:
            results.ok("POST /auth/register — creates user (201)")
        else:
            results.fail("POST /auth/register — expected 201", f"got {resp.status_code}: {resp.text}")
    except Exception as exc:
        results.error("POST /auth/register", exc)

    # ── POST /auth/register — duplicate email ─────────────────────────────────
    try:
        payload = {
            "email": E2E_ADMIN_EMAIL,
            "password": E2E_ADMIN_PASSWORD,
            "first_name": "E2E",
            "last_name": "Admin",
            "role": "admin",
        }
        resp = requests.post(f"{AUTH_URL}/register", json=payload, timeout=5)
        if resp.status_code == 400:
            results.ok("POST /auth/register duplicate — returns 400")
        else:
            results.fail("POST /auth/register duplicate", f"expected 400, got {resp.status_code}")
    except Exception as exc:
        results.error("POST /auth/register duplicate", exc)

    # ── POST /auth/login — valid credentials ─────────────────────────────────
    try:
        http = login(E2E_ADMIN_EMAIL, E2E_ADMIN_PASSWORD)
        results.ok("POST /auth/login — admin login (200)")
    except Exception as exc:
        results.error("POST /auth/login admin", exc)
        http = None

    # ── POST /auth/login — invalid credentials ───────────────────────────────
    try:
        resp = requests.post(
            f"{AUTH_URL}/login",
            json={"email": E2E_ADMIN_EMAIL, "password": "wrongpassword"},
            timeout=5,
        )
        if resp.status_code == 401:
            results.ok("POST /auth/login — invalid password returns 401")
        else:
            results.fail("POST /auth/login invalid", f"expected 401, got {resp.status_code}")
    except Exception as exc:
        results.error("POST /auth/login invalid", exc)

    # ── GET /auth/me — authenticated ─────────────────────────────────────────
    if http is not None:
        try:
            resp = http.get(f"{AUTH_URL}/me", timeout=5)
            if resp.status_code == 200 and resp.json().get("email") == E2E_ADMIN_EMAIL:
                results.ok("GET /auth/me — returns current user (200)")
            else:
                results.fail("GET /auth/me", f"got {resp.status_code}: {resp.text}")
        except Exception as exc:
            results.error("GET /auth/me", exc)

    # ── GET /auth/me — unauthenticated ────────────────────────────────────────
    try:
        resp = requests.get(f"{AUTH_URL}/me", timeout=5)
        if resp.status_code == 401:
            results.ok("GET /auth/me unauthenticated — returns 401")
        else:
            results.fail("GET /auth/me unauthenticated", f"expected 401, got {resp.status_code}")
    except Exception as exc:
        results.error("GET /auth/me unauthenticated", exc)

    # ── Student cannot access GET /students/ (admin-only) ────────────────────
    try:
        student_http = login(E2E_STUDENT_EMAIL, E2E_STUDENT_PASSWORD)
        resp = student_http.get(f"{BASE_URL}/students/", timeout=5)
        if resp.status_code == 403:
            results.ok("GET /students/ as student — returns 403 (admin only)")
        else:
            results.fail("GET /students/ as student", f"expected 403, got {resp.status_code}")
    except Exception as exc:
        results.error("GET /students/ as student", exc)

    # ── Unauthenticated request to protected endpoint ────────────────────────
    try:
        resp = requests.get(f"{BASE_URL}/students/", timeout=5)
        if resp.status_code == 401:
            results.ok("GET /students/ unauthenticated — returns 401")
        else:
            results.fail("GET /students/ unauthenticated", f"expected 401, got {resp.status_code}")
    except Exception as exc:
        results.error("GET /students/ unauthenticated", exc)

    # ── POST /auth/logout ─────────────────────────────────────────────────────
    if http is not None:
        try:
            resp = http.post(f"{AUTH_URL}/logout", timeout=5)
            if resp.status_code == 200:
                results.ok("POST /auth/logout — logs out (200)")
            else:
                results.fail("POST /auth/logout", f"got {resp.status_code}: {resp.text}")
        except Exception as exc:
            results.error("POST /auth/logout", exc)

    return results.summary()


def main() -> None:
    print("\n=== Auth E2E ===")
    print("  Starting server...")
    process = start_server()
    print(f"  Server running on port {BASE_URL.split(':')[-1]}")
    try:
        run_tests()
    finally:
        stop_server(process)
        print("  Server stopped.")


if __name__ == "__main__":
    main()
    sys.exit(0)
