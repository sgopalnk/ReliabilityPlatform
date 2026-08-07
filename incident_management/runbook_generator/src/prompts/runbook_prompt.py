RUNBOOK_PROMPT = """
You are an experienced Site Reliability Engineer.

Generate a clear, structured operational runbook in Markdown based on the production incident below.

The runbook should contain the following sections:

# Incident Runbook

## Executive Summary

Provide a concise summary of the incident.

## Initial Assessment

Describe the immediate observations.

## Investigation Steps

Provide a numbered list of investigation steps.

## Possible Root Causes

List the most likely causes.

## Immediate Mitigation

Describe actions to restore service.

## Rollback Strategy

If applicable, explain when and how to roll back.

## Verification Steps

Explain how to verify that the incident has been resolved.

## Escalation

Identify when the issue should be escalated.

## References

Suggest dashboards, logs, metrics, or documentation that should be reviewed.

Production Incident:

{incident}
"""