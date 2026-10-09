import sys
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import DisposalPlanRequest, DisposalPlanResponse
from backend.decision_engine import decision_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("swachh-api")

app = FastAPI(
    title="Swachh.ai API",
    description="Location-aware authoritative waste-disposal decision assistant",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local hackathon development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Swachh.ai Backend Decision Engine",
        "version": "1.0.0"
    }

@app.post("/api/disposal-plan", response_model=DisposalPlanResponse)
def get_disposal_plan(request: DisposalPlanRequest):
    logger.info(f"Received disposal plan request for location '{request.location}': {request.waste_description}")
    try:
        plan = decision_engine.generate_plan(request)
        return plan
    except Exception as e:
        logger.error(f"Error processing disposal plan: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
