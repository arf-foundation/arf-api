from typing import Literal
from pydantic import BaseModel

class RiskResponse(BaseModel):
    system_risk: float
    status: Literal["low", "moderate", "high", "critical"]
