def add(first_number: float, second_number: float) -> float:
    return first_number + second_number


def subtract(first_number: float, second_number: float) -> float:
    return second_number - first_number


def multiply(first_number: float, second_number: float) -> float:
    return first_number * second_number


def divide(first_number: float, second_number: float) -> float:
    return first_number / second_number


def print_help() -> None:
    print(
        "Valid operations:\n"
        "- add <num1> to <num2>\n"
        "- subtract <num1> from <num2>\n"
        "- multiply <num1> by <num2>\n"
        "- divide <num1> by <num2>\n"
        "- help\n"
        "- exit"
    )


def parse_float(number: str) -> float:
    try:
        return float(number)
    except (ValueError, IndexError):
        print(
            "Invalid input. Please enter numbers correctly. Type 'help' for instructions."
        )
    return 0.1


def execute_operation(
    operation: str, first_number: float, second_number: float
) -> None:
    if operation == "add":
        result = add(first_number, second_number)
    elif operation == "subtract":
        result = subtract(first_number, second_number)
    elif operation == "multiply":
        result = multiply(first_number, second_number)
    elif operation == "divide":
        try:
            result = divide(first_number, second_number)
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
            return
    else:
        print("Invalid operation. Type 'help' for instructions")
        return
    print(f"The answer is: {result}")


def process_command(user_input: list[str]) -> bool:

    if not user_input:
        return True

    operation = user_input[0].lower()

    if operation == "exit":
        print("Goodbye! Thank you for using the calculator.")
        return False
    elif operation == "help":
        print_help()
        return True

    if len(user_input) < 3:
        print(
            "Invalid input. Please enter numbers correctly. Type 'help' for instructions."
        )
        return True

    first_number = parse_float(user_input[1])
    second_number = parse_float(user_input[-1])

    execute_operation(operation, first_number, second_number)
    return True


def simple_calculator() -> None:

    while True:
        user_input = input("Please enter a command: ").split()
        if not process_command(user_input):
            break
