import pytest
from _pytest.capture import CaptureFixture
from solution.business_logic.budget import Budget
from solution.business_logic.income import Income
from solution.business_logic.expense import Expense
from solution.user_interface.cli_helpers import (
    add_transaction_ui,
    handle_remove,
    print_error,
    remove_transaction_ui,
)

DESCRIPTION = "description"
AMOUNT_HUNDRED = 100
INVALID_DESCRIPTION = ""
INVALID_AMOUNT = ""
EXPENSE = "expense"
INCOME = "income"
SUCCESS_ADD_INCOME = "Income added successfully!"
SUCCESS_ADD_EXPENSE = "Expense added successfully!"
ERROR_ADD_INVALID_AMOUNT = "Invalid input. Please enter a valid amount."
ERROR_ADD_INVALID_DESCRIPTION = "Description must be a non-empty string"
SUCCESS_REMOVE_TRANSACTION_INCOME = "Income Removed successfully!"
SUCCESS_REMOVE_TRANSACTION_EXPENSE = "Expense Removed successfully!"
FAILED_REMOVE_TRANSACTION_INCOME_BY_DES = (
    "Error: No income found with description ''. "
    "Please make sure the description matches an existing income."
)
FAILED_REMOVE_TRANSACTION_EXPENSE_BY_DES = (
    "Error: No expense found with description ''. "
    "Please make sure the description matches an existing expense."
)
FAILED_REMOVE_TRANSACTION_BY_INDEX = (
    "Error: Invalid index 0. Index must be between 1 and 1."
)
BUILTINS_INPUT = "builtins.input"
FAILED_HANDLE_REMOVE_EXPENSE = "\nEnter a valid number 1 or 2"

OPTION_ONE = "1"
OPTION_TWO = "2"
INDEX_ZERO = 0
INDEX_ONE = 1
INVALID_INT = "abc"


@pytest.mark.parametrize(
    "transaction_type, success_message",
    [
        (INCOME, SUCCESS_ADD_INCOME),
        (EXPENSE, SUCCESS_ADD_EXPENSE),
    ],
)
def test_add_transaction_ui_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    transaction_type: str,
    success_message: str,
) -> None:
    """Test add_transaction_ui for both income and expense."""
    budget = Budget()
    inputs = iter([DESCRIPTION, str(AMOUNT_HUNDRED)])
    monkeypatch.setattr(BUILTINS_INPUT, lambda _: next(inputs))

    add_transaction_ui(budget, transaction_type)

    items = getattr(budget, transaction_type)
    assert len(items) == 1
    item = items[0]

    if transaction_type == INCOME:
        assert isinstance(item, Income)
    else:
        assert isinstance(item, Expense)

    assert item.description == DESCRIPTION
    assert item.amount == AMOUNT_HUNDRED

    captured = capsys.readouterr()
    assert success_message in captured.out


@pytest.mark.parametrize(
    "transaction_type, failed_message , inputs",
    [
        (
            INCOME,
            ERROR_ADD_INVALID_DESCRIPTION,
            [INVALID_DESCRIPTION, str(AMOUNT_HUNDRED)],
        ),
        (
            EXPENSE,
            ERROR_ADD_INVALID_DESCRIPTION,
            [INVALID_DESCRIPTION, str(AMOUNT_HUNDRED)],
        ),
        (
            INCOME,
            ERROR_ADD_INVALID_AMOUNT,
            [DESCRIPTION, INVALID_AMOUNT],
        ),
        (
            EXPENSE,
            ERROR_ADD_INVALID_AMOUNT,
            [DESCRIPTION, INVALID_AMOUNT],
        ),
        (
            INCOME,
            ERROR_ADD_INVALID_AMOUNT,
            [INVALID_DESCRIPTION, INVALID_AMOUNT],
        ),
        (
            EXPENSE,
            ERROR_ADD_INVALID_AMOUNT,
            [INVALID_DESCRIPTION, INVALID_AMOUNT],
        ),
    ],
)
def test_add_transaction_ui_failed(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    transaction_type: str,
    failed_message: str,
    inputs: list[str],
) -> None:
    budget = Budget()
    user_input = iter(inputs)
    monkeypatch.setattr(BUILTINS_INPUT, lambda _: next(user_input))

    add_transaction_ui(budget, transaction_type)

    items = getattr(budget, transaction_type)
    assert len(items) == 0

    captured = capsys.readouterr()

    assert failed_message in captured.out


