"use client";

import React from "react";
import {
  BatteryWarning,
  Lightbulb,
  Pill,
  Cable,
  FlaskConical,
  Trash2,
  CheckCircle2,
  FileText,
  MapPin,
  ShieldAlert,
} from "lucide-react";
import { WasteItemDecision } from "@/types";

interface DisposalCardProps {
  item: WasteItemDecision;
}

export function DisposalCard({ item }: DisposalCardProps) {
  // Determine representative icon
  const getIcon = () => {
    const name = item.item_name.toLowerCase();
    const cat = item.detected_category.toLowerCase();

    if (name.includes("power bank") || name.includes("battery") || cat.includes("battery")) {
      return <BatteryWarning className="h-6 w-6 text-amber-400" />;
    }
    if (name.includes("cfl") || name.includes("bulb") || name.includes("tube") || name.includes("lamp")) {
      return <Lightbulb className="h-6 w-6 text-yellow-300" />;
    }
    if (name.includes("medicine") || name.includes("paracetamol") || name.includes("syrup") || cat.includes("pharmaceutical")) {
      return <Pill className="h-6 w-6 text-rose-400" />;
    }
    if (name.includes("charger") || name.includes("cable") || name.includes("cord") || cat.includes("electronic")) {
      return <Cable className="h-6 w-6 text-sky-400" />;
    }
    if (name.includes("paint") || name.includes("chemical") || name.includes("pesticide")) {
      return <FlaskConical className="h-6 w-6 text-orange-400" />;
    }
    return <Trash2 className="h-6 w-6 text-emerald-400" />;
  };

  // Confidence styling
  const getConfidenceBadge = () => {
    if (item.confidence === "high") {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
          High Confidence
        </span>
      );
    }
    if (item.confidence === "limited") {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
          <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
          Limited Guidance
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">
        <span className="h-1.5 w-1.5 rounded-full bg-rose-400" />
        Unsupported Pathway
      </span>
    );
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 shadow-xl transition-all duration-200 hover:border-slate-700 hover:shadow-2xl flex flex-col gap-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700/50 flex items-center justify-center">
            {getIcon()}
          </div>
          <div>
            <h3 className="text-lg font-bold text-white tracking-tight">
              {item.item_name}
            </h3>
            <span className="inline-block mt-0.5 text-xs font-medium text-emerald-400">
              {item.detected_category}
            </span>
          </div>
        </div>
        {getConfidenceBadge()}
      </div>

      {/* Main Action Block: WHAT TO DO */}
      <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/20 p-4">
        <div className="flex items-center gap-2 mb-1.5">
          <CheckCircle2 className="h-4 w-4 text-emerald-400 shrink-0" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
            What To Do
          </h4>
        </div>
        <p className="text-sm font-medium text-slate-200 leading-relaxed pl-6">
          {item.handling_instruction}
        </p>
      </div>

      {/* Disposal Pathway */}
      <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-4">
        <div className="flex items-center gap-2 mb-1.5">
          <MapPin className="h-4 w-4 text-sky-400 shrink-0" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-sky-400">
            Local Disposal Pathway
          </h4>
        </div>
        <p className="text-sm text-slate-300 leading-relaxed pl-6">
          {item.disposal_pathway}
        </p>
      </div>

      {/* Why / Hazard Reason */}
      <div className="rounded-xl border border-amber-500/20 bg-amber-950/15 p-4">
        <div className="flex items-center gap-2 mb-1.5">
          <ShieldAlert className="h-4 w-4 text-amber-400 shrink-0" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400">
            Why (Environmental & Safety Rationale)
          </h4>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed pl-6">
          {item.hazard_reason}
        </p>
      </div>

      {/* Citation / Source Footer */}
      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-1.5">
          <FileText className="h-3.5 w-3.5 text-slate-500" />
          <span className="font-medium text-slate-400">Source:</span>
          <span className="text-slate-300 truncate max-w-xs sm:max-w-md">
            {item.regulatory_source}
          </span>
        </div>
      </div>
    </div>
  );
}

