"use strict";

import React from "react";
import { Recycle, ShieldCheck, Sparkles } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-emerald-900/30 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-950/50">
            <Recycle className="h-6 w-6 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-white flex items-center">
                Swachh<span className="text-emerald-400">.ai</span>
              </span>
              <span className="px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Track 03: Waste & Energy
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">
              Know your waste. Know what to do.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
            <span>Authoritative RAG Grounded</span>
          </div>
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
            <Sparkles className="h-3.5 w-3.5 text-amber-400" />
            <span>Decision Engine</span>
          </div>
        </div>
      </div>
    </header>
  );
}