@pytest.mark.parametrize(
    "transaction_type, inputs, success_message",
    [
        (
            INCOME,
            [OPTION_ONE, DESCRIPTION],
            SUCCESS_REMOVE_TRANSACTION_INCOME,
        ),
        (
            EXPENSE,
            [OPTION_ONE, DESCRIPTION],
            SUCCESS_REMOVE_TRANSACTION_EXPENSE,
        ),
        (
            INCOME,
            [OPTION_TWO, INDEX_ONE],
            SUCCESS_REMOVE_TRANSACTION_INCOME,
        ),
        (
            EXPENSE,
            [OPTION_TWO, INDEX_ONE],
            SUCCESS_REMOVE_TRANSACTION_EXPENSE,
        ),
    ],
)
def test_remove_transaction_ui_success(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    transaction_type: str,
    inputs: list[str],
    success_message: str,
) -> None:

    budget = Budget()
    user_input = iter(inputs)
    budget.add_income(Income(DESCRIPTION, AMOUNT_HUNDRED))
    budget.add_expense(Expense(DESCRIPTION, AMOUNT_HUNDRED))

    monkeypatch.setattr(BUILTINS_INPUT, lambda _: next(user_input))

    remove_transaction_ui(budget, transaction_type)

    items = getattr(budget, transaction_type)
    assert len(items) == 0

    captured = capsys.readouterr()

    assert f"1. remove {transaction_type} by description" in captured.out
    assert f"2. remove {transaction_type} by index" in captured.out
    assert success_message in captured.out


@pytest.mark.parametrize(
    "transaction_type, inputs, failed_message",
    [
        (
            INCOME,
            [OPTION_ONE, INVALID_DESCRIPTION],
            FAILED_REMOVE_TRANSACTION_INCOME_BY_DES,
        ),
        (
            EXPENSE,
            [OPTION_ONE, INVALID_DESCRIPTION],
            FAILED_REMOVE_TRANSACTION_EXPENSE_BY_DES,
        ),
        (
            INCOME,
            [OPTION_TWO, INDEX_ZERO],
            FAILED_REMOVE_TRANSACTION_BY_INDEX,
        ),
        (
            EXPENSE,
            [OPTION_TWO, INDEX_ZERO],
            FAILED_REMOVE_TRANSACTION_BY_INDEX,
        ),
    ],
)
def test_remove_transaction_ui_failed(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    transaction_type: str,
    inputs: list[str],
    failed_message: str,
) -> None:

    budget = Budget()
    user_input = iter(inputs)
    budget.add_income(Income(DESCRIPTION, AMOUNT_HUNDRED))
    budget.add_expense(Expense(DESCRIPTION, AMOUNT_HUNDRED))

    monkeypatch.setattr(BUILTINS_INPUT, lambda _: next(user_input))

    remove_transaction_ui(budget, transaction_type)

    items = getattr(budget, transaction_type)
    assert len(items) == 1

    captured = capsys.readouterr()

    assert f"1. remove {transaction_type} by description" in captured.out
    assert f"2. remove {transaction_type} by index" in captured.out
    assert failed_message in captured.out


@pytest.mark.parametrize(
    "remove_item_type, option, expected_output",
    [
        (INCOME, OPTION_ONE, OPTION_ONE),
        (EXPENSE, OPTION_ONE, OPTION_ONE),
        (INCOME, OPTION_TWO, int(OPTION_TWO)),
        (EXPENSE, OPTION_TWO, int(OPTION_TWO)),
    ],
)
def test_handle_remove_success(
    monkeypatch: pytest.MonkeyPatch,
    remove_item_type: str,
    option: str,
    expected_output: str,
) -> None:

    monkeypatch.setattr(BUILTINS_INPUT, lambda _: option)

    result = handle_remove(remove_item_type, option)

    assert result == expected_output


@pytest.mark.parametrize(
    "remove_item_type, inputs",
    [(INCOME, INVALID_INT), (EXPENSE, INVALID_INT)],
)
def test_handle_remove_invalid_index_input(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    remove_item_type: str,
    inputs: str,
) -> None:
    user_input = iter([inputs])
    monkeypatch.setattr(BUILTINS_INPUT, lambda _: next(user_input))

    handle_remove(remove_item_type, OPTION_TWO)

    captured = capsys.readouterr()

    assert "Error:" in captured.out


@pytest.mark.parametrize(
    "remove_item_type, option, failed_message",
    [
        (INCOME, str(INDEX_ZERO), FAILED_HANDLE_REMOVE_EXPENSE),
        (EXPENSE, str(INDEX_ZERO), FAILED_HANDLE_REMOVE_EXPENSE),
    ],
)
def test_handle_remove_failed(
    monkeypatch: pytest.MonkeyPatch,
    capsys: CaptureFixture[str],
    remove_item_type: str,
    option: str,
    failed_message: str,
) -> None:

    monkeypatch.setattr(BUILTINS_INPUT, lambda _: option)

    result = handle_remove(remove_item_type, option)

    captured = capsys.readouterr()

    assert failed_message in captured.out
    assert result == 0


def test_print_error(capsys: CaptureFixture[str]) -> None:
    error_msg = "This is an error"
    print_error(error_msg)

    captured = capsys.readouterr()
    assert f"Error: {error_msg}" in captured.out

    exception = ValueError("Invalid value")
    print_error(exception)

    captured = capsys.readouterr()
    assert "Error: Invalid value" in captured.out
