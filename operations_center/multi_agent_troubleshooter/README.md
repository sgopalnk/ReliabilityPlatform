# Multi-Agent Troubleshooter

The Multi-Agent Troubleshooter coordinates specialized troubleshooting agents to investigate production incidents from multiple technical perspectives.

The MVP focuses on evidence-based investigation across CPU, memory, and network signals.

## Purpose

A production incident can involve multiple infrastructure signals simultaneously.

Instead of relying on a single analysis path, the Multi-Agent Troubleshooter delegates investigation to specialized agents and combines their findings into a structured result.

The module is designed to:

- investigate production incidents using multiple specialized agents
- separate technical investigation responsibilities
- collect structured findings from each agent
- tolerate individual agent failures
- return a consistent troubleshooting result
- remain provider-agnostic through the platform LLM client

## Architecture

```text
Incident
   |
   v
MultiAgentTroubleshooter
   |
   v
TroubleshootingCoordinator
   |
   +-------------------+-------------------+
   |                   |                   |
   v                   v                   v
CPU Agent          Memory Agent        Network Agent
   |                   |                   |
   +-------------------+-------------------+
                       |
                       v
             TroubleshootingResult

## Finding Synthesis

After the specialized agents complete their investigation, the FindingSynthesizer evaluates their findings collectively.

The synthesizer produces a structured SynthesisResult containing:

- overall summary
- key findings
- correlations between findings
- conflicts or contradictory findings
- evidence-based root-cause hypothesis
- confidence score

The synthesizer is designed to distinguish observed evidence from hypotheses. It should not claim a definitive root cause when the available evidence is insufficient.

The complete result returned by MultiAgentTroubleshooter is a TroubleshootingAnalysis containing both:

- TroubleshootingResult — raw findings and agent failures
- SynthesisResult — cross-agent analysis

## Failure Handling

An individual agent failure does not terminate the investigation.

For example:

CPU Agent       -> success
Memory Agent    -> failure
Network Agent   -> success

The coordinator records the Memory Agent failure while preserving the successful findings.

The resulting investigation status is:

- completed — all configured agents succeeded
- partial — some agents succeeded and some failed
- failed — no successful findings were produced

## Input Validation

The troubleshooter rejects empty or whitespace-only incident descriptions.

Examples:

""
"   "

Both are rejected with ValueError: Incident description cannot be empty.

## CLI Usage

Run the troubleshooter with:

python -m operations_center.multi_agent_troubleshooter.app "<incident>"

The CLI returns the complete investigation and synthesis as JSON.

If no incident or only whitespace is provided, the CLI displays the usage message instead of starting an investigation.

## Testing

Run the complete test suite:

pytest

The test suite covers CLI behavior, input validation, specialized agents, coordinator behavior, agent failure handling, finding synthesis, service orchestration, integration behavior, and end-to-end behavior.

## Design Principles

### Evidence Before Conclusions

The module separates observed evidence from hypotheses. Correlation or temporal association should not automatically be treated as a confirmed root cause.

### Specialized Responsibilities

Each troubleshooting agent focuses on a specific technical perspective rather than attempting to investigate every possible failure mode.

### Failure Isolation

A failure in one agent should not prevent the remaining agents from contributing useful findings.

### Structured Output

Pydantic models provide consistent contracts between agents, the coordinator, the synthesizer, and consuming applications.

### Provider Agnostic

LLM interaction is handled through the shared platform LLM client rather than coupling the module directly to a specific provider.

### Modular Architecture

Investigation, coordination, synthesis, prompts, and models remain separated so individual components can evolve independently.
