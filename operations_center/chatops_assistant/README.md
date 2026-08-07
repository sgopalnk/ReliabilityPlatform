# ChatOps Assistant

An AI-powered Operations Copilot for Reliability Engineers.

ChatOps Assistant is part of the ReliabilityPlatform and helps engineers understand production systems, reliability engineering concepts, Kubernetes, Linux, cloud infrastructure, networking, observability, and incident management through natural language conversations.

---

## Features

- Natural language question answering
- Reliability Engineering concepts
- Kubernetes explanations
- Linux command explanations
- AWS service explanations
- Networking concepts
- Observability guidance
- Incident management guidance
- Runbook explanation
- Incident analysis explanation

---

## Project Structure

```
chatops_assistant/
├── app.py
├── README.md
├── examples/
├── sample_data/
├── src/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── exceptions.py
│   ├── prompt_builder.py
│   └── response_formatter.py
└── tests/
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file.

```
LLM_API_KEY=<your_api_key>
LLM_MODEL=<model_name>
```

---

## Usage

From the ReliabilityPlatform root:

```bash
python -m operations_center.chatops_assistant.app
```

Example:

```
Ask a Reliability Engineering question:
```

```
What is MTTR?
```

---

## Example Questions

- What is MTTR?
- Explain CrashLoopBackOff.
- Explain Kubernetes readiness probes.
- How do I investigate high CPU usage?
- Explain SLOs and SLIs.
- Explain this runbook.
- Explain this incident analysis.
- What information should I collect before escalating to the database team?

---

## Running Tests

From the ReliabilityPlatform root:

```bash
pytest operations_center/chatops_assistant/tests
```

---

## Roadmap

Completed

- Conversational AI interface
- Prompt builder
- Structured responses
- Unit tests

Future

- Conversation history
- Incident context
- Runbook context
- Log explanation
- Metric explanation
- Trace explanation
- Knowledge base integration