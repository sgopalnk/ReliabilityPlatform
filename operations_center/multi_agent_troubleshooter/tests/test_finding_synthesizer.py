from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFailure,
    AgentFinding,
    SynthesisResult,
    TroubleshootingResult,
)
from operations_center.multi_agent_troubleshooter.src.services.finding_synthesizer import (
    FindingSynthesizer,
)


def test_synthesizer_returns_structured_result() -> None:
    """Verify that the synthesizer converts the LLM response into a SynthesisResult."""

    llm_client = MagicMock()
    llm_client.generate.return_value = """
    {
        "summary": "CPU pressure correlates with increased latency.",
        "key_findings": [
            "CPU utilization reached 95%.",
            "Network latency increased."
        ],
        "correlations": [
            "CPU pressure coincides with increased network latency."
        ],
        "conflicts": [],
        "root_cause_hypothesis": "The recent deployment may have introduced CPU pressure.",
        "confidence": 0.88
    }
    """

    synthesizer = FindingSynthesizer(llm_client=llm_client)

    result = TroubleshootingResult(
        incident="Payment service is returning HTTP 500 errors.",
        findings=[
            AgentFinding(
                agent_name="CPU Agent",
                summary="High CPU detected.",
                evidence=["CPU usage reached 95%."],
                confidence=0.95,
            ),
            AgentFinding(
                agent_name="Network Agent",
                summary="Network latency increased.",
                evidence=["Latency increased to 2 seconds."],
                confidence=0.91,
            ),
        ],
        status="completed",
    )

    synthesis = synthesizer.synthesize(result)

    assert isinstance(synthesis, SynthesisResult)
    assert synthesis.summary == "CPU pressure correlates with increased latency."
    assert len(synthesis.key_findings) == 2
    assert len(synthesis.correlations) == 1
    assert synthesis.conflicts == []
    assert synthesis.confidence == 0.88

    llm_client.generate.assert_called_once()


def test_synthesizer_includes_agent_failures_in_input() -> None:
    """Verify that failed agents are included in the synthesis request."""

    llm_client = MagicMock()
    llm_client.generate.return_value = """
    {
        "summary": "CPU evidence is available but network analysis failed.",
        "key_findings": [
            "CPU utilization reached 95%."
        ],
        "correlations": [],
        "conflicts": [],
        "root_cause_hypothesis": "Insufficient evidence for a strong root cause hypothesis.",
        "confidence": 0.60
    }
    """

    synthesizer = FindingSynthesizer(llm_client=llm_client)

    result = TroubleshootingResult(
        incident="Payment service is returning HTTP 500 errors.",
        findings=[
            AgentFinding(
                agent_name="CPU Agent",
                summary="High CPU detected.",
                evidence=["CPU usage reached 95%."],
                confidence=0.95,
            )
        ],
        failures=[
            AgentFailure(
                agent_name="Network Agent",
                error="Network investigation failed.",
            )
        ],
        status="partial",
    )

    synthesis = synthesizer.synthesize(result)

    assert synthesis.confidence == 0.60

    prompt = llm_client.generate.call_args.args[0]

    assert "Network Agent" in prompt
    assert "Network investigation failed." in prompt
    assert "partial" in prompt
