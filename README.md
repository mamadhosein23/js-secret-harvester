# JS Asset & Endpoint Harvester

A lightweight static analysis tool designed to audit client-side JavaScript bundles, extract hidden API endpoints, and identify exposed sensitive credentials using heuristic Shannon entropy scoring and pattern matching.

---

## Key Features

- **Automated JS Discovery:** Crawls and extracts all loaded script URLs from target web pages.
- **Endpoint Extraction:** Parses relative routes, internal API paths, and external service URLs.
- **Shannon Entropy Analysis:** Identifies high-entropy strings (e.g., cryptographic keys, access tokens) to minimize false positives compared to standard regex-only approaches.
- **Modular Architecture:** Clean separation of concerns across network fetching, text parsing, and statistical scoring modules.

---

## Architecture Overview
```text
harvester/
├── __init__.py       # Package initialization and public interface
├── fetcher.py        # HTTP client for script discovery and source retrieval
├── entropy.py        # Shannon entropy calculation engine
└── parser.py         # Route and token extraction logic
