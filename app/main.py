from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_incidents, routes_risk, routes_intents, routes_history, routes_governance
from app.core.config import settings
from app.api.deps import limiter
from agentic_reliability_framework.core.governance.risk_engine import RiskEngine
import os

app = FastAPI(title="ARF API Control Plane", version="0.3.0")

# Set up rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Initialize RiskEngine (once)
hmc_model_path = os.getenv("ARF_HMC_MODEL", "models/hmc_model.json")
use_hyperpriors = os.getenv("ARF_USE_HYPERPRIORS", "false").lower() == "true"
app.state.risk_engine = RiskEngine(
    hmc_model_path=hmc_model_path,
    use_hyperpriors=use_hyperpriors,
    n0=1000,
    hyperprior_weight=0.3
)

# Include routers
app.include_router(routes_incidents.router, prefix="/api/v1", tags=["incidents"])
app.include_router(routes_risk.router, prefix="/api/v1", tags=["risk"])
app.include_router(routes_intents.router, prefix="/api/v1", tags=["intents"])
app.include_router(routes_history.router, prefix="/api/v1", tags=["history"])
app.include_router(routes_governance.router, prefix="/api/v1", tags=["governance"])

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
