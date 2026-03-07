from typing import Literal
from pydantic import BaseModel, Field
from typing import Literal

class IntentSimulation(BaseModel):
    action: Literal["restart_service", "scale_out", "rollback", "alert_team"] = Field(..., description="Proposed action")
    target: str = Field(..., description="Target component")

class IntentSimulationResponse(BaseModel):
    risk_score: float
    recommendation: Literal["safe_to_execute", "requires_approval", "blocked"]
