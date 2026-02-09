from solution.exercise5 import solve_quadratic


def test_quadratic_simple():
    assert solve_quadratic(1, -3, 2) == "x1 = 1.00, x2 = 2.00"

def test_quadratic_same_roots():
    assert solve_quadratic(1, -2, 1) == "x1 = 1.00, x2 = 1.00"

def test_quadratic_negative_b():
    assert solve_quadratic(2, 7, 3) == "x1 = -3.00, x2 = -0.50"