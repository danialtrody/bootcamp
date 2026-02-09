from typing import List


class BankAccount:

    def __init__(self, account_name: str, initial_balance: float = 0) -> None:
        self.account_name = account_name
        self._balance = max(initial_balance, 0)
        self._account_activity: List[str] = []

        if initial_balance > 0:
            self._account_activity.append(f"Amount: {initial_balance}")

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, any_thing: float) -> None:
        raise ValueError("Balance is protected. Use deposit or withdraw.")

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than 0.")

        self._balance += amount
        self._account_activity.append(f"Deposit: {amount}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than 0.")
        if amount > self.balance:
            raise ValueError(
                f"Available balance is {self._balance}, "
                f"cannot withdraw {amount}."
            )

        self._balance -= amount
        self._account_activity.append(f"Withdraw: {amount}")

    def get_statement(self) -> str:
        return (
            f"Account name: {self.account_name}\n"
            f"Account balance: {self.balance}\n"
            f"Account's activity:\n{self._account_activity}")
