from solution.exercise1 import analyze_log_content


def test_empty_log_content() -> None:
    log_content = ""
    expected_output: dict[str, int] = {}

    assert analyze_log_content(log_content) == expected_output


def test_single_error_log_content() -> None:
    log_content = (
        "2024-04-29 15:45:00,089 INFO [name:starwars_engine][pid:2995] Message one"
    )
    expected_output = {"Info": 1}

    assert analyze_log_content(log_content) == expected_output


def test_long_log_content() -> None:
    log_content = """
2024-04-29 15:45:00,089 INFO [name:starwars_engine][pid:2995] Message one
2024-04-29 15:45:05,123 WARNING [name:starwars_engine][pid:2996] Check disk space
2024-04-29 15:45:08,111 /var/log/apache2/server.access.log 172.18.0.12 - -
"POST /api/command/?201dfd68-e48d-587b-e715-3ff83ef3af19 HTTP/1.1" 200
2024-04-29 15:45:10,456 ERROR [name:starwars_engine][pid:2997] Failed to start engine
2024-04-29 15:46:00,789 INFO [name:starwars_engine][pid:2998] All systems go
"""
    expected_output = {"Error": 1, "Warning": 1, "Info": 2}

    assert analyze_log_content(log_content) == expected_output
