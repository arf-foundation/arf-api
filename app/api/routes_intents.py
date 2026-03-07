from fastapi import APIRouter, HTTPException
from app.models.intent_models import IntentSimulation, IntentSimulationResponse
from app.services.intent_service import simulate_intent

router = APIRouter()

@router.post("/simulate_intent", response_model=IntentSimulationResponse)
async def simulate_intent_endpoint(intent: IntentSimulation):
    try:
        result = simulate_intent(intent)
        return IntentSimulationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
