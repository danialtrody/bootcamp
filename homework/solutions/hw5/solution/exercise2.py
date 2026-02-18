MONTH_HOURS = 160
MONTHS_IN_YEAR = 12


class Employee:
    def __init__(self, employee_id: str, full_name: str, hourly_rate: float) -> None:
        self.employee_id = employee_id
        self.full_name = full_name
        self.hourly_rate = hourly_rate

    def calculate_compensation(self) -> float:
        return self.hourly_rate * MONTH_HOURS

    def display_information(self) -> str:
        return f"Employee ID: {self.employee_id}, Full Name: {self.full_name}, Hourly Rate: ${self.hourly_rate:.2f}/hr"


class FullTimeEmployee(Employee):
    def __init__(
        self, employee_id: str, full_name: str, annual_salary: float, department: str
    ) -> None:
        super().__init__(employee_id, full_name, 0)  # hourly_rate not used
        self.annual_salary = annual_salary
        self.department = department

    def calculate_compensation(self) -> float:
        return self.annual_salary / MONTHS_IN_YEAR

    def display_information(self) -> str:
        return (
            f"Employee ID: {self.employee_id}, Full Name: {self.full_name}, "
            f"Department: {self.department}, Annual Salary: ${self.annual_salary:,.2f}"
        )


class Manager(FullTimeEmployee):
    def __init__(
        self,
        employee_id: str,
        full_name: str,
        annual_salary: float,
        department: str,
        team_size: int,
        bonus_percentage: float,
    ) -> None:
        super().__init__(employee_id, full_name, annual_salary, department)
        self.team_size = team_size
        self.bonus_percentage = bonus_percentage

    def calculate_compensation(self) -> float:
        base_salary = super().calculate_compensation()
        return base_salary * (1 + self.bonus_percentage)

    def display_information(self) -> str:
        info = super().display_information()
        bonus = self.bonus_percentage * 100
        return f"{info}, Team Size: {self.team_size}, " f"Bonus: {bonus}%"
