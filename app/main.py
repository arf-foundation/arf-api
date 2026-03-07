from fastapi import FastAPI
from app.api import routes_incidents, routes_risk, routes_intents, routes_history

app = FastAPI(title="ARF API Control Plane", version="0.1.0")

# Include routers
app.include_router(routes_incidents.router, prefix="/api/v1", tags=["incidents"])
app.include_router(routes_risk.router, prefix="/api/v1", tags=["risk"])
app.include_router(routes_intents.router, prefix="/api/v1", tags=["intents"])
app.include_router(routes_history.router, prefix="/api/v1", tags=["history"])

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
