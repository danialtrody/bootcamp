from functools import wraps

SUPPORTED_TYPES = (int, float, str, list, dict, bool, type(None))


def _check_args(args, annotations_keys, annotations_values) -> None:
    for index, arg in enumerate(args):
        if index < len(annotations_values):
            expected_type = annotations_values[index]
            if expected_type in SUPPORTED_TYPES and not isinstance(arg, expected_type):
                raise TypeError(
                    f"Argument '{annotations_keys[index]}' must be of type "
                    f"{expected_type}, got {type(arg)} instead."
                )


def _check_kwargs(kwargs, function_annotations) -> None:
    for key, value in kwargs.items():
        if function_annotations.get(key):
            expected_type = function_annotations[key]
            if expected_type in SUPPORTED_TYPES and not isinstance(
                value, expected_type
            ):
                raise TypeError(
                    f"Argument '{key}' must be of type {expected_type}, got {type(value)} instead."
                )


def _check_return(result, expected_return_type) -> None:
    if expected_return_type in SUPPORTED_TYPES and not isinstance(
        result, expected_return_type
    ):
        raise TypeError(
            f"Return value must be of type {expected_return_type}, got {type(result)} instead."
        )


def type_check(function) -> None:
    @wraps(function)
    def wrapper(*args, **kwargs):
        function_annotations = function.__annotations__
        annotations_values = list(function_annotations.values())[:-1]
        annotations_keys = list(function_annotations.keys())[:-1]

        _check_args(args, annotations_keys, annotations_values)
        _check_kwargs(kwargs, function_annotations)

        result = function(*args, **kwargs)
        expected_return_type = function_annotations.get("return")

        _check_return(result, expected_return_type)

        return result

    return wrapper


@type_check
def format_data(name: str, age: int, data: dict, other_info=None) -> str:
    other_info_str = f", Other Info : {other_info}" if other_info else ""
    return f"Name: {name}, Age: {age}, Data: {data['key']}{other_info_str}"
