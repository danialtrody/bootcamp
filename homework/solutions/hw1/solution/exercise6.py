import sys

def print_primitive_types_sizes() -> None:
    int_types = [0, 1, 42, -1000, 123456789]
    float_types = [0.0, 1.5, -3.14, 2.71828, 1e10]
    complex_types = [0j, 1+2j, -3+4j, 2.5+3.5j, 1e5+1e2j]
    str_types = ["", "a", "hello", "Python", "long string"]
    bytes_types = [b"", b"a", b"hello", b"Python", b"long bytes"]

    for value in int_types:
        print(f"Type: {type(value)}, Value: {value}, Size: {sys.getsizeof(value)} bytes")
    for value in float_types:
        print(f"Type: {type(value)}, Value: {value}, Size: {sys.getsizeof(value)} bytes")
    for value in complex_types:
        print(f"Type: {type(value)}, Value: {value}, Size: {sys.getsizeof(value)} bytes")
    for value in str_types:
        print(f"Type: {type(value)}, Value: {value}, Size: {sys.getsizeof(value)} bytes")
    for value in bytes_types:
        print(f"Type: {type(value)}, Value: {value}, Size: {sys.getsizeof(value)} bytes")

if __name__ == "__main__":
    print_primitive_types_sizes()