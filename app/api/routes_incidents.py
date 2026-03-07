from fastapi import APIRouter, HTTPException
from app.models.incident_models import IncidentReport, IncidentResponse
from app.services.incident_service import process_incident
from app.core.storage import incident_history

router = APIRouter()

@router.post("/report_incident", response_model=IncidentResponse)
async def report_incident(report: IncidentReport):
    try:
        reliability = process_incident(report)
        incident_history.append({
            "service": report.service,
            "signal_type": report.signal_type,
            "value": report.value,
            "reliability": reliability
        })
        return IncidentResponse(service=report.service, reliability=reliability)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
