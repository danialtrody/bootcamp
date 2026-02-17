from solution.exercise2 import (
    get_all_employee_names,
    get_employees_by_department,
    get_average_salary_by_department,
    get_high_earners,
)

HIGH_THRESHOLD = 100000


def test_get_all_employee_names_empty_dict() -> None:

    expected_output: list = []
    output = get_all_employee_names({})

    assert output == expected_output


def test_get_employees_by_department_empty_dict() -> None:

    expected_output: list = []
    output = get_employees_by_department({}, "department_name")

    assert output == expected_output


def test_average_salary_by_department_empty_dict() -> None:

    expected_output: dict = {}
    output = get_average_salary_by_department({})

    assert output == expected_output


def test_get_high_earners_no_departments() -> None:
    expected_output: dict = {}
    output = get_high_earners({}, HIGH_THRESHOLD)
    assert output == expected_output
