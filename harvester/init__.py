"""
JS Static Analysis & Endpoint Harvester.

Package initialization and public API exposure.
"""

from .entropy import calculate_entropy, is_high_entropy
from .fetcher import JSScraper
from .parser import extract_endpoints, extract_potential_secrets

__version__ = "0.1.0"
__author__ = "Mohammad Hossein"

__all__ = [
    # Metadata
    "__version__",
    "__author__",
    # Entropy analysis
    "calculate_entropy",
    "is_high_entropy",
    # Networking / Fetching
    "JSScraper",
    # Parsing & Analysis
    "extract_endpoints",
    "extract_potential_secrets",
]
