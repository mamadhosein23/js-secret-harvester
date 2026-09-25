import math
from collections import Counter
def calculate_entropy(data: str) -> float:
    """محاسبه Shannon Entropy برای یک رشته."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    counts = Counter(data)
    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    return entropy
def is_high_entropy(data: str, threshold: float = 4.5, min_len: int = 16) -> bool:
    """بررسی اینکه آیا رشته آنتروپی بالا و طول مناسب برای توکن/کلید دارد یا خیر."""
  
