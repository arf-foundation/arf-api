import random
from agentic_reliability_framework.core.governance.risk_engine import RiskEngine
from app.models.intent_models import IntentSimulation

risk_engine = RiskEngine()

def simulate_intent(intent: IntentSimulation) -> dict:
    # Simplified risk evaluation – in reality you'd pass proper context
    risk_score = random.uniform(0, 1)  # placeholder
    if risk_score < 0.2:
        recommendation = "safe_to_execute"
    elif risk_score < 0.6:
        recommendation = "requires_approval"
    else:
        recommendation = "blocked"
    return {"risk_score": risk_score, "recommendation": recommendation}
