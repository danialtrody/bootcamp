def extract_value(line: str, key: str) -> str:
    after_key = line.split(f"[{key}:")[1]
    value = after_key.split("]")[0]
    return value
