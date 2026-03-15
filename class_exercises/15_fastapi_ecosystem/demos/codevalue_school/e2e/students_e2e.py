"""E2E tests for the /students router."""
import sys

import requests

from e2e_utils import BASE_URL, TestResults, login, register_user, start_server, stop_server

STUDENTS_URL = f"{BASE_URL}/students/"

E2E_ADMIN_EMAIL = "e2e.admin@example-e2e.com"
E2E_ADMIN_PASSWORD = "E2eAdminPass123!"

# Test data — unique enough to avoid collisions with real data
TEST_STUDENT = {
    "first_name": "E2E",
    "last_name": "TestStudent",
    "email": "e2e.teststudent@example-e2e.com",
    "birth_date": "2000-01-15",
}

UPDATE_DATA = {
    "first_name": "E2E",
    "last_name": "UpdatedStudent",
    "email": "e2e.teststudent@example-e2e.com",
    "birth_date": "2000-01-15",
}


def _get_admin_session() -> requests.Session:
    register_user(E2E_ADMIN_EMAIL, E2E_ADMIN_PASSWORD, "E2E", "Admin", role="admin")
    return login(E2E_ADMIN_EMAIL, E2E_ADMIN_PASSWORD)


def run_tests() -> dict:
    results = TestResults("Students E2E")
    created_id = None

    try:
        http = _get_admin_session()
    except Exception as exc:
        results.error("Setup: admin login", exc)
        return results.summary()

    # ── Unauthenticated request returns 401 ──────────────────────────────────
    try:
        resp = requests.get(STUDENTS_URL, timeout=5)
        if resp.status_code == 401:
            results.ok("GET /students/ unauthenticated — returns 401")
        else:
            results.fail("GET /students/ unauthenticated", f"expected 401, got {resp.status_code}")
    except Exception as exc:
        results.error("GET /students/ unauthenticated", exc)

    # ── POST /students/ ──────────────────────────────────────────────────────
    try:
        resp = http.post(STUDENTS_URL, json=TEST_STUDENT, timeout=5)
        if resp.status_code == 201:
            body = resp.json()
            created_id = body.get("student_id")
            if created_id:
                results.ok("POST /students/ — creates a student (201)")
            else:
                results.fail("POST /students/ — response missing student_id", str(body))
        else:
            results.fail("POST /students/ — expected 201", f"got {resp.status_code}: {resp.text}")
    except Exception as exc:
        results.error("POST /students/", exc)

    # ── GET /students/ ───────────────────────────────────────────────────────
    try:
        resp = http.get(STUDENTS_URL, timeout=5)
        if resp.status_code == 200 and isinstance(resp.json(), list):
            results.ok("GET /students/ — returns list (200)")
        else:
            results.fail("GET /students/ — expected 200 list", f"got {resp.status_code}")
    except Exception as exc:
        results.error("GET /students/", exc)

    # ── GET /students/{id} ───────────────────────────────────────────────────
    if created_id is not None:
        try:
            resp = http.get(f"{STUDENTS_URL}{created_id}", timeout=5)
            if resp.status_code == 200 and resp.json().get("student_id") == created_id:
                results.ok(f"GET /students/{created_id} — returns correct student (200)")
            else:
                results.fail(
                    f"GET /students/{created_id} — unexpected response",
                    f"{resp.status_code}: {resp.text}",
                )
        except Exception as exc:
            results.error(f"GET /students/{created_id}", exc)

    # ── GET /students/{id} — not found ───────────────────────────────────────
    try:
        resp = http.get(f"{STUDENTS_URL}999999999", timeout=5)
        if resp.status_code == 404:
            results.ok("GET /students/999999999 — returns 404 for unknown id")
        else:
            results.fail("GET /students/999999999 — expected 404", f"got {resp.status_code}")
    except Exception as exc:
        results.error("GET /students/999999999", exc)

    # ── PUT /students/{id} ───────────────────────────────────────────────────
    if created_id is not None:
        try:
            resp = http.put(f"{STUDENTS_URL}{created_id}", json=UPDATE_DATA, timeout=5)
            if resp.status_code == 200 and resp.json().get("last_name") == "UpdatedStudent":
                results.ok(f"PUT /students/{created_id} — updates student (200)")
            else:
                results.fail(
                    f"PUT /students/{created_id} — unexpected response",
                    f"{resp.status_code}: {resp.text}",
                )
        except Exception as exc:
            results.error(f"PUT /students/{created_id}", exc)

    # ── PUT /students/{id} — not found ───────────────────────────────────────
    try:
        resp = http.put(f"{STUDENTS_URL}999999999", json=UPDATE_DATA, timeout=5)
        if resp.status_code == 404:
            results.ok("PUT /students/999999999 — returns 404 for unknown id")
        else:
            results.fail("PUT /students/999999999 — expected 404", f"got {resp.status_code}")
    except Exception as exc:
        results.error("PUT /students/999999999", exc)

    # ── DELETE /students/{id} ────────────────────────────────────────────────
    if created_id is not None:
        try:
            resp = http.delete(f"{STUDENTS_URL}{created_id}", timeout=5)
            if resp.status_code == 204:
                results.ok(f"DELETE /students/{created_id} — deletes student (204)")
            else:
                results.fail(
                    f"DELETE /students/{created_id} — expected 204",
                    f"got {resp.status_code}: {resp.text}",
                )
        except Exception as exc:
            results.error(f"DELETE /students/{created_id}", exc)
            created_id = None  # prevent double-delete attempt

    # ── DELETE /students/{id} — not found ────────────────────────────────────
    try:
        resp = http.delete(f"{STUDENTS_URL}999999999", timeout=5)
        if resp.status_code == 404:
            results.ok("DELETE /students/999999999 — returns 404 for unknown id")
        else:
            results.fail("DELETE /students/999999999 — expected 404", f"got {resp.status_code}")
    except Exception as exc:
        results.error("DELETE /students/999999999", exc)

    # ── Verify deletion ───────────────────────────────────────────────────────
    if created_id is not None:
        try:
            resp = http.get(f"{STUDENTS_URL}{created_id}", timeout=5)
            if resp.status_code == 404:
                results.ok(f"GET after DELETE /students/{created_id} — confirms removal (404)")
            else:
                results.fail(
                    f"GET after DELETE /students/{created_id} — expected 404",
                    f"got {resp.status_code}",
                )
        except Exception as exc:
            results.error(f"GET after DELETE /students/{created_id}", exc)

    return results.summary()


def main() -> None:
    print("\n=== Students E2E ===")
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
