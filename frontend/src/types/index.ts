export interface WasteItemDecision {
  item_name: string;
  detected_category: string;
  handling_instruction: string;
  disposal_pathway: string;
  hazard_reason: string;
  confidence: "high" | "limited" | "unsupported";
  regulatory_source: string;
}

export interface DisposalPlanResponse {
  location: string;
  items: WasteItemDecision[];
  general_advisory: string;
}

