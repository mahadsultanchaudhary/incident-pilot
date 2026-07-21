from typing import Any
from ..models import Incident


class PostmortemGenerator:
    def generate(self, incident: Incident, analysis: dict[str, Any]) -> str:
        fixes = "\n".join(f"- {item}" for item in analysis.get("suggested_fixes", []))
        next_steps = "\n".join(f"- {item}" for item in analysis.get("next_steps", []))
        return (f"# {incident.title}\n\n## Impact\n{analysis.get('executive_summary', incident.summary)}\n\n"
                f"## Root cause\n{analysis.get('root_cause', incident.summary)}\n\n## Resolution\n{fixes}\n\n## Follow-up\n{next_steps}")
