import pytest
from solution.exercise1 import format_data

NAME = "Alice"
DATA_VALUE = "value"


def test_correct_types() -> None:
    result = format_data(NAME, 30, {"key": DATA_VALUE}, 1234)
    expected_output = f"Name: {NAME}, Age: 30, Data: {DATA_VALUE}, Other Info : 1234"
    assert result == expected_output


def test_incorrect_type_age() -> None:
    expected_output = (
        "Argument 'age' must be of type <class 'int'>, got <class 'str'> instead."
    )
    with pytest.raises(TypeError, match=expected_output):
        format_data(NAME, "thirty", {"key": DATA_VALUE})


def test_incorrect_type_data() -> None:
    expected_output = (
        "Argument 'data' must be of type <class 'dict'>, got <class 'list'> instead."
    )
    with pytest.raises(TypeError, match=expected_output):
        format_data(NAME, 30, ["not a dict"], 1234)


def test_missing_optional() -> None:
    result = format_data(NAME, 30, {"key": DATA_VALUE})
    expected_output = f"Name: {NAME}, Age: 30, Data: {DATA_VALUE}"
    assert result == expected_output
