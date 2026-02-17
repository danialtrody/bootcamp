import pytest
from solution.exercise2 import (
    get_all_employee_names,
    get_employees_by_department,
    get_average_salary_by_department,
    get_high_earners,
)

NAME = "name"
EMPLOYEES = "employees"
SALARY = "salary"

ENGINEERING = "Engineering"
SALES = "Sales"

ALICE = "Alice"
BOB = "Bob"
CHARLIE = "Charlie"
DIANA = "Diana"
EVE = "Eve"

FRONTEND = "Frontend"
BACKEND = "Backend"
DIRECT_SALES = "Direct Sales"

HIGH_THRESHOLD = 100000
VERY_HIGH_THRESHOLD = 115000


single_departments = {
    "departments": [
        {
            NAME: ENGINEERING,
            "teams": [
                {
                    NAME: FRONTEND,
                    EMPLOYEES: [{NAME: CHARLIE, SALARY: 105000}],
                }
            ],
        }
    ]
}


company = {
    "departments": [
        {
            NAME: ENGINEERING,
            "teams": [
                {
                    NAME: BACKEND,
                    EMPLOYEES: [
                        {NAME: ALICE, SALARY: 120000},
                        {NAME: BOB, SALARY: 110000},
                    ],
                },
                {
                    NAME: FRONTEND,
                    EMPLOYEES: [{NAME: CHARLIE, SALARY: 105000}],
                },
            ],
        },
        {
            NAME: SALES,
            "teams": [
                {
                    NAME: DIRECT_SALES,
                    EMPLOYEES: [
                        {NAME: DIANA, SALARY: 95000},
                        {NAME: EVE, SALARY: 98000},
                    ],
                }
            ],
        },
    ]
}


def test_get_all_employee_names() -> None:
    expected_output = [ALICE, BOB, CHARLIE, DIANA, EVE]
    names = get_all_employee_names(company)

    assert names == expected_output


def test_get_all_employee_names_single_item() -> None:
    expected_output = [CHARLIE]
    output = get_all_employee_names(single_departments)

    assert output == expected_output


@pytest.mark.parametrize(
    "department_name, expected_output",
    [
        (ENGINEERING, [ALICE, BOB, CHARLIE]),
        (SALES, [DIANA, EVE]),
    ],
)
def test_get_employees_by_department(
    department_name: str,
    expected_output: list[str],
) -> None:
    output = get_employees_by_department(company, department_name)

    assert output == expected_output


def test_get_employees_by_department_single_item() -> None:
    expected_output = [CHARLIE]
    output = get_employees_by_department(single_departments, ENGINEERING)

    assert output == expected_output


def test_get_average_salary_by_department() -> None:
    expected_output = {ENGINEERING: 111666.67, SALES: 96500.0}
    output = get_average_salary_by_department(company)

    assert output == expected_output


def test_average_salary_by_department_one() -> None:
    expected_output = {ENGINEERING: 105000}
    output = get_average_salary_by_department(single_departments)

    assert output == expected_output


def test_get_high_earners() -> None:
    expected_output = {ENGINEERING: [ALICE, BOB, CHARLIE], SALES: []}
    output = get_high_earners(company, HIGH_THRESHOLD)

    assert output == expected_output


def test_get_high_earners_high_threshold() -> None:
    expected_output = {ENGINEERING: [ALICE], SALES: []}
    output = get_high_earners(company, VERY_HIGH_THRESHOLD)

    assert output == expected_output
