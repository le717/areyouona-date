from math import floor, sqrt


__all__ = ["calculate_mean", "calculate_sd", "calculate_z"]


def calculate_mean(vals: list) -> int:
    """Calculate a mean."""
    return floor(sum(vals) / len(vals))


def calculate_sd(m: int, vals: list) -> int:
    """Calculate a sample standard deviation."""
    diffs = [val - m for val in vals]
    n = len(vals) - 1
    v = sum(num ** 2 for num in diffs) / n
    return floor(sqrt(v))


def calculate_z(x: int, m: int, sd: int) -> float:
    """Calculate a z-score, rounded to two decimal places."""
    return round((x - m) / sd, 2)
