from agentic_reliability_framework.core.reliability_signal import signal_to_reliability
from app.models.incident_models import IncidentReport

def process_incident(report: IncidentReport) -> float:
    reliability = signal_to_reliability(report.value, signal_type=report.signal_type)
    return reliability
