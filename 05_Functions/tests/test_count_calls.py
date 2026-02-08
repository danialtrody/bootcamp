from solutions.count_calls import greet

def test_greet_initial_call_count():
    assert greet.call_count == 0


def test_greet_call_count():
    greet("Alice")
    greet("Bob")
    assert greet.call_count == 2


def test_greet_returns_correct_value():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"

