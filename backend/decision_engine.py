import os
import json
import time
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

from backend.schemas import DisposalPlanRequest, DisposalPlanResponse, WasteItemDecision
from backend.rag_service import rag_service

load_dotenv()
logger = logging.getLogger("swachh-ai")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.8-flash")


def _gemini_generate(client: genai.Client, model: str, prompt: str, response_schema=None) -> str:
    """Call Gemini with exponential backoff on 503. Returns response text."""
    for attempt in range(3):
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=response_schema
            ) if response_schema else None

            kwargs = {"model": model, "contents": prompt}
            if config:
                kwargs["config"] = config

            response = client.models.generate_content(**kwargs)
            return response.text.strip()
        except ServerError as e:
            if "503" in str(e) and attempt < 2:
                wait = 2 ** attempt  # 1s, 2s
                logger.warning(f"Gemini 503 on {model}, retrying in {wait}s (attempt {attempt+1}/3)")
                time.sleep(wait)
            else:
                raise


class DecisionEngine:
    def __init__(self):
        self.client = None
        if GEMINI_API_KEY:
            try:
                self.client = genai.Client(api_key=GEMINI_API_KEY)
                logger.info(f"Gemini client initialized. Primary: {PRIMARY_MODEL}, Fallback: {FALLBACK_MODEL}")
            except Exception as e:
                logger.warning(f"Gemini init failed: {e}")
        else:
            logger.warning("GEMINI_API_KEY not set.")

    def extract_items_fallback(self, text: str) -> List[str]:
        separators = [",", " and ", " as well as ", " plus ", "\n", ";"]
        cleaned = text
        for sep in separators:
            cleaned = cleaned.replace(sep, "|")
        parts = [p.strip() for p in cleaned.split("|") if len(p.strip()) > 2]
        cleaned_items = []
        for p in parts:
            p_clean = p
            for prefix in ["i have an ", "i have a ", "i have ", "some ", "an ", "a "]:
                if p_clean.lower().startswith(prefix):
                    p_clean = p_clean[len(prefix):].strip()
            if p_clean:
                cleaned_items.append(p_clean)
        return cleaned_items or [text.strip()]

    def _call_with_model_fallback(self, prompt: str, response_schema=None) -> str:
        """Try PRIMARY_MODEL, fall back to FALLBACK_MODEL on failure."""
        for model in [PRIMARY_MODEL, FALLBACK_MODEL]:
            try:
                result = _gemini_generate(self.client, model, prompt, response_schema)
                logger.info(f"Gemini response from {model}.")
                return result
            except Exception as e:
                logger.warning(f"{model} failed: {e}")
        raise RuntimeError("All Gemini models unavailable.")

    def extract_items(self, text: str) -> List[str]:
        if not self.client:
            return self.extract_items_fallback(text)

        prompt = f"""Extract the individual physical waste items mentioned in this user text.
Return ONLY a comma-separated list of items, nothing else.
Examples:
User: "I have a broken power bank, an old CFL bulb and expired medicine"
Output: power bank, CFL bulb, expired medicine

User text: "{text}"
Output:"""

        try:
            raw = self._call_with_model_fallback(prompt)
            items = [i.strip() for i in raw.split(",") if i.strip()]
            return items if items else self.extract_items_fallback(text)
        except Exception as e:
            logger.error(f"Item extraction failed: {e}")
            return self.extract_items_fallback(text)

    def generate_plan(self, request: DisposalPlanRequest) -> DisposalPlanResponse:
        items = self.extract_items(request.waste_description)
        logger.info(f"Identified items for '{request.location}': {items}")

        item_contexts: List[Dict[str, Any]] = []
        for item in items:
            chunks = rag_service.retrieve_guidance(item, location=request.location, n_results=3)
            item_contexts.append({
                "item": item,
                "chunks": chunks,
                "context_str": rag_service.format_context_for_prompt(chunks)
            })

        if self.client:
            return self._generate_with_gemini(request.location, item_contexts)
        return self._generate_with_grounded_fallback(request.location, item_contexts)

    def _generate_with_gemini(self, location: str, item_contexts: List[Dict[str, Any]]) -> DisposalPlanResponse:
        context_payload = ""
        for idx, ic in enumerate(item_contexts, 1):
            context_payload += f"\n### Item {idx}: {ic['item']}\nAuthoritative Guidelines Retrieved:\n{ic['context_str']}\n"

        prompt = f"""You are Swachh.ai, an authoritative environmental waste-disposal decision assistant.
The citizen is located in: {location}.

TASK:
Produce an actionable, grounded disposal plan for each of the citizen's waste items.
Base your instructions strictly on the authoritative regulatory guidelines provided below.
DO NOT invent municipal collection centers or make up non-existent regulations.

CLASSIFICATION RULES (follow strictly):
- Power banks, lithium batteries, swollen batteries → "E-waste / Portable Battery"
- Chargers, cables, cords, adapters, phones, laptops, IT accessories → "E-waste (Consumer Electronics / IT)"
- CFL bulbs, tube lights, fluorescent lamps → "Domestic Hazardous Waste (Mercury-bearing)"
- Medicines, tablets, syrups, pharmaceuticals → "Domestic Hazardous Waste (Pharmaceutical)"
- Paints, pesticides, chemical solvents → "Domestic Hazardous Waste (Chemical)"
- Food, vegetable peels, organic matter → "Wet / Biodegradable Waste"

SAFETY & CONFIDENCE CRITERIA:
- If a clear regulatory rule and disposal pathway exists in the provided guidelines: set confidence to "high".
- If general guidance exists but the specific local pathway is ambiguous: set confidence to "limited".
- If no verified household disposal pathway exists: set confidence to "unsupported", and explicitly instruct the citizen NOT to discard it into general wet or dry garbage.

ITEMS AND RETRIEVED GUIDELINES:
{context_payload}
"""

        try:
            raw = self._call_with_model_fallback(prompt, response_schema=DisposalPlanResponse.model_json_schema())
            data = json.loads(raw)
            return DisposalPlanResponse(**data)
        except Exception as e:
            logger.error(f"Gemini plan generation failed: {e}. Using grounded fallback.")
            return self._generate_with_grounded_fallback(location, item_contexts)

    def _classify_item(self, item: str, chunks: List[Dict[str, Any]]) -> str:
        """Classify by item name first; chunk tags only as last resort."""
        name = item.lower()
        if any(k in name for k in ["power bank", "battery", "lithium"]):
            return "battery"
        if any(k in name for k in ["cfl", "bulb", "tube light", "fluorescent", "lamp"]):
            return "cfl"
        if any(k in name for k in ["medicine", "tablet", "syrup", "paracetamol", "capsule", "ointment", "pharmaceutical"]):
            return "pharmaceutical"
        if any(k in name for k in ["charger", "cable", "cord", "adapter", "phone", "laptop", "computer", "electronic"]):
            return "e-waste"
        if any(k in name for k in ["paint", "pesticide", "chemical", "thinner", "solvent"]):
            return "chemical"
        if any(k in name for k in ["peel", "vegetable", "fruit", "food", "leftover", "cooked", "raw", "kitchen", "organic", "leaf", "leaves", "grass", "flower"]):
            return "wet"
        return "general"

    def _generate_with_grounded_fallback(self, location: str, item_contexts: List[Dict[str, Any]]) -> DisposalPlanResponse:
        decisions: List[WasteItemDecision] = []

        for ic in item_contexts:
            item = ic["item"]
            chunks = ic["chunks"]
            top_chunk = chunks[0] if chunks else None
            source = f"{top_chunk.get('doc_title', 'CPCB Guidelines')} ({top_chunk.get('source_citation', 'Official Rules')})" if top_chunk else "General Solid Waste Guidelines"

            item_type = self._classify_item(item, chunks)

            if item_type == "battery":
                category = "E-waste / Portable Battery"
                handling = "Keep completely separate from household garbage. Do not puncture, crush, or expose to heat."
                pathway = "Surrender to an authorized EPR battery collection point or brand take-back programme. Do not hand over to informal scrap dealers or place in general waste."
                reason = "Lithium-ion cells pose severe thermal runaway and fire hazards if crushed in municipal garbage trucks."
            elif item_type == "cfl":
                category = "Domestic Hazardous Waste (Mercury-bearing)"
                handling = "Handle with extreme care. Wrap intact bulbs in paper or original cardboard to prevent breakage."
                pathway = "Hand over separately to municipal collection staff during hazardous waste collection. Do not place in ordinary household bins."
                reason = "Contains toxic mercury vapor that causes neurotoxic damage and environmental soil contamination."
            elif item_type == "pharmaceutical":
                category = "Domestic Hazardous Waste (Pharmaceutical)"
                handling = "Keep in original packaging or a sealed pouch. Never flush down sinks, toilets, or drains."
                pathway = "Hand over to municipal collection workers in a dedicated separate bag, or return to a pharmacy take-back programme where available."
                reason = "Flushing pharmaceuticals contaminates water bodies and promotes antimicrobial resistance."
            elif item_type == "e-waste":
                category = "E-waste (Consumer Electronics / IT)"
                handling = "Bundle cords neatly. Do not burn or mix with wet waste."
                pathway = "Deposit at an authorized CPCB/SPCB e-waste collection point or producer take-back facility. Do not discard in general household bins."
                reason = "Contains recyclable metals, but burning releases toxic dioxins and heavy metals."
            elif item_type == "chemical":
                category = "Domestic Hazardous Waste (Chemical)"
                handling = "Keep sealed in original container. Never pour down drains or mix with other waste."
                pathway = "Contact your municipal authority for hazardous household waste collection. Do not place in regular bins."
                reason = "Chemical waste contaminates soil and groundwater and poses fire or toxicity risks."
            elif item_type == "wet":
                category = "Wet / Biodegradable Waste"
                handling = "Collect in a separate container. Do not mix with dry or hazardous waste."
                pathway = "Place in the Green bin and hand over to door-to-door municipal collection workers daily for composting."
                reason = "Biodegradable organic matter must be composted separately to prevent contamination of recyclables and reduce landfill load."
            else:
                category = "Household Solid Waste"
                handling = "Segregate at source into designated municipal bins (Green for wet/organic, Blue for dry/recyclable)."
                pathway = "Hand over to your municipal doorstep collection service on the scheduled collection day."
                reason = "Mandatory source segregation under Solid Waste Management Rules, 2016."

            decisions.append(WasteItemDecision(
                item_name=item.capitalize(),
                detected_category=category,
                handling_instruction=handling,
                disposal_pathway=pathway,
                hazard_reason=reason,
                confidence="limited",
                regulatory_source=source
            ))

        return DisposalPlanResponse(
            location=location,
            items=decisions,
            general_advisory=f"Never mix hazardous or electronic waste into ordinary wet/dry garbage. Consult your local municipal authority in {location} for verified collection schedules and drop-off points."
        )


# Global singleton
decision_engine = DecisionEngine()
