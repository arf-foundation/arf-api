from typing import Literal
from pydantic import BaseModel, Field
from typing import Literal

class IncidentReport(BaseModel):
    service: str = Field(..., description="Service name")
    signal_type: Literal["latency", "error_rate", "cpu", "memory"] = Field(..., description="Type of signal")
    value: float = Field(..., description="Measured value")

class IncidentResponse(BaseModel):
    service: str
    reliability: float
