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