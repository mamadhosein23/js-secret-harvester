"""
Information entropy calculation utilities.
"""

from collections import Counter
import math


def calculate_entropy(data: str) -> float:
    """Calculate the Shannon Entropy of a string using an optimized mathematical form.

    H(X) = log2(N) - (1/N) * sum(count * log2(count))
    """
    if not data:
        return 0.0

    length = len(data)
    counts = Counter(data)

    # Fast path: all characters are identical
    if len(counts) == 1:
        return 0.0

    # Mathematically equivalent to standard Shannon entropy, but reduces floating-point divisions inside the loop
    sum_c_log_c = sum(count * math.log2(count) for count in counts.values())
    return math.log2(length) - (sum_c_log_c / length)


def is_high_entropy(data: str, threshold: float = 4.5, min_len: int = 16) -> bool:
    """Determine if a token contains high entropy above the specified threshold.

    Short strings are excluded because Shannon entropy cannot reliably distinguish
    randomness from small sample sizes.
    """
    if not data or len(data) < min_len:
        return False

    return calculate_entropy(data) >= threshold
