# Incident Commander

An AI-powered command-line application that analyzes production incidents using a Large Language Model (LLM) and generates structured, validated incident reports.

---

## Overview

AI Incident Commander demonstrates how modern AI applications can be built using sound software engineering principles.

Instead of returning free-form AI responses, the application converts the model output into a validated **Pydantic** domain model, making the results reliable, machine-readable, and suitable for future automation such as APIs, dashboards, AI agents, and operational workflows.

This project focuses on **AI Engineering**, not just LLM integration.

---

## Why This Project?

Most LLM applications return unstructured text that is difficult to validate, reuse, or integrate into software systems.

This project demonstrates a production-oriented approach by:

- Separating AI prompts from business logic
- Validating AI responses using Pydantic
- Following Clean Architecture principles
- Implementing robust error handling
- Producing structured outputs suitable for downstream automation

---

## Features

- AI-powered production incident analysis
- Structured incident reports
- Prompt management
- Pydantic-based response validation
- JSON parsing and schema validation
- Clean layered architecture
- Environment-based configuration
- Custom exception handling
- Professional command-line interface

---

## Architecture

```text
                     Incident File
                           │
                           ▼
                        app.py
                           │
                           ▼
                  IncidentAnalyzer
                   │             │
                   ▼             ▼
           Prompt Builder   OpenAI Client
                   │
                   ▼
              OpenAI GPT Model
                   │
                   ▼
              JSON Response
                   │
                   ▼
          Pydantic Validation
                   │
                   ▼
            IncidentAnalysis
                   │
                   ▼
          Formatted CLI Report
```

---

## Project Structure

```text
ai-incident-commander/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
│
├── sample_data/
│   ├── payment-service-500.txt
│   ├── database-latency.txt
│   ├── kubernetes-node-failure.txt
│   ├── memory-leak.txt
│   └── kafka-consumer-lag.txt
│
├── src/
│   ├── config.py
│   ├── exceptions.py
│   ├── incident_analyzer.py
│   ├── openai_client.py
│   │
│   ├── prompts/
│   │   └── incident_prompt.py
│   │
│   └── models/
│       └── incident_analysis.py
│
└── tests/
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd ai-incident-commander
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_openai_api_key
```

---

## Usage

Run the application:

```bash
python app.py sample_data/payment-service-500.txt
```

The application generates a structured report containing:

- Executive Summary
- Possible Root Cause
- Confidence Level
- Immediate Actions
- Business Impact

---

## Sample Output

```text
==================================================
              AI INCIDENT COMMANDER
==================================================

Executive Summary
--------------------------------------------------
...

Possible Root Cause
--------------------------------------------------
...

Confidence Level
--------------------------------------------------
...

Immediate Actions
--------------------------------------------------
1. ...
2. ...
3. ...

Business Impact
--------------------------------------------------
...
```

---

## Technologies Used

- Python 3.13
- OpenAI Python SDK
- Pydantic v2
- python-dotenv
- Git
- GitHub

---

## Engineering Concepts Demonstrated

This project demonstrates:

- Prompt Engineering
- Structured AI Outputs
- Pydantic Models
- JSON Parsing
- Schema Validation
- Clean Architecture
- Separation of Concerns
- Domain-Driven Design
- Custom Exception Handling
- Command-Line Application Design

---

## Lessons Learned

Through this project I gained practical experience with:

- Designing AI applications using clean architecture
- Separating prompts, business logic, and configuration
- Converting LLM responses into validated domain models
- Using Pydantic for schema validation
- Implementing robust exception handling
- Building reusable AI components instead of one-off scripts

---

## Future Enhancements

Potential future enhancements include:

- REST API
- Web interface
- Docker support
- Automated testing with pytest
- CI/CD pipeline
- Support for logs, metrics, and Kubernetes events
- Integration into a larger AI Reliability Platform

---

## License

This project is licensed under the MIT License.