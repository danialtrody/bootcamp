import pytest
from solution.exercise2 import(get_all_employee_names, 
                               get_employees_by_department,
                               get_average_salary_by_department,
                               get_high_earners
                               )

NAME = "name"

single_departments = {
    "departments": [
        {
            NAME: "Engineering",
            "teams": [
                {
                    NAME: "Frontend",
                    "employees": [{NAME: "Charlie", "salary": 105000}],
                }
            ],
        }
    ]
}


company = {
    "departments": [
        {
            NAME: "Engineering",
            "teams": [
                {
                    NAME: "Backend",
                    "employees": [
                        {NAME: "Alice", "salary": 120000},
                        {NAME: "Bob", "salary": 110000},
                    ],
                },
                {
                    NAME: "Frontend",
                    "employees": [{NAME: "Charlie", "salary": 105000}],
                },
            ],
        },
        {
            NAME: "Sales",
            "teams": [
                {
                    NAME: "Direct Sales",
                    "employees": [
                        {NAME: "Diana", "salary": 95000},
                        {NAME: "Eve", "salary": 98000},
                    ],
                }
            ],
        },
    ]
}


def test_get_all_employee_names() -> None:

    expected_output = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    output = get_all_employee_names(company)

    assert output == expected_output


def test_get_all_employee_names_empty_dict() -> None:

    expected_output: list = []
    output = get_all_employee_names({})

    assert output == expected_output


def test_get_all_employee_names_single_item() -> None:

    expected_output = ["Charlie"]
    output = get_all_employee_names(single_departments)

    assert output == expected_output


@pytest.mark.parametrize(
    "department_name, expected_output",
    [("Engineering", ["Alice", "Bob", "Charlie"]), ("Sales", ["Diana", "Eve"])],
)
def test_get_employees_by_department(
    department_name: str, expected_output: str
) -> None:

    output = get_employees_by_department(company, department_name)

    assert output == expected_output


def test_get_employees_by_department_empty_dict() -> None:

    expected_output: list = []
    output = get_employees_by_department({}, "department_name")

    assert output == expected_output


def test_get_employees_by_department_single_item() -> None:

    expected_output = ["Charlie"]
    output = get_employees_by_department(single_departments, "Engineering")

    assert output == expected_output
    
    
    
def test_get_average_salary_by_department() -> None:

    expected_output = {'Engineering': 111666.67, 'Sales': 96500.0}
    output = get_average_salary_by_department(company)

    assert output == expected_output


def test_get_average_salary_by_department_empty_dict() -> None:

    expected_output: list = {}
    output = get_average_salary_by_department({})

    assert output == expected_output


def test_get_employees_by_department_single_item() -> None:

    expected_output = {"Engineering": 105000}
    output = get_average_salary_by_department(single_departments)

    assert output == expected_output

def test_get_high_earners() -> None:
    expected_output = {
        "Engineering": ["Alice", "Bob", "Charlie"],
        "Sales": []
    }
    output = get_high_earners(company, 100000)
    assert output == expected_output


def test_get_high_earners_high_threshold() -> None:
    expected_output = {
        "Engineering": ["Alice"],
        "Sales": []
    }
    output = get_high_earners(company, 115000)
    assert output == expected_output


def test_get_high_earners_no_departments() -> None:
    expected_output = {}
    output = get_high_earners({}, 100000)
    assert output == expected_output

