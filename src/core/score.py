from math import floor, sqrt


__all__ = ["calculate_score"]


def __calculate_mean(vals: list) -> int:
    """Calculate a mean."""
    return sum(vals) // len(vals)


def __calculate_sd(mean: int, vals: list) -> int:
    """Calculate a sample standard deviation."""
    diffs = [val - mean for val in vals]
    n = len(vals) - 1
    v = sum(num ** 2 for num in diffs) / n
    return floor(sqrt(v))


def __calculate_z(x: int, m: int, sd: int) -> float:
    """Calculate a z-score, rounded to two decimal places."""
    return round((x - m) / sd, 2)


def calculate_score():
    pass
