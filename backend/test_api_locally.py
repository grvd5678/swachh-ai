import sys
import json
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.schemas import DisposalPlanRequest
from backend.decision_engine import decision_engine

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def test_engine():
    print("=" * 60)
    print("Testing Swachh.ai Decision Engine end-to-end...")
    print("=" * 60)

    req = DisposalPlanRequest(
        waste_description="I have a broken swollen power bank, an old CFL bulb, and some expired paracetamol tablets",
        location="Kolkata"
    )

    plan = decision_engine.generate_plan(req)
    print("\nGenerated Disposal Plan JSON:\n")
    print(json.dumps(plan.model_dump(), indent=2))

if __name__ == "__main__":
    test_engine()
