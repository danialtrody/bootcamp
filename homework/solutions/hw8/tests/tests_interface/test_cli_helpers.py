import pytest
from unittest.mock import patch, MagicMock
from _pytest.capture import CaptureFixture
from solution.user_interface.cli_helpers import add_transaction_ui
from starlette.status import HTTP_201_CREATED

API_BASE_URL = "http://localhost:8000"


@pytest.mark.parametrize("transaction_type", ["income", "expense"])
@patch("builtins.input", side_effect=["Salary", "5000"])
@patch("requests.post")
def test_add_transaction_ui_success(
    mock_post: MagicMock,
    mock_input: MagicMock,
    transaction_type: str,
    capsys: CaptureFixture[str],
) -> None:

    mock_post.return_value.status_code = HTTP_201_CREATED

    add_transaction_ui(transaction_type)

    mock_post.assert_called_once_with(
        f"{API_BASE_URL}/{transaction_type}",
        json={"description": "Salary", "amount": 5000},
    )

    captured = capsys.readouterr()

    assert f"{transaction_type.capitalize()} added successfully!" in captured.out
