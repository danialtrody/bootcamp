import os


class ConfigError(Exception):
    """Base exception for configuration errors"""


class ConfigFileNotFoundError(ConfigError):
    """raised when config file doesn't exist"""


class ConfigParseError(ConfigError):
    """raised when config file has invalid format"""


class ConfigValidationError(ConfigError):
    """raised when config values are invalid"""


def parse_config(filename: str, required_keys: list[str]) -> dict[str, str]:
    if not os.path.exists(filename):
        raise ConfigFileNotFoundError(f"File '{filename}' not found")

    result: dict[str, str] = {}

    with open(filename, "r") as file:
        for index, line in enumerate(file):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ConfigParseError(f"Invalid format on line {index}: {line}")

            key, value = line.split("=")
            result[key] = value

    missing_keys = [key for key in required_keys if key not in result]
    if missing_keys:
        raise ConfigValidationError(f"Missing keys: {missing_keys}")

    return result
