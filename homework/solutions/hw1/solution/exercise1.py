def extract_pid(log_line: str) -> int:
    split_by_pid = log_line.split("pid:")[1]
    split_by_bracket = split_by_pid.split("]")[0]
    return int(split_by_bracket)
