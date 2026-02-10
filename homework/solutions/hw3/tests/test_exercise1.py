import pytest
from solution.exercise1 import format_data


def test_correct_types():
    result = format_data("Alice", 30, {"key": "value"}, 1234)
    expected_output = "Name: Alice, Age: 30, Data: value, Other Info : 1234"
    assert result == expected_output


def test_incorrect_type_age():
    expected_output = (
        "Argument 'age' must be of type <class 'int'>, got <class 'str'> instead."
    )
    with pytest.raises(TypeError, match=expected_output):
        format_data("Alice", "thirty", {"key": "value"})


def test_incorrect_type_data():
    expected_output = (
        "Argument 'data' must be of type <class 'dict'>, got <class 'list'> instead."
    )
    with pytest.raises(TypeError, match=expected_output):
        format_data("Alice", 30, ["not a dict"], 1234)


def test_missing_optional():
    result = format_data("Alice", 30, {"key": "value"})
    expected_output = "Name: Alice, Age: 30, Data: value"
    assert result == expected_output
