from typing import Dict


def analyze_log_content(log_content: str) -> Dict[str, int]:
    number_of_error: Dict[str, int] = {}

    for word in log_content.split():
        if word in ("ERROR", "WARNING", "INFO"):
            capitalized_word = word.capitalize()
            number_of_error[capitalized_word] = (
                number_of_error.get(capitalized_word, 0) + 1
            )

    return number_of_error
