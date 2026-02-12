from _pytest.monkeypatch import MonkeyPatch
from _pytest.capture import CaptureFixture
from solution.exercise2 import simple_calculator

EXIT = "exit"
HELP = "help"
INPUT_PATH = "builtins.input"


def test_exit_input(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    monkeypatch.setattr(INPUT_PATH, lambda _: EXIT)
    simple_calculator()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Goodbye! Thank you for using the calculator."


def test_help_input(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    inputs = iter([HELP, EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert (
        "Valid operations:\n"
        "- add <num1> to <num2>\n"
        "- subtract <num1> from <num2>\n"
        "- multiply <num1> by <num2>\n"
        "- divide <num1> by <num2>\n"
        "- help\n"
        "- exit"
    ) in captured.out


def test_invalid_input(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    inputs = iter(["add-sub", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert (
        "Invalid input. Please enter numbers correctly. Type 'help' for instructions."
        in captured.out
    )


def test_add_operation(monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]) -> None:
    inputs = iter(["add 2 to 5", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "7.0" in captured.out


def test_subtract_operation(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    inputs = iter(["subtract 2 from 5", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "3.0" in captured.out


def test_multiply_operation(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    inputs = iter(["multiply 2 by 5", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "10.0" in captured.out


def test_valid_divide_operation(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    inputs = iter(["divide 10 by 5", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "2.0" in captured.out


def test_zero_divide_operation(
    monkeypatch: MonkeyPatch, capsys: CaptureFixture[str]
) -> None:
    inputs = iter(["divide 10 by 0", EXIT])
    monkeypatch.setattr(INPUT_PATH, lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "Error: Cannot divide by zero." in captured.out
