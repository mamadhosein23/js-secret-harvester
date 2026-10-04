import re

from .entropy import calculate_entropy, is_high_entropy


# Match quoted absolute URLs and root-relative paths.
ENDPOINT_REGEX = re.compile(
    r"""(?P<quote>["'])(?P<endpoint>(?:https?://|/(?!/))[^"'\\\s<>]*)(?P=quote)""",
    re.IGNORECASE,
)

# Match quoted strings that may contain high-entropy secrets.
GENERIC_STRING_REGEX = re.compile(
    r"""(?P<quote>["'])(?P<value>[A-Za-z0-9_\-+/=]{16,128})(?P=quote)"""
)

# Match common secret formats.
KNOWN_KEY_PATTERNS: dict[str, re.Pattern[str]] = {
    "AWS Access Key": re.compile(
        r"\b(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)"
        r"[A-Z0-9]{16}\b"
    ),
    "Google API Key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "JSON Web Token (JWT)": re.compile(
        r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\b"
    ),
}


def extract_endpoints(content: str) -> set[str]:
    """Extract quoted absolute URLs and root-relative paths from JavaScript."""
    if not content:
        return set()

    return {
        match.group("endpoint")
        for match in ENDPOINT_REGEX.finditer(content)
    }


def _is_high_entropy_candidate(value: str) -> bool:
    """Check entropy using a lower threshold for hexadecimal strings."""
    if re.fullmatch(r"[0-9a-fA-F]+", value):
        return is_high_entropy(value, threshold=3.0, min_len=16)

    return is_high_entropy(value)


def extract_potential_secrets(content: str) -> set[str]:
    """Extract known-format secrets and likely high-entropy quoted strings."""
    if not content:
        return set()

    secrets: set[str] = set()

    # Find secrets matching known formats, even when they are not quoted.
    for pattern in KNOWN_KEY_PATTERNS.values():
        secrets.update(match.group(0) for match in pattern.finditer(content))

    # Use entropy as a heuristic for unknown secret formats.
    for match in GENERIC_STRING_REGEX.finditer(content):
        candidate = match.group("value")
        if _is_high_entropy_candidate(candidate):
            secrets.add(candidate)

    return secrets
