import pytest
from solution.exercise2 import fibonacci


def test_number_less_than_one():
    expected_output = "input number must be greater or equal to 1"
    with pytest.raises(ValueError, match=expected_output):
        fibonacci(-1)


def test_number_1():
    number = 1
    expected_output = 0
    assert fibonacci(number) == expected_output


def test_number_2():
    number = 2
    expected_output = 1
    assert fibonacci(number) == expected_output


def test_small_number():
    number = 10
    expected_output = 34
    assert fibonacci(number) == expected_output


def test_big_number():
    number = 300
    expected_output = 137347080577163115432025771710279131845700275212767467264610201
    assert fibonacci(number) == expected_output
