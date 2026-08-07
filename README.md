# ReliabilityPlatform

ReliabilityPlatform is an AI-powered Reliability Engineering platform designed to help engineering teams improve operational excellence through intelligent automation.

The platform provides a collection of independent yet integrated AI-powered modules that assist with production incident response, operational documentation, and future reliability engineering workflows.

The long-term vision is to build a comprehensive Reliability Engineering platform that enables engineers to investigate incidents, generate operational knowledge, improve system reliability, and automate repetitive operational tasks using Large Language Models (LLMs).

---

## Current Features

### AI Incident Commander

Analyzes production incidents using an LLM and produces structured incident analysis including:

- Executive Summary
- Possible Root Cause
- Confidence Level
- Immediate Actions
- Business Impact

---

### AI Runbook Generator

Generates production-ready operational runbooks from incident descriptions, enabling engineering teams to create consistent operational documentation quickly.

---

## Platform Architecture

```
ReliabilityPlatform/
│
├── core/
│   ├── config.py
│   ├── llm_client.py
│   └── logger.py
│
├── incident_commander/
│
├── runbook_generator/
│
├── docs/
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Design Principles

ReliabilityPlatform is built around a few core engineering principles:

- Modular architecture
- Shared platform components
- Independent, reusable modules
- Consistent project structure
- Production-quality engineering practices
- AI-assisted Reliability Engineering

Each module can run independently while sharing common platform services provided by the Core SDK.

---

## Technology Stack

- Python 3
- OpenAI API
- Pydantic
- python-dotenv

---

## Repository Structure

```
core/
```

Shared platform services used by all modules.

Current shared components:

- Configuration Management
- LLM Client
- Logging

```
incident_commander/
```

AI-powered incident analysis.

```
runbook_generator/
```

AI-powered operational runbook generation.

---

## Getting Started

### Clone the repository

```bash
git clone git@github.com:sg/ReliabilityPlatform.git
cd ReliabilityPlatform
```

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root.

Example:

```text
LLM_API_KEY=your_api_key
LLM_MODEL=gpt-5-mini
```

---

## Running the Applications

### AI Incident Commander

```bash
python -m incident_commander.app incident_commander/sample_data/payment-service-500.txt
```

---

### AI Runbook Generator

```bash
python -m runbook_generator.app runbook_generator/sample_data/payment-service-500.txt
```

---

## Current Release

**v0.1.0 — Foundation**

This release establishes the foundation of the ReliabilityPlatform, including:

- Shared Core SDK
- AI Incident Commander
- AI Runbook Generator
- Common LLM client
- Shared logging infrastructure
- Unified project architecture

---

## License

This project is licensed under the terms described in the LICENSE file.

© 2026 SGOPAL. All Rights Reserved.