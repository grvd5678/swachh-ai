"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { WasteInputForm } from "@/components/WasteInputForm";
import { DisposalCard } from "@/components/DisposalCard";
import { DisposalPlanResponse } from "@/types";
import {
  Recycle,
  AlertTriangle,
  Database,
  Cpu,
  Cloud,
  CheckCircle,
} from "lucide-react";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [plan, setPlan] = useState<DisposalPlanResponse | null>(null);

  const handleGetPlan = async (wasteDescription: string, location: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/disposal-plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          waste_description: wasteDescription,
          location: location,
        }),
      });

      if (!response.ok) {
        throw new Error(`API returned HTTP ${response.status}`);
      }

      const data: DisposalPlanResponse = await response.json();
      setPlan(data);
    } catch (err: unknown) {
      console.error("Backend API request failed:", err);
      setError(
        "Unable to generate your disposal plan. The Swachh.ai decision engine could not be reached. Please ensure the backend is running and try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Header />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col gap-10">
        {/* Hero Section */}
        <div className="text-center max-w-3xl mx-auto flex flex-col items-center gap-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
            <Recycle className="h-3.5 w-3.5" />
            <span>AI Waste-Disposal Decision Assistant</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Know your waste. <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 via-teal-300 to-emerald-500">
              Know what to do.
            </span>
          </h1>

          <p className="text-sm sm:text-base text-slate-400 max-w-xl">
            Ordinary garbage is simple. But power banks, CFL bulbs, and expired
            medicines cause severe contamination when discarded incorrectly.
            Get an authoritative, location-aware disposal plan in seconds.
          </p>

          <div className="flex items-center gap-4 text-xs font-medium text-slate-400 mt-2">
            <span className="flex items-center gap-1.5">
              <CheckCircle className="h-4 w-4 text-emerald-400" />
              Not a generic chatbot
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle className="h-4 w-4 text-emerald-400" />
              Actionable decisions
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle className="h-4 w-4 text-emerald-400" />
              CPCB / Municipal grounded
            </span>
          </div>
        </div>

        {/* Input Form */}
        <section aria-label="Waste disposal plan input">
          <WasteInputForm onSubmit={handleGetPlan} loading={loading} />
        </section>

        {/* Error State */}
        {error && (
          <div className="rounded-xl border border-rose-500/30 bg-rose-950/20 p-5 flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-rose-400 shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-semibold text-rose-300">Unable to generate disposal plan</p>
              <p className="text-xs text-rose-200/70 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Output Section */}
        {plan && (
          <section
            id="disposal-plan-results"
            className="flex flex-col gap-6 scroll-mt-20"
            aria-label="Your Disposal Plan"
          >
            <div className="flex items-center justify-between flex-wrap gap-3 pb-2 border-b border-slate-800">
              <div>
                <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
                  <Recycle className="h-7 w-7 text-emerald-400" />
                  <span>Your Disposal Plan</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Actionable instructions tailored for:{" "}
                  <strong className="text-slate-200">{plan.location}</strong>
                </p>
              </div>

              <div className="text-xs text-slate-400 px-3 py-1 rounded-lg bg-slate-900 border border-slate-800">
                {plan.items.length} items identified and analyzed
              </div>
            </div>

            {/* Overarching Advisory */}
            <div className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-4 flex items-start gap-3">
              <AlertTriangle className="h-5 w-5 text-amber-400 shrink-0 mt-0.5" />
              <div className="text-xs text-amber-200/90 leading-relaxed">
                <strong className="font-semibold text-amber-300">
                  ⚠️ Critical Citizen Safety Rule:{" "}
                </strong>
                {plan.general_advisory}
              </div>
            </div>

            {/* Itemized Disposal Cards */}
            <div className="grid grid-cols-1 gap-6">
              {plan.items.map((item, index) => (
                <DisposalCard key={index} item={item} />
              ))}
            </div>
          </section>
        )}

        {/* Architecture & Hackathon Credibility Section */}
        <section className="mt-8 rounded-2xl border border-slate-800/80 bg-slate-900/40 p-6 sm:p-8 flex flex-col gap-6">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <Cpu className="h-4 w-4 text-emerald-400" />
              How Swachh.ai Works Under The Hood
            </h3>
            <span className="text-xs text-slate-500">
              WeMakeDevs AWS Track 03: Waste & Energy
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs">
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col gap-1.5">
              <div className="font-semibold text-emerald-400 flex items-center gap-1.5">
                <Recycle className="h-4 w-4" />
                1. Item Identification
              </div>
              <p className="text-slate-400 leading-relaxed">
                Splits multi-item descriptions into individual physical waste streams.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col gap-1.5">
              <div className="font-semibold text-sky-400 flex items-center gap-1.5">
                <Database className="h-4 w-4" />
                2. RAG Retrieval
              </div>
              <p className="text-slate-400 leading-relaxed">
                Queries ChromaDB for official CPCB SWM, E-Waste & local KMC bye-laws.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col gap-1.5">
              <div className="font-semibold text-amber-400 flex items-center gap-1.5">
                <Cpu className="h-4 w-4" />
                3. Gemini 3.5 Flash-Lite
              </div>
              <p className="text-slate-400 leading-relaxed">
                Generates structured, typed JSON decisions grounded in retrieved law.
              </p>
            </div>

            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800/80 flex flex-col gap-1.5">
              <div className="font-semibold text-teal-400 flex items-center gap-1.5">
                <Cloud className="h-4 w-4" />
                4. AWS Cloud Deployment
              </div>
              <p className="text-slate-400 leading-relaxed">
                S3 knowledge repository, ECS Express Mode + Fargate backend, CloudWatch monitoring.
              </p>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>
          Swachh.ai — Built by Gourav Das for WeMakeDevs AWS Hackathon (Track 03: Waste & Energy)
        </p>
      </footer>
    </div>
  );
}
