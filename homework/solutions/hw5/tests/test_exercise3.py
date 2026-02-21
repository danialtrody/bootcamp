import pytest
import time
from typing import Any
from solution.exercise3 import MyLruCache

MAX_SIZE = 3
TTL = 2
KEY = "key"
VALUE = "value"
FIRST_KEY = "first_key"


@pytest.fixture
def cache() -> MyLruCache:
    return MyLruCache(MAX_SIZE, TTL)


def test_init(cache: MyLruCache) -> None:
    assert cache.maxsize == MAX_SIZE
    assert cache.ttl == TTL
    assert cache.head.next == cache.tail
    assert cache.tail.prev == cache.head


@pytest.mark.parametrize(
    "key,output",
    [
        ("test_key", "test_value"),
        ("wrong_key", None),
    ],
)
def test_get(
    cache: MyLruCache,
    key: str,
    output: Any | None,
) -> None:

    cache.set("test_key", "test_value")

    get_result = cache.get(key)

    assert get_result == output


def test_ttl_expiration(cache: MyLruCache) -> None:
    cache.set("temp", "data")
    time.sleep(TTL + 0.1)
    assert cache.get("temp") is None


def test_set_basic(cache: MyLruCache) -> None:
    cache.set(KEY, VALUE)
    assert cache.get(KEY) == "value"


def test_set(cache: MyLruCache) -> None:
    cache.set(KEY, VALUE)
    cache.set(KEY, "updated_value")

    assert cache.get(KEY) == "updated_value"


def test_lru_eviction(cache: MyLruCache) -> None:
    cache.set("1", "a")
    cache.set("2", "b")
    cache.set("3", "c")

    cache.get("1")

    cache.set("4", "d")

    assert "2" not in cache
    assert "1" in cache
    assert "3" in cache
    assert "4" in cache


def test_clear(cache: MyLruCache) -> None:
    cache.set(FIRST_KEY, VALUE)
    cache.set("second_key", "second_value")
    cache.clear()

    assert cache.cache == {}
    assert cache.head.next == cache.tail
    assert cache.tail.prev == cache.head


def test_len(cache: MyLruCache) -> None:
    cache.set(FIRST_KEY, VALUE)

    assert len(cache) == 1


def test_contain(cache: MyLruCache) -> None:
    cache.set(FIRST_KEY, VALUE)

    assert FIRST_KEY in cache
