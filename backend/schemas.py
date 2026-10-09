from pydantic import BaseModel, Field
from typing import List, Literal

class DisposalPlanRequest(BaseModel):
    waste_description: str = Field(
        ...,
        description="Natural language description of waste items (e.g., 'A broken power bank, CFL bulb, expired syrup')",
        example="I have an old power bank, a fused CFL bulb, and some expired paracetamol tablets."
    )
    location: str = Field(
        default="Kolkata",
        description="Citizen's location / municipality context",
        example="Kolkata"
    )

class WasteItemDecision(BaseModel):
    item_name: str = Field(..., description="Name of the specific waste item identified")
    detected_category: str = Field(..., description="Authoritative waste classification category")
    handling_instruction: str = Field(..., description="Actionable immediate handling steps for the citizen")
    disposal_pathway: str = Field(..., description="Where and how to safely dispose of or surrender this item")
    hazard_reason: str = Field(..., description="Environmental or safety reason why this handling is required")
    confidence: Literal["high", "limited", "unsupported"] = Field(
        ...,
        description="Confidence level based on authoritative grounding: high (clear rule), limited (guidance exists but pathway is ambiguous), unsupported (no verified pathway)"
    )
    regulatory_source: str = Field(..., description="Authoritative document and rule citation retrieved")

class DisposalPlanResponse(BaseModel):
    location: str = Field(..., description="Location context used for the disposal plan")
    items: List[WasteItemDecision] = Field(..., description="Itemized disposal decisions")
    general_advisory: str = Field(..., description="Overarching citizen safety warning")

