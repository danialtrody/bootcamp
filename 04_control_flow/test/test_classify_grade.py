import pytest
from solution.classify_grade import classify_grade


def test_classify_grade():
    assert classify_grade(95) == "A"
    assert classify_grade(90) == "A"
    assert classify_grade(85) == "B"
    assert classify_grade(80) == "B"
    assert classify_grade(75) == "C"
    assert classify_grade(70) == "C"
    assert classify_grade(65) == "D"
    assert classify_grade(60) == "D"
    assert classify_grade(5) == "F"
    assert classify_grade(0) == "F"
    

def test_classify_grade_invalid_low():
    with pytest.raises(ValueError, match="Score must be between 0 and 100."):
        classify_grade(-1)

def test_classify_grade_invalid_high():
    with pytest.raises(ValueError, match="Score must be between 0 and 100."):
        classify_grade(101)