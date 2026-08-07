# Runbook Generator

Generate production-ready operational runbooks from production incident descriptions using Large Language Models (LLMs).

---

## Overview

AI Runbook Generator transforms production incident descriptions into structured, actionable operational runbooks.

Instead of manually documenting investigation steps during an outage, engineers can provide a concise incident summary and receive a comprehensive Markdown runbook that includes:

- Executive Summary
- Initial Assessment
- Investigation Steps
- Possible Root Causes
- Immediate Mitigation
- Rollback Strategy
- Verification Steps
- Escalation Guidance
- Operational References

The project is designed for Site Reliability Engineers (SREs), DevOps Engineers, Platform Engineers, and Incident Responders.

---

## Why This Project?

During production incidents, engineers often spend valuable time gathering investigation steps, rollback procedures, Kubernetes commands, and escalation guidance.

AI Runbook Generator accelerates incident response by producing consistent, structured operational runbooks that can be reviewed, customized, and executed by engineering teams.

This project is also designed as one of the foundational modules of a future AI Reliability Platform.

---

## Features

- Generate operational runbooks from production incident descriptions
- Produce structured Markdown output
- Kubernetes-oriented troubleshooting guidance
- Rollback recommendations
- Investigation and verification workflows
- Escalation guidance
- Provider-agnostic LLM architecture
- Modular and reusable project structure
- File-based input and output

---

## Architecture

```text
                app.py
                   │
                   ▼
         RunbookGenerator
                   │
                   ▼
             LLMClient
                   │
                   ▼
      LLM Provider (OpenAI)
                   │
                   ▼
        Markdown Runbook
                   │
                   ▼
             runbooks/
```

The application separates responsibilities into reusable components:

- Configuration
- LLM Client
- Prompt Engineering
- Runbook Generation
- File Utilities

This architecture allows future support for additional LLM providers without changing the business logic.

---

## Project Structure

```text
ai-runbook-generator/

├── runbooks/
├── sample_data/
├── src/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── __init__.py
│
├── tests/
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

Clone the repository:

```bash
git clone git@github.com:YOUR_USERNAME/ai-runbook-generator.git
cd ai-runbook-generator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```text
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.5
LLM_API_KEY=your_api_key_here
```

---

## LLM Provider

The current implementation uses the OpenAI Responses API.

The application is designed with a provider-agnostic architecture, allowing future support for additional providers without changing the business logic.

Planned future providers include:

- Anthropic Claude
- Google Gemini
- Azure OpenAI
- Ollama (Local LLMs)

---


## Usage

Place an incident description inside:

```text
sample_data/payment-service-500.txt
```

Run:

```bash
python app.py
```

The generated runbook will be written to:

```text
runbooks/payment-service-runbook.md
```

---

## Example Input

```text
Payment service is returning HTTP 500 errors.

CPU utilization increased from 35% to 95%.

Pods restarted three times.

Deployment completed 10 minutes before the incident.
```

---

## Example Output

The generated Markdown runbook includes:

- Executive Summary
- Initial Assessment
- Investigation Steps
- Possible Root Causes
- Immediate Mitigation
- Rollback Strategy
- Verification Steps
- Escalation Guidance
- Operational References

---

## Roadmap

### Version 1.0

- AI-powered runbook generation
- Markdown output
- Modular architecture
- OpenAI support

### Future Enhancements

- Multiple LLM providers
- CLI arguments
- Interactive mode
- Template customization
- PDF export
- HTML export
- Knowledge base integration
- Enterprise deployment
- Shared AI Reliability Platform core library

---

## License

This project is released under a **Proprietary License**.

You are welcome to view the source code for learning and evaluation purposes. However, copying, modifying, redistributing, or using this software in commercial products is prohibited without prior written permission.

See the `LICENSE` file for the complete license terms.