import pytest
from solution.exercise1 import fetch_sorted_todos
import responses


# python -m pytest

USER_ID = "userId"
ID = "id"
TITLE = "title"
COMPLETED = "completed"

three_fake_todos = [
    {USER_ID: 1, ID: 1, TITLE: "delectus aut autem", COMPLETED: False},
    {
        USER_ID: 1,
        ID: 2,
        TITLE: "quis ut nam facilis et officia qui",
        COMPLETED: False,
    },
    {USER_ID: 1, ID: 3, TITLE: "fugiat veniam minus", COMPLETED: False},
]
SORTED_THREE_FAKE_TODOS = sorted(three_fake_todos, key=lambda todo: todo[TITLE])
LIMIT_THREE = 3

two_fake_todos = [
    {USER_ID: 1, ID: 1, TITLE: "delectus aut autem", COMPLETED: False},
    {
        USER_ID: 1,
        ID: 2,
        TITLE: "quis ut nam facilis et officia qui",
        COMPLETED: False,
    },
]
SORTED_TWO_FAKE_TODOS = sorted(two_fake_todos, key=lambda todo: todo[TITLE])
LIMIT_TWO = 2


single_fake_todos = [
    {USER_ID: 1, ID: 1, "title": "delectus aut autem", "completed": False}
]
SORTED_SINGLE_FAKE_TODOS = sorted(single_fake_todos, key=lambda title: title["title"])
SINGLE_LIMIT = 1

EMPTY_LIMIT = 0


@responses.activate
@pytest.mark.parametrize(
    "fake_todos, limit, expected",
    [
        (three_fake_todos, LIMIT_THREE, SORTED_THREE_FAKE_TODOS),
        (single_fake_todos, SINGLE_LIMIT, SORTED_SINGLE_FAKE_TODOS),
        ([], EMPTY_LIMIT, []),
    ],
)
def test_fetch_sorted_todos_success(
    fake_todos: list[dict], limit: int, expected: list[dict]
):

    for todo in fake_todos:
        responses.add(
            responses.GET,
            f"https://jsonplaceholder.typicode.com/todos/{todo['id']}",
            json=todo,
            status=200,
        )

    todos = fetch_sorted_todos(limit)

    assert todos == expected


@responses.activate
@pytest.mark.parametrize(
    "fake_todos, limit, expected",
    [
        (three_fake_todos, LIMIT_THREE, SORTED_THREE_FAKE_TODOS),
        (three_fake_todos, LIMIT_TWO, SORTED_TWO_FAKE_TODOS),
        (three_fake_todos, SINGLE_LIMIT, single_fake_todos),
        (three_fake_todos, EMPTY_LIMIT, []),
    ],
)
def test_fetch_sorted_todos_success_diff_limits(
    fake_todos: list[dict], limit: int, expected: list[dict]
):

    for todo in fake_todos:
        responses.add(
            responses.GET,
            f"https://jsonplaceholder.typicode.com/todos/{todo['id']}",
            json=todo,
            status=200,
        )

    todos = fetch_sorted_todos(limit)

    assert todos == expected


@responses.activate
@pytest.mark.parametrize("status_code", [400, 500])
def test_fetch_sorted_todos_http_error(status_code):

    responses.add(
        responses.GET,
        "https://jsonplaceholder.typicode.com/todos/1",
        status=status_code,
    )

    todos = fetch_sorted_todos(limit=1)

    assert todos == []
