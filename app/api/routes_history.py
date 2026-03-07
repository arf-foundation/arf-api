from fastapi import APIRouter
from app.core.storage import incident_history

router = APIRouter()

@router.get("/history")
async def get_history():
    return {"incidents": incident_history}
