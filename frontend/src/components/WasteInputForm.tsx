"use client";

import React, { useState } from "react";
import { MapPin, ArrowRight, Loader2 } from "lucide-react";

interface WasteInputFormProps {
  onSubmit: (wasteDescription: string, location: string) => Promise<void>;
  loading: boolean;
}

const PRESETS = [
  {
    label: "🔋 Power bank + 💡 CFL + 💊 Medicine",
    text: "I have a broken swollen power bank, an old CFL bulb, and some expired paracetamol tablets.",
    location: "Kolkata, West Bengal",
  },
  {
    label: "🔌 Charger & Damaged Cables",
    text: "An old phone charger with frayed copper wires and a cracked mobile adapter.",
    location: "Kolkata, West Bengal",
  },
  {
    label: "🧴 Chemical Can & Plastic Packets",
    text: "Empty pesticide spray can, half-used paint thinner, and clean milk pouches.",
    location: "Kolkata, West Bengal",
  },
];

const CITIES = ["Kolkata", "Delhi", "Bengaluru", "Mumbai"];

export function WasteInputForm({ onSubmit, loading }: WasteInputFormProps) {
  const [wasteDescription, setWasteDescription] = useState(
    "I have a broken power bank, an old CFL bulb, and expired medicine."
  );
  const [location, setLocation] = useState("Kolkata, West Bengal");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!wasteDescription.trim()) return;
    onSubmit(wasteDescription, location);
  };

  const applyPreset = (presetText: string, presetLoc: string) => {
    setWasteDescription(presetText);
    setLocation(presetLoc);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/90 p-6 sm:p-8 shadow-2xl backdrop-blur-sm">
      <form onSubmit={handleSubmit} className="flex flex-col gap-6">
        {/* Waste Input */}
        <div>
          <label
            htmlFor="waste-input"
            className="block text-sm font-semibold text-slate-200 mb-2"
          >
            What do you need to dispose of?
          </label>
          <textarea
            id="waste-input"
            rows={3}
            value={wasteDescription}
            onChange={(e) => setWasteDescription(e.target.value)}
            placeholder="e.g. A swollen laptop battery, fused tube light, and old syrup bottles..."
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 transition-all resize-none"
            disabled={loading}
            required
          />

          {/* Quick Presets for Demo */}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="text-xs text-slate-400 font-medium">Try demo presets:</span>
            {PRESETS.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => applyPreset(preset.text, preset.location)}
                className="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700/80 text-slate-300 transition-colors"
                disabled={loading}
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        {/* Location Input */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label
              htmlFor="location-input"
              className="block text-sm font-semibold text-slate-200"
            >
              Where are you? (Location Context)
            </label>
            <span className="text-xs text-emerald-400 font-medium flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              Prioritizes local municipal bye-laws
            </span>
          </div>

          <div className="relative">
            <MapPin className="absolute left-3.5 top-3.5 h-4 w-4 text-slate-400" />
            <input
              id="location-input"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Kolkata, West Bengal"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 transition-all"
              disabled={loading}
              required
            />
          </div>

          {/* Quick City Chips */}
          <div className="mt-2.5 flex items-center gap-2">
            <span className="text-xs text-slate-400">Quick select:</span>
            {CITIES.map((city) => (
              <button
                key={city}
                type="button"
                onClick={() => setLocation(`${city}, India`)}
                className={`px-2 py-0.5 text-xs rounded-md border transition-colors ${
                  location.toLowerCase().includes(city.toLowerCase())
                    ? "bg-emerald-500/20 border-emerald-500/40 text-emerald-300"
                    : "bg-slate-800/60 border-slate-700/60 text-slate-400 hover:text-slate-200"
                }`}
                disabled={loading}
              >
                {city}
              </button>
            ))}
          </div>
        </div>

        {/* CTA Button */}
        <div>
          <button
            type="submit"
            disabled={loading || !wasteDescription.trim()}
            className="w-full h-12 rounded-xl bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 text-slate-950 font-bold text-sm sm:text-base tracking-wide flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 hover:from-emerald-400 hover:to-teal-500 active:scale-[0.99] transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                <span>Consulting Authoritative RAG & Gemini...</span>
              </>
            ) : (
              <>
                <span>Get My Disposal Plan</span>
                <ArrowRight className="h-5 w-5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

