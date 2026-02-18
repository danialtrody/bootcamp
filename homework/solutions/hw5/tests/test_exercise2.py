from solution.exercise2 import Employee, FullTimeEmployee, Manager

EMPLOYEE_ALICE = "Alice Johnson"
EMPLOYEE_BOB = "Bob Smith"
EMPLOYEE_CAROL = "Carol Whie"
ENGINEERING = "Engineering"
BONUS_MANAGER = 0.1


def test_employee_compensation() -> None:
    emp = Employee("E001", EMPLOYEE_ALICE, 25.0)
    assert emp.calculate_compensation() == 4000


def test_fulltime_compensation() -> None:
    emp = FullTimeEmployee("E002", EMPLOYEE_BOB, 90000, ENGINEERING)
    assert emp.calculate_compensation() == 7500


def test_manager_compensation() -> None:
    emp = Manager("E003", EMPLOYEE_CAROL, 120000, ENGINEERING, 5, BONUS_MANAGER)
    assert emp.calculate_compensation() == 11000


def test_polymorphism_total_payroll() -> None:
    employees = [
        Employee("E001", EMPLOYEE_ALICE, 25.0),
        FullTimeEmployee("E002", EMPLOYEE_BOB, 90000, ENGINEERING),
        Manager("E003", EMPLOYEE_CAROL, 120000, ENGINEERING, 5, BONUS_MANAGER),
    ]
    total_pay = sum(emp.calculate_compensation() for emp in employees)
    assert total_pay == 22500


def test_display_information() -> None:
    emp = Employee("E001", EMPLOYEE_ALICE, 25.0)
    full_timer = FullTimeEmployee("E002", EMPLOYEE_BOB, 90000, ENGINEERING)
    manager = Manager("E003", EMPLOYEE_CAROL, 120000, ENGINEERING, 5, BONUS_MANAGER)

    info_emp = emp.display_information()
    assert EMPLOYEE_ALICE in info_emp
    assert "Hourly Rate" in info_emp

    info_full = full_timer.display_information()
    assert EMPLOYEE_BOB in info_full
    assert "Department" in info_full
    assert "Annual Salary" in info_full

    info_mgr = manager.display_information()
    assert EMPLOYEE_CAROL in info_mgr
    assert "Team Size" in info_mgr
    assert "Bonus" in info_mgr
