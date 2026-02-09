from typing import Callable
from functools import wraps


def count_calls(func: Callable):
    counter = 0
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal counter
        result = func(*args, **kwargs)
        counter += 1
        wrapper.call_count = counter
        return result

    wrapper.call_count = 0
    return wrapper



@count_calls
def greet(name: str) -> str:
    return f"Hello, {name}!"

