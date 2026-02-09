from typing import List, Dict

MIN_SCORE = 0
MAX_SCORE = 100
PASSING_SCORE = 60
INITIAL_LOWEST_SCORE = MAX_SCORE


def calculate_test_statistics(scores: List[int]) -> Dict[str, float | int]:

    total = 0
    count = 0
    passed = 0
    failed = 0
    highest = 0
    lowest = INITIAL_LOWEST_SCORE

    for score in scores:
        if MIN_SCORE <= score <= MAX_SCORE:
            total += score
            count += 1
            highest = max(highest, score)
            lowest = min(lowest, score)

            if score >= PASSING_SCORE:
                passed += 1
            else:
                failed += 1

    if count == 0:
        return empty_statistics()

    return {
        "average": calculate_average(total, count),
        "highest": highest,
        "lowest": lowest,
        "passed": passed,
        "failed": failed,
        "pass_rate": calculate_pass_rate(passed, count),
    }


def empty_statistics() -> Dict[str, float | int]:
    return {
        "average": 0,
        "highest": 0,
        "lowest": 0,
        "passed": 0,
        "failed": 0,
        "pass_rate": 0,
    }


def calculate_average(total: int, count: int) -> float:
    return total / count


def calculate_pass_rate(passed: int, count: int) -> float:
    return (passed / count) * 100


