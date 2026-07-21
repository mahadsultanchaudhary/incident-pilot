import json
from typing import Any
from openai import OpenAI
from ..config import get_settings
from ..models import Incident, LogEvent
from ..services.postmortem_generator import PostmortemGenerator
from ..services.timeline_builder import TimelineBuilder


class AIAnalysisService:
    """Builds a compact evidence context; raw log archives are never sent to the model."""
    def __init__(self):
        self.settings = get_settings()

    def _context(self, incident: Incident, events: list[LogEvent]) -> dict[str, Any]:
        return {"incident": {"title": incident.title, "service": incident.service, "severity": incident.severity,
            "summary": incident.summary, "occurrences": incident.occurrence_count},
            "events": [{"time": e.timestamp.isoformat(), "level": e.level, "message": e.message,
                        "endpoint": e.endpoint, "status": e.status_code} for e in events[:12]]}

    def analyze(self, incident: Incident, events: list[LogEvent]) -> dict[str, Any]:
        context = self._context(incident, events)
        fallback = self._fallback(incident, events)
        if not self.settings.openai_api_key:
            return fallback
        prompt = ("Analyze this incident evidence. Return JSON with executive_summary, root_cause, confidence, "
                  "affected_services, suggested_fixes, next_steps. Do not assume data beyond evidence.\n" + json.dumps(context))
        try:
            client = OpenAI(api_key=self.settings.openai_api_key, base_url=self.settings.openai_base_url or None)
            completion = client.chat.completions.create(model=self.settings.model_name,
                messages=[{"role": "system", "content": "You are a production incident analyst. Output only JSON."},
                          {"role": "user", "content": prompt}], response_format={"type": "json_object"})
            response = json.loads(completion.choices[0].message.content or "{}")
            return {**fallback, **response, "timeline": fallback["timeline"], "evidence": fallback["evidence"]}
        except Exception:
            return fallback

    def answer(self, incident: Incident, question: str, analysis: dict[str, Any]) -> str:
        if "confidence" in question.lower():
            return f"Root-cause confidence is {analysis.get('confidence', incident.root_cause_confidence):.0%}, based on repeated correlated failures and the captured stack trace."
        if "fix" in question.lower():
            return "Prioritize the suggested guardrail and add an integration test around the failing checkout path before the next deployment."
        return f"The available evidence points to {analysis.get('root_cause', incident.summary)}. The affected path is {incident.service}."

    def postmortem(self, incident: Incident, analysis: dict[str, Any]) -> str:
        return PostmortemGenerator().generate(incident, analysis)

    def _fallback(self, incident: Incident, events: list[LogEvent]) -> dict[str, Any]:
        root = incident.summary
        timeline = TimelineBuilder().build(events)
        return {"executive_summary": f"{incident.service} is experiencing {incident.occurrence_count} correlated failures affecting the monitored request path.",
                "timeline": timeline, "root_cause": root, "confidence": incident.root_cause_confidence,
                "affected_services": [incident.service], "suggested_fixes": ["Add explicit input validation before the failing operation.", "Add a bounded retry and timeout policy for dependent services."],
                "next_steps": ["Assign an owner and deploy a targeted mitigation.", "Create a regression test from this request correlation."],
                "evidence": [{"assertion": f"Repeated error signature in {incident.service}", "relevance": incident.root_cause_confidence}]}
