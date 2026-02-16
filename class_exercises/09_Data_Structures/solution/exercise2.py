NAME = "name"
DEPARTMENTS = "departments"
TEAMS = "teams"
EMPLOYEES = "employees"
SALARY = "salary"


def get_all_employee_names(company: dict) -> list[str]:
    departments = company.get(DEPARTMENTS, [])

    teams = [team for department in departments for team in department.get(TEAMS, [])]
    employees = [employee for team in teams for employee in team.get(EMPLOYEES, [])]
    names = [employee.get(NAME) for employee in employees]

    return names


def get_employees_by_department(company: dict, department_name: str) -> list[str]:
    departments = company.get(DEPARTMENTS, [])
    teams = [
        team
        for department in departments
        for team in department.get(TEAMS, [])
        if department.get(NAME) == department_name
    ]
    employees = [employee for team in teams for employee in team.get(EMPLOYEES, [])]
    names = [employee.get(NAME) for employee in employees]

    return names


def get_average_salary_by_department(company: dict) -> dict[str, float]:
    departments = company.get(DEPARTMENTS, [])

    return {
        department.get(NAME): round(
            (
                sum(
                    employee.get(SALARY, 0)
                    for team in department.get(TEAMS, [])
                    for employee in team.get(EMPLOYEES, [])
                )
                / len(
                    [
                        employee
                        for team in department.get(TEAMS, [])
                        for employee in team.get(EMPLOYEES, [])
                    ]
                )
            ),
            2,
        )
        for department in departments
    }


def get_high_earners(company: dict, threshold: int) -> dict[str, list[str]]:
    departments = company.get(DEPARTMENTS, [])

    return {
        department.get(NAME): [
            employee.get(NAME)
            for team in department.get(TEAMS, [])
            for employee in team.get(EMPLOYEES, [])
            if employee.get(SALARY, 0) > threshold
        ]
        for department in departments
    }
