from solution.exercise2 import simple_calculator


def test_exit_input(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "exit")
    simple_calculator()
    captured = capsys.readouterr()

    assert captured.out.strip() == ("Goodbye! Thank you for using the calculator.")


def test_help_input(monkeypatch, capsys):
    inputs = iter(["help", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
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


def test_invalid_input(monkeypatch, capsys):
    inputs = iter(["add-sub", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert (
        "Invalid input. Please enter numbers correctly. Type 'help' for instructions."
        in captured.out
    )


def test_add_operation(monkeypatch, capsys):
    inputs = iter(["add 2 to 5", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "7.0" in captured.out


def test_subtract_operation(monkeypatch, capsys):
    inputs = iter(["subtract 2 from 5", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "3.0" in captured.out


def test_multiply_operation(monkeypatch, capsys):
    inputs = iter(["multiply 2 by 5", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "10.0" in captured.out


def test_valid_divide_operation(monkeypatch, capsys):
    inputs = iter(["divide 10 by 5", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "2.0" in captured.out


def test_zero_divide_operation(monkeypatch, capsys):
    inputs = iter(["divide 10 by 0", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    simple_calculator()
    captured = capsys.readouterr()

    assert "Error: Cannot divide by zero." in captured.out
