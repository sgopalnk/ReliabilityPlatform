# ReliabilityPlatform Module Template

This document defines the standard structure for every module in the ReliabilityPlatform.

---

# Standard Module Layout

```
module/
│
├── README.md
├── app.py
├── __init__.py
│
├── examples/
├── sample_data/
├── tests/
│
└── src/
    ├── __init__.py
    ├── exceptions.py
    │
    ├── models/
    ├── prompts/
    ├── services/
    └── utils/        # Create only when needed
```

---

# Responsibilities

## app.py

Application entry point.

Responsible only for:

- Reading user input
- Calling the module service
- Displaying output

No business logic.

---

## services/

Contains the main orchestration logic.

Usually contains one primary service.

Examples:

- IncidentAnalyzer
- RunbookGenerator
- ChatOpsAssistant
- MultiAgentTroubleshooter

---

## models/

Pydantic request/response models.

No business logic.

---

## prompts/

Prompt templates and prompt builders.

No LLM calls.

---

## exceptions.py

Module-specific exceptions.

---

## utils/

Utility functions.

Create only when there is a genuine need.

Avoid creating empty utility packages.

---

# Shared Components

Every module must reuse the shared Core SDK.

Never duplicate:

- config.py
- llm_client.py
- logger.py

Import them from:

```
core/
```

---

# Engineering Principles

- Production-quality Python
- Single Responsibility Principle
- Modular design
- Testable code
- Comprehensive docstrings
- Comments explain WHY, not WHAT
- Reuse shared components
- Avoid unnecessary abstractions

---

# Testing

Every module should contain unit tests.

Tests should run from the repository root:

```bash
pytest
```

---

# Release Checklist

Before committing:

- All tests pass
- README updated
- Examples added
- No duplicated infrastructure
- No __pycache__ committed
- Imports use shared Core SDK