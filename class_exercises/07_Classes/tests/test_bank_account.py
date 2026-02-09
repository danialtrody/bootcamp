import pytest
from solutions.bank_account import BankAccount


def test_balance_protected():
    account = BankAccount("TestUser", 100)

    with pytest.raises(
        ValueError, match="Balance is protected. Use deposit or withdraw."
    ):
        account.balance = 1000


def test_deposit():
    account = BankAccount("TestUser", 0)
    account.deposit(1000.0)

    assert account.balance == 1000.0


def test_deposit_invalid_input():
    account = BankAccount("TestUser", 0)

    with pytest.raises(ValueError, match="Deposit amount must be greater than 0."):
        account.deposit(-1)


def test_withdraw():
    account = BankAccount("TestUser", 1000)
    account.withdraw(500)

    assert account.balance == 500


def test_withdraw_invalid_input():
    account = BankAccount("TestUser", 0)

    with pytest.raises(ValueError, match="Withdraw amount must be greater than 0."):
        account.withdraw(-1)


def test_withdraw_insufficient_balance():
    account = BankAccount("TestUser", 500)

    with pytest.raises(
        ValueError, match="Available balance is 500, cannot withdraw 5000."
    ):
        account.withdraw(5000)


def test_get_statement():
    user = BankAccount("danial", 1000)

    user.deposit(1000.0)
    assert user.balance == 2000.0

    user.withdraw(300.0)
    assert user.balance == 1700.0

    assert user.get_statement() == (
        "Account name: danial\n"
        "Account balance: 1700.0\n"
        "Account's activity:\n"
        "['Amount: 1000', 'Deposit: 1000.0', 'Withdraw: 300.0']"
    )
